# bot_db_manager.py
# Database management for bots
import sqlite3
import json
from datetime import datetime

# Database file path
BOT_DB_FILE = 'bots.db'

def get_bot_db_connection():
    """Create and return a database connection for bots"""
    conn = sqlite3.connect(BOT_DB_FILE)
    conn.row_factory = sqlite3.Row  # This allows column access by name
    return conn

def init_bot_database():
    """Initialize the bots database and create tables if they don't exist"""
    conn = get_bot_db_connection()
    cursor = conn.cursor()
    
    # Create users table for authentication/roles
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'viewer',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create bots table if it doesn't exist (Enhanced schema)
    # Note: bot_name is NOT UNIQUE to allow versioning (draft + live versions)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bot_name TEXT NOT NULL,
            initial_greeting TEXT NOT NULL,
            configuration_json TEXT NOT NULL,
            description TEXT DEFAULT '',
            status TEXT DEFAULT 'published',
            language TEXT DEFAULT 'myanmar',
            owner_id INTEGER,
            is_live INTEGER DEFAULT 1,
            version_number INTEGER DEFAULT 1,
            parent_bot_id INTEGER,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(owner_id) REFERENCES users(id),
            FOREIGN KEY(parent_bot_id) REFERENCES bots(id)
        )
    ''')
    
    # Migrate existing table: Remove UNIQUE constraint from bot_name if it exists
    # SQLite doesn't support DROP CONSTRAINT, so we need to recreate the table
    try:
        # Check if table exists and get its schema
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='bots'")
        table_result = cursor.fetchone()
        
        if table_result and table_result[0]:
            table_sql = table_result[0]
            # Check if UNIQUE constraint exists on bot_name
            if 'UNIQUE' in table_sql.upper() and 'bot_name' in table_sql:
                print("Migrating bots table to remove UNIQUE constraint from bot_name...")
                
                # Get row count
                cursor.execute("SELECT COUNT(*) FROM bots")
                row_count = cursor.fetchone()[0]
                
                # Drop bots_new if it exists (from previous failed migration)
                cursor.execute('DROP TABLE IF EXISTS bots_new')
                
                # Create new table without UNIQUE constraint
                cursor.execute('''
                    CREATE TABLE bots_new (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        bot_name TEXT NOT NULL,
                        initial_greeting TEXT NOT NULL,
                        configuration_json TEXT NOT NULL,
                        description TEXT DEFAULT '',
                        status TEXT DEFAULT 'published',
                        language TEXT DEFAULT 'myanmar',
                        owner_id INTEGER,
                        is_live INTEGER DEFAULT 1,
                        version_number INTEGER DEFAULT 1,
                        parent_bot_id INTEGER,
                        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                        updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY(owner_id) REFERENCES users(id),
                        FOREIGN KEY(parent_bot_id) REFERENCES bots(id)
                    )
                ''')
                
                # Copy data if table has data
                if row_count > 0:
                    # Get list of columns that exist in old table
                    cursor.execute("PRAGMA table_info(bots)")
                    old_columns = [row[1] for row in cursor.fetchall()]
                    
                    # Build column list for SELECT (only columns that exist)
                    select_cols = []
                    insert_cols = []
                    for col in ['id', 'bot_name', 'initial_greeting', 'configuration_json', 
                               'description', 'status', 'language', 'owner_id', 
                               'is_live', 'version_number', 'parent_bot_id', 'created_at', 'updated_at']:
                        if col in old_columns:
                            select_cols.append(col)
                            insert_cols.append(col)
                    
                    # Build the INSERT statement
                    insert_sql = f'''
                        INSERT INTO bots_new ({', '.join(insert_cols)})
                        SELECT {', '.join(select_cols)}
                        FROM bots
                    '''
                    cursor.execute(insert_sql)
                
                # Drop old table and rename new one
                cursor.execute('DROP TABLE bots')
                cursor.execute('ALTER TABLE bots_new RENAME TO bots')
                
                # Recreate indexes
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_bots_live ON bots(bot_name, is_live)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_bots_name ON bots(bot_name)')
                
                conn.commit()
                print("Migration completed: UNIQUE constraint removed from bot_name")
    except Exception as e:
        # Migration failed, but table might already be correct
        print(f"Migration check completed (may already be migrated): {e}")
        conn.rollback()
        pass
    
    # Ensure owner_id column exists for legacy databases
    cursor.execute("PRAGMA table_info(bots)")
    bot_columns = [row[1] for row in cursor.fetchall()]
    if 'owner_id' not in bot_columns:
        try:
            cursor.execute('ALTER TABLE bots ADD COLUMN owner_id INTEGER')
        except sqlite3.OperationalError:
            # Column already exists (race condition) - ignore
            pass
    
    # Add versioning columns if they don't exist
    if 'is_live' not in bot_columns:
        try:
            cursor.execute('ALTER TABLE bots ADD COLUMN is_live INTEGER DEFAULT 1')
        except sqlite3.OperationalError:
            pass
    
    if 'version_number' not in bot_columns:
        try:
            cursor.execute('ALTER TABLE bots ADD COLUMN version_number INTEGER DEFAULT 1')
        except sqlite3.OperationalError:
            pass
    
    if 'parent_bot_id' not in bot_columns:
        try:
            cursor.execute('ALTER TABLE bots ADD COLUMN parent_bot_id INTEGER')
        except sqlite3.OperationalError:
            pass
    
    # Migrate status field: Update existing bots to 'published' if status is 'active' or NULL
    try:
        cursor.execute("UPDATE bots SET status = 'published' WHERE status IS NULL OR status = 'active' OR status = ''")
        conn.commit()
        print("Status field migration completed: Existing bots set to 'published'")
    except Exception as e:
        print(f"Status migration note: {e}")
        pass
    
    # Create bot_versions table for version history
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bot_versions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bot_id INTEGER NOT NULL,
            bot_name TEXT NOT NULL,
            version_number INTEGER NOT NULL,
            initial_greeting TEXT NOT NULL,
            configuration_json TEXT NOT NULL,
            is_live INTEGER DEFAULT 0,
            is_draft INTEGER DEFAULT 0,
            created_by INTEGER,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            published_at TEXT,
            FOREIGN KEY (bot_id) REFERENCES bots(id) ON DELETE CASCADE,
            FOREIGN KEY (created_by) REFERENCES users(id),
            UNIQUE(bot_id, version_number)
        )
    ''')
    
    # Create indexes for versioning
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_bot_versions_bot_id ON bot_versions(bot_id, version_number)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_bot_versions_live ON bot_versions(bot_id, is_live)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_bots_live ON bots(bot_name, is_live)')
    
    # Create conversation_logs table for analytics
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversation_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bot_id INTEGER NOT NULL,
            bot_name TEXT NOT NULL,
            user_message TEXT NOT NULL,
            bot_response TEXT NOT NULL,
            session_id TEXT,
            step_index INTEGER,
            step_type TEXT,
            intent TEXT,
            confidence REAL,
            api_latency REAL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (bot_id) REFERENCES bots(id) ON DELETE CASCADE
        )
    ''')
    
    # Add new columns if they don't exist (for existing databases)
    try:
        cursor.execute("ALTER TABLE conversation_logs ADD COLUMN step_type TEXT")
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    try:
        cursor.execute("ALTER TABLE conversation_logs ADD COLUMN api_latency REAL")
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    # Create bot_analytics table for aggregated stats
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bot_analytics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bot_id INTEGER NOT NULL,
            bot_name TEXT NOT NULL,
            date TEXT NOT NULL,
            total_conversations INTEGER DEFAULT 0,
            total_messages INTEGER DEFAULT 0,
            unique_users INTEGER DEFAULT 0,
            avg_response_time REAL DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (bot_id) REFERENCES bots(id) ON DELETE CASCADE,
            UNIQUE(bot_id, date)
        )
    ''')
    
    # Create indexes for better performance
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_bot_name ON bots(bot_name)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_bot_owner ON bots(owner_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_conversation_bot ON conversation_logs(bot_id, created_at)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_analytics_bot_date ON bot_analytics(bot_id, date)')
    
    conn.commit()
    conn.close()
    print(f"Bots database initialized: {BOT_DB_FILE}")

    # Ensure there is at least one owner account available
    ensure_default_owner()

def ensure_default_owner():
    """Create a default owner account if no users exist"""
    conn = get_bot_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT COUNT(*) FROM users')
        user_count = cursor.fetchone()[0]
        if user_count == 0:
            from werkzeug.security import generate_password_hash
            default_username = 'admin'
            default_email = 'admin@example.com'
            default_password = 'admin123'
            password_hash = generate_password_hash(default_password)
            cursor.execute('''
                INSERT INTO users (username, email, password_hash, role)
                VALUES (?, ?, ?, ?)
            ''', (default_username, default_email, password_hash, 'owner'))
            conn.commit()
            print("Default owner account created (username: admin, password: admin123)")
    except Exception as e:
        print(f"Error ensuring default owner: {e}")
    finally:
        conn.close()

def save_bot(bot_name, initial_greeting, steps_data, owner_id=None, publish=False):
    """
    Save or update a bot configuration (creates draft by default, or publishes if publish=True)
    
    Args:
        bot_name (str): The name of the bot (must be unique)
        initial_greeting (str): The initial greeting message
        steps_data (list): List of step dictionaries containing type and content
        owner_id (int): Owner user ID
        publish (bool): If True, publish immediately; if False, save as draft
    
    Returns:
        tuple: (success: bool, message: str, bot_id: int or None)
    """
    conn = get_bot_db_connection()
    cursor = conn.cursor()
    
    try:
        # Convert steps_data to JSON string
        configuration_json = json.dumps(steps_data, ensure_ascii=False)
        updated_at = datetime.now().isoformat()
        
        # Check if bot with this name already exists
        cursor.execute('''
            SELECT id, owner_id, version_number, is_live 
            FROM bots 
            WHERE bot_name = ?
            ORDER BY version_number DESC, is_live DESC
            LIMIT 1
        ''', (bot_name,))
        existing_bot = cursor.fetchone()
        
        if existing_bot:
            # Check if there's a draft
            cursor.execute('''
                SELECT id, version_number
                FROM bots
                WHERE bot_name = ? AND is_live = 0
                ORDER BY version_number DESC
                LIMIT 1
            ''', (bot_name,))
            draft = cursor.fetchone()
            
            if draft:
                # Update existing draft
                owner_to_use = owner_id if owner_id is not None else existing_bot['owner_id']
                status_to_set = 'published' if publish else 'draft'
                cursor.execute('''
                    UPDATE bots 
                    SET initial_greeting = ?, 
                        configuration_json = ?, 
                        owner_id = ?, 
                        status = ?,
                        updated_at = ?
                    WHERE id = ?
                ''', (initial_greeting, configuration_json, owner_to_use, status_to_set, updated_at, draft['id']))
                
                bot_id = draft['id']
                
                # Update version history
                cursor.execute('''
                    UPDATE bot_versions
                    SET initial_greeting = ?, configuration_json = ?, created_at = ?
                    WHERE bot_id = ? AND version_number = ?
                ''', (initial_greeting, configuration_json, updated_at, bot_id, draft['version_number']))
                
                conn.commit()
                conn.close()
                
                print(f"Draft updated for bot '{bot_name}' (ID: {bot_id})")
                
                # If publish requested, publish the draft
                if publish:
                    result = publish_draft(bot_name, owner_id)
                    if result[0]:
                        return (True, f"Bot '{bot_name}' saved and published successfully", bot_id)
                    else:
                        return (True, f"Bot '{bot_name}' saved as draft. {result[1]}", bot_id)
                
                return (True, f"Draft updated for bot '{bot_name}'", bot_id)
            else:
                # No draft exists, create new draft
                return create_bot_draft(bot_name, initial_greeting, steps_data, owner_id)
        else:
            # New bot - create first version
            if publish:
                # Create as published version
                cursor.execute('''
                    INSERT INTO bots (bot_name, initial_greeting, configuration_json, owner_id, 
                                    version_number, is_live, status, updated_at)
                    VALUES (?, ?, ?, ?, 1, 1, 'published', ?)
                ''', (bot_name, initial_greeting, configuration_json, owner_id, updated_at))
                
                bot_id = cursor.lastrowid
                
                # Save to version history
                cursor.execute('''
                    INSERT INTO bot_versions (bot_id, bot_name, version_number, initial_greeting, 
                                            configuration_json, is_live, is_draft, created_by, 
                                            created_at, published_at)
                    VALUES (?, ?, 1, ?, ?, 1, 0, ?, ?, ?)
                ''', (bot_id, bot_name, initial_greeting, configuration_json, 
                      owner_id, updated_at, updated_at))
                
                conn.commit()
                conn.close()
                
                print(f"Bot '{bot_name}' created and published (ID: {bot_id})")
                return (True, f"Bot '{bot_name}' created and published successfully", bot_id)
            else:
                # Create as draft
                return create_bot_draft(bot_name, initial_greeting, steps_data, owner_id)
            
    except sqlite3.IntegrityError as e:
        conn.rollback()
        conn.close()
        error_str = str(e)
        if 'UNIQUE' in error_str or 'unique' in error_str:
            error_msg = f"Database constraint violation: Bot name '{bot_name}' may have UNIQUE constraint. Please run database migration."
            print(f"IntegrityError: {error_str}")
            print(f"Error saving bot: {error_msg}")
        else:
            error_msg = f"Database constraint violation: {error_str}"
            print(f"Error saving bot: {error_msg}")
        return (False, error_msg, None)
    except Exception as e:
        conn.rollback()
        conn.close()
        error_msg = f"Error saving bot: {str(e)}"
        print(error_msg)
        return (False, error_msg, None)

def get_all_bots(user_id=None, role='viewer'):
    """
    Fetch all unique bots from the database
    Returns one entry per bot_name (preferring live version, then latest draft)
    
    Returns:
        list: List of dictionaries containing bot data
    """
    conn = get_bot_db_connection()
    cursor = conn.cursor()
    
    try:
        # Get all bots with versioning info
        if role == 'owner' or user_id is None:
            cursor.execute('''
                SELECT id, bot_name, initial_greeting, configuration_json, owner_id, 
                       version_number, is_live, status, created_at, updated_at
                FROM bots
                ORDER BY bot_name, is_live DESC, version_number DESC
            ''')
        else:
            cursor.execute('''
                SELECT id, bot_name, initial_greeting, configuration_json, owner_id,
                       version_number, is_live, status, created_at, updated_at
                FROM bots
                WHERE owner_id = ? OR owner_id IS NULL
                ORDER BY bot_name, is_live DESC, version_number DESC
            ''', (user_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        # Group by bot_name and keep only the first (preferred) version for each bot
        # Priority: live version > latest draft
        bots_dict = {}
        for row in rows:
            bot_name = row['bot_name']
            
            # Safely get versioning info (handle missing columns)
            # sqlite3.Row doesn't have .get(), use try/except or check keys
            try:
                row_is_live = row['is_live'] if 'is_live' in row.keys() else 1
            except (KeyError, IndexError):
                row_is_live = 1
            try:
                row_version = row['version_number'] if 'version_number' in row.keys() else 1
            except (KeyError, IndexError):
                row_version = 1
            
            # If we haven't seen this bot, or if current row is live and previous wasn't
            if bot_name not in bots_dict:
                bots_dict[bot_name] = row
            else:
                existing_row = bots_dict[bot_name]
                try:
                    existing_is_live = existing_row['is_live'] if 'is_live' in existing_row.keys() else 1
                except (KeyError, IndexError):
                    existing_is_live = 1
                try:
                    existing_version = existing_row['version_number'] if 'version_number' in existing_row.keys() else 1
                except (KeyError, IndexError):
                    existing_version = 1
                
                # Replace with live version if we found one, or with newer version if both are same type
                if row_is_live == 1 and existing_is_live != 1:
                    bots_dict[bot_name] = row
                elif row_is_live == existing_is_live and row_version > existing_version:
                    # Same type (both live or both draft), prefer newer version
                    bots_dict[bot_name] = row
        
        # Convert to list of dictionaries
        bots = []
        for bot_name, row in bots_dict.items():
            # Safely get versioning fields from Row object
            try:
                version_number = row['version_number'] if 'version_number' in row.keys() else 1
            except (KeyError, IndexError):
                version_number = 1
            try:
                is_live = row['is_live'] if 'is_live' in row.keys() else 1
            except (KeyError, IndexError):
                is_live = 1
            try:
                status = row['status'] if 'status' in row.keys() else 'published'
            except (KeyError, IndexError):
                status = 'published'
            
            bots.append({
                'id': row['id'],
                'bot_name': row['bot_name'],
                'initial_greeting': row['initial_greeting'],
                'configuration_json': row['configuration_json'],
                'owner_id': row['owner_id'],
                'version_number': version_number,
                'is_live': bool(is_live),
                'status': status,
                'steps': json.loads(row['configuration_json']),  # Parse JSON back to list
                'created_at': row['created_at'],
                'updated_at': row['updated_at']
            })
        
        # Sort by updated_at descending
        bots.sort(key=lambda x: x['updated_at'] or '', reverse=True)
        
        print(f"Retrieved {len(bots)} unique bots from database")
        return bots
    except Exception as e:
        conn.close()
        print(f"Error fetching bots: {e}")
        import traceback
        traceback.print_exc()
        return []

def get_bot_by_name(bot_name, use_draft=False):
    """
    Fetch a bot by its name
    
    Args:
        bot_name (str): The name of the bot
        use_draft (bool): If True, return draft version; if False, return live version
    
    Returns:
        dict or None: Bot data if found, None otherwise
    """
    if use_draft:
        return get_bot_draft_version(bot_name)
    else:
        # For chat API, always use live version
        live_bot = get_bot_live_version(bot_name)
        if live_bot:
            return live_bot
        
        # Fallback: if no live version, try to get any version
        conn = get_bot_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT id, bot_name, initial_greeting, configuration_json, owner_id, 
                       version_number, is_live, created_at, updated_at
                FROM bots
                WHERE bot_name = ?
                ORDER BY version_number DESC
                LIMIT 1
            ''', (bot_name,))
            
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return {
                    'id': row['id'],
                    'bot_name': row['bot_name'],
                    'initial_greeting': row['initial_greeting'],
                    'configuration_json': row['configuration_json'],
                    'owner_id': row['owner_id'],
                    'version_number': row['version_number'],
                    'is_live': bool(row['is_live']),
                    'steps': json.loads(row['configuration_json']),
                    'created_at': row['created_at'],
                    'updated_at': row['updated_at']
                }
            return None
        except Exception as e:
            conn.close()
            print(f"Error fetching bot: {e}")
            return None

def delete_bot(bot_name):
    """
    Delete a bot from the database (deletes all versions)
    
    Args:
        bot_name (str): The name of the bot to delete
    
    Returns:
        bool: True if deletion was successful, False otherwise
    """
    conn = get_bot_db_connection()
    cursor = conn.cursor()
    
    try:
        # Delete all versions of the bot (conversation_logs and bot_versions will be deleted automatically due to CASCADE)
        cursor.execute('''
            DELETE FROM bots
            WHERE bot_name = ?
        ''', (bot_name,))
        
        if cursor.rowcount > 0:
            conn.commit()
            conn.close()
            print(f"Bot '{bot_name}' and all its versions deleted successfully")
            return True
        else:
            conn.close()
            print(f"Bot '{bot_name}' not found")
            return False
    except Exception as e:
        conn.rollback()
        conn.close()
        print(f"Error deleting bot: {e}")
        import traceback
        traceback.print_exc()
        return False

def create_user(username, email, password_hash, role='viewer'):
    """Create a new user account"""
    conn = get_bot_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO users (username, email, password_hash, role)
            VALUES (?, ?, ?, ?)
        ''', (username, email, password_hash, role))
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return True, user_id, None
    except sqlite3.IntegrityError as e:
        conn.close()
        return False, None, 'Username or email already exists'
    except Exception as e:
        conn.close()
        return False, None, str(e)

def get_user_by_username(username):
    conn = get_bot_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            SELECT id, username, email, password_hash, role, created_at
            FROM users
            WHERE username = ?
        ''', (username,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return dict(row)
        return None
    except Exception as e:
        conn.close()
        print(f"Error fetching user: {e}")
        return None

def get_user_by_email(email):
    conn = get_bot_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT id, username, email, password_hash, role, created_at
            FROM users
            WHERE email = ?
        """, (email,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return dict(row)
        return None
    except Exception as e:
        conn.close()
        print(f"Error fetching user by email: {e}")
        return None


def get_user_by_id(user_id):
    conn = get_bot_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            SELECT id, username, email, role, created_at
            FROM users
            WHERE id = ?
        ''', (user_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return dict(row)
        return None
    except Exception as e:
        conn.close()
        print(f"Error fetching user: {e}")
        return None

def list_users():
    conn = get_bot_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            SELECT id, username, email, role, created_at
            FROM users
            ORDER BY created_at DESC
        ''')
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    except Exception as e:
        conn.close()
        print(f"Error listing users: {e}")
        return []

def update_user_role(user_id, role):
    conn = get_bot_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            UPDATE users SET role = ? WHERE id = ?
        ''', (role, user_id))
        conn.commit()
        conn.close()
        return cursor.rowcount > 0
    except Exception as e:
        conn.close()
        print(f"Error updating role: {e}")
        return False

def update_user_role_by_email(email, role):
    """Update a user's role by their email address."""
    conn = get_bot_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            UPDATE users SET role = ? WHERE email = ?
        ''', (role, email))
        conn.commit()
        updated = cursor.rowcount > 0
        conn.close()
        if updated:
            print(f"Updated role for {email} to {role}")
        else:
            print(f"No user found with email {email}")
        return updated
    except Exception as e:
        conn.close()
        print(f"Error updating role by email: {e}")
        return False

def delete_user(user_id):
    """
    Delete a user from the database
    
    Args:
        user_id (int): The ID of the user to delete
    
    Returns:
        bool: True if deletion was successful, False otherwise
    """
    conn = get_bot_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            DELETE FROM users
            WHERE id = ?
        ''', (user_id,))
        
        if cursor.rowcount > 0:
            conn.commit()
            conn.close()
            print(f"User ID {user_id} deleted successfully")
            return True
        else:
            conn.close()
            print(f"User ID {user_id} not found")
            return False
    except Exception as e:
        conn.rollback()
        conn.close()
        print(f"Error deleting user: {e}")
        return False

# ==================== BOT VERSIONING FUNCTIONS ====================

def get_bot_live_version(bot_name):
    """
    Get the live (published) version of a bot
    
    Args:
        bot_name (str): The name of the bot
    
    Returns:
        dict or None: Live bot data if found, None otherwise
    """
    conn = get_bot_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            SELECT id, bot_name, initial_greeting, configuration_json, owner_id, 
                   version_number, is_live, created_at, updated_at
            FROM bots
            WHERE bot_name = ? AND is_live = 1
            ORDER BY version_number DESC
            LIMIT 1
        ''', (bot_name,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'id': row['id'],
                'bot_name': row['bot_name'],
                'initial_greeting': row['initial_greeting'],
                'configuration_json': row['configuration_json'],
                'owner_id': row['owner_id'],
                'version_number': row['version_number'],
                'is_live': bool(row['is_live']),
                'steps': json.loads(row['configuration_json']),
                'created_at': row['created_at'],
                'updated_at': row['updated_at']
            }
        return None
    except Exception as e:
        conn.close()
        print(f"Error fetching live bot version: {e}")
        return None

def get_bot_draft_version(bot_name):
    """
    Get the draft version of a bot
    
    Args:
        bot_name (str): The name of the bot
    
    Returns:
        dict or None: Draft bot data if found, None otherwise
    """
    conn = get_bot_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            SELECT id, bot_name, initial_greeting, configuration_json, owner_id, 
                   version_number, is_live, parent_bot_id, created_at, updated_at
            FROM bots
            WHERE bot_name = ? AND is_live = 0
            ORDER BY version_number DESC
            LIMIT 1
        ''', (bot_name,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'id': row['id'],
                'bot_name': row['bot_name'],
                'initial_greeting': row['initial_greeting'],
                'configuration_json': row['configuration_json'],
                'owner_id': row['owner_id'],
                'version_number': row['version_number'],
                'is_live': bool(row['is_live']),
                'parent_bot_id': row['parent_bot_id'],
                'steps': json.loads(row['configuration_json']),
                'created_at': row['created_at'],
                'updated_at': row['updated_at']
            }
        return None
    except Exception as e:
        conn.close()
        print(f"Error fetching draft bot version: {e}")
        return None

def get_bot_versions(bot_name):
    """
    Get all versions of a bot
    
    Args:
        bot_name (str): The name of the bot
    
    Returns:
        list: List of version dictionaries
    """
    conn = get_bot_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            SELECT id, bot_name, initial_greeting, configuration_json, owner_id, 
                   version_number, is_live, parent_bot_id, created_at, updated_at
            FROM bots
            WHERE bot_name = ?
            ORDER BY version_number DESC, is_live DESC
        ''', (bot_name,))
        
        rows = cursor.fetchall()
        conn.close()
        
        versions = []
        for row in rows:
            versions.append({
                'id': row['id'],
                'bot_name': row['bot_name'],
                'initial_greeting': row['initial_greeting'],
                'configuration_json': row['configuration_json'],
                'owner_id': row['owner_id'],
                'version_number': row['version_number'],
                'is_live': bool(row['is_live']),
                'parent_bot_id': row['parent_bot_id'],
                'steps': json.loads(row['configuration_json']),
                'created_at': row['created_at'],
                'updated_at': row['updated_at']
            })
        return versions
    except Exception as e:
        conn.close()
        print(f"Error fetching bot versions: {e}")
        return []

def create_bot_draft(bot_name, initial_greeting, steps_data, owner_id=None):
    """
    Create a draft version of a bot
    
    Args:
        bot_name (str): The name of the bot
        initial_greeting (str): The initial greeting message
        steps_data (list): List of step dictionaries
        owner_id (int): Owner user ID
    
    Returns:
        tuple: (success: bool, message: str, bot_id: int or None)
    """
    conn = get_bot_db_connection()
    cursor = conn.cursor()
    
    try:
        # Check if bot exists (live or draft)
        cursor.execute('''
            SELECT id, version_number, is_live 
            FROM bots 
            WHERE bot_name = ?
            ORDER BY version_number DESC
            LIMIT 1
        ''', (bot_name,))
        
        existing = cursor.fetchone()
        
        configuration_json = json.dumps(steps_data, ensure_ascii=False)
        updated_at = datetime.now().isoformat()
        
        if existing:
            # Bot exists, create new draft version
            new_version = existing['version_number'] + 1
            parent_bot_id = existing['id']
        else:
            # New bot, create first version as draft
            new_version = 1
            parent_bot_id = None
        
        # Create draft (is_live = 0, status = 'draft')
        cursor.execute('''
            INSERT INTO bots (bot_name, initial_greeting, configuration_json, owner_id, 
                            version_number, is_live, status, parent_bot_id, updated_at)
            VALUES (?, ?, ?, ?, ?, 0, 'draft', ?, ?)
        ''', (bot_name, initial_greeting, configuration_json, owner_id, 
              new_version, parent_bot_id, updated_at))
        
        bot_id = cursor.lastrowid
        
        # Save to version history
        cursor.execute('''
            INSERT INTO bot_versions (bot_id, bot_name, version_number, initial_greeting, 
                                    configuration_json, is_draft, created_by, created_at)
            VALUES (?, ?, ?, ?, ?, 1, ?, ?)
        ''', (bot_id, bot_name, new_version, initial_greeting, 
              configuration_json, owner_id, updated_at))
        
        conn.commit()
        conn.close()
        
        print(f"Draft version {new_version} created for bot '{bot_name}' (ID: {bot_id})")
        return (True, f"Draft version {new_version} created successfully", bot_id)
        
    except Exception as e:
        conn.rollback()
        conn.close()
        error_msg = f"Error creating draft: {str(e)}"
        print(error_msg)
        return (False, error_msg, None)

def publish_draft(bot_name, owner_id=None):
    """
    Publish a draft version (make it live)
    
    Args:
        bot_name (str): The name of the bot
        owner_id (int): Owner user ID for authorization
    
    Returns:
        tuple: (success: bool, message: str)
    """
    conn = get_bot_db_connection()
    cursor = conn.cursor()
    
    try:
        # Get the latest draft
        cursor.execute('''
            SELECT id, version_number, owner_id
            FROM bots
            WHERE bot_name = ? AND is_live = 0
            ORDER BY version_number DESC
            LIMIT 1
        ''', (bot_name,))
        
        draft = cursor.fetchone()
        
        if not draft:
            conn.close()
            return (False, "No draft version found to publish")
        
        # Check authorization if owner_id provided
        if owner_id and draft['owner_id'] != owner_id:
            conn.close()
            return (False, "Unauthorized: You don't own this bot")
        
        # Unpublish current live version (set to draft)
        cursor.execute('''
            UPDATE bots
            SET is_live = 0, status = 'draft'
            WHERE bot_name = ? AND is_live = 1 AND status = 'published'
        ''', (bot_name,))
        
        # Publish the draft
        published_at = datetime.now().isoformat()
        cursor.execute('''
            UPDATE bots
            SET is_live = 1, status = 'published', updated_at = ?
            WHERE id = ?
        ''', (published_at, draft['id']))
        
        # Update version history
        cursor.execute('''
            UPDATE bot_versions
            SET is_live = 1, is_draft = 0, published_at = ?
            WHERE bot_id = ? AND version_number = ?
        ''', (published_at, draft['id'], draft['version_number']))
        
        conn.commit()
        conn.close()
        
        print(f"Draft version {draft['version_number']} published for bot '{bot_name}'")
        return (True, f"Version {draft['version_number']} published successfully")
        
    except Exception as e:
        conn.rollback()
        conn.close()
        error_msg = f"Error publishing draft: {str(e)}"
        print(error_msg)
        return (False, error_msg)

def delete_draft(bot_name, owner_id=None):
    """
    Delete a draft version
    
    Args:
        bot_name (str): The name of the bot
        owner_id (int): Owner user ID for authorization
    
    Returns:
        tuple: (success: bool, message: str)
    """
    conn = get_bot_db_connection()
    cursor = conn.cursor()
    
    try:
        # Get the draft
        cursor.execute('''
            SELECT id, version_number, owner_id
            FROM bots
            WHERE bot_name = ? AND is_live = 0
            ORDER BY version_number DESC
            LIMIT 1
        ''', (bot_name,))
        
        draft = cursor.fetchone()
        
        if not draft:
            conn.close()
            return (False, "No draft version found")
        
        # Check authorization
        if owner_id and draft['owner_id'] != owner_id:
            conn.close()
            return (False, "Unauthorized: You don't own this bot")
        
        # Delete draft
        cursor.execute('DELETE FROM bots WHERE id = ?', (draft['id'],))
        
        # Delete from version history
        cursor.execute('''
            DELETE FROM bot_versions 
            WHERE bot_id = ? AND version_number = ?
        ''', (draft['id'], draft['version_number']))
        
        conn.commit()
        conn.close()
        
        print(f"Draft version {draft['version_number']} deleted for bot '{bot_name}'")
        return (True, f"Draft version {draft['version_number']} deleted successfully")
        
    except Exception as e:
        conn.rollback()
        conn.close()
        error_msg = f"Error deleting draft: {str(e)}"
        print(error_msg)
        return (False, error_msg)

def log_conversation(bot_id, bot_name, user_message, bot_response, session_id=None, step_index=None, step_type=None, intent=None, confidence=None, api_latency=None):
    """Log a conversation interaction for analytics"""
    conn = get_bot_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO conversation_logs 
            (bot_id, bot_name, user_message, bot_response, session_id, step_index, step_type, intent, confidence, api_latency)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (bot_id, bot_name, user_message, bot_response, session_id, step_index, step_type, intent, confidence, api_latency))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        conn.close()
        print(f"Error logging conversation: {e}")
        return False

def get_conversation_stats(bot_id=None, days=30):
    """Get conversation statistics"""
    conn = get_bot_db_connection()
    cursor = conn.cursor()
    try:
        from datetime import datetime, timedelta
        cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
        
        if bot_id:
            cursor.execute('''
                SELECT 
                    COUNT(*) as total_messages,
                    COUNT(DISTINCT session_id) as unique_sessions,
                    bot_name
                FROM conversation_logs
                WHERE bot_id = ? AND created_at >= ?
                GROUP BY bot_name
            ''', (bot_id, cutoff_date))
        else:
            cursor.execute('''
                SELECT 
                    COUNT(*) as total_messages,
                    COUNT(DISTINCT session_id) as unique_sessions,
                    bot_name
                FROM conversation_logs
                WHERE created_at >= ?
                GROUP BY bot_name
            ''', (cutoff_date,))
        
        rows = cursor.fetchall()
        conn.close()
        
        stats = []
        for row in rows:
            stats.append({
                'bot_name': row['bot_name'],
                'total_messages': row['total_messages'],
                'unique_sessions': row['unique_sessions']
            })
        return stats
    except Exception as e:
        conn.close()
        print(f"Error getting conversation stats: {e}")
        return []

def get_bot_analytics(bot_id, days=30):
    """Get detailed analytics for a specific bot"""
    conn = get_bot_db_connection()
    cursor = conn.cursor()
    try:
        from datetime import datetime, timedelta
        cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
        
        cursor.execute('''
            SELECT 
                DATE(created_at) as date,
                COUNT(*) as message_count,
                COUNT(DISTINCT session_id) as session_count
            FROM conversation_logs
            WHERE bot_id = ? AND created_at >= ?
            GROUP BY DATE(created_at)
            ORDER BY date DESC
        ''', (bot_id, cutoff_date))
        
        rows = cursor.fetchall()
        conn.close()
        
        analytics = []
        for row in rows:
            analytics.append({
                'date': row['date'],
                'message_count': row['message_count'],
                'session_count': row['session_count']
            })
        return analytics
    except Exception as e:
        conn.close()
        print(f"Error getting bot analytics: {e}")
        return []

def get_step_analytics(bot_id, days=30):
    """Get step-level analytics including drop-off rates"""
    conn = get_bot_db_connection()
    cursor = conn.cursor()
    try:
        from datetime import datetime, timedelta
        cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
        
        # Get step completion statistics
        cursor.execute('''
            SELECT 
                step_index,
                step_type,
                COUNT(*) as completion_count,
                COUNT(DISTINCT session_id) as unique_sessions,
                AVG(api_latency) as avg_latency
            FROM conversation_logs
            WHERE bot_id = ? AND created_at >= ? AND step_index IS NOT NULL
            GROUP BY step_index, step_type
            ORDER BY step_index
        ''', (bot_id, cutoff_date))
        
        rows = cursor.fetchall()
        
        # Get total sessions to calculate drop-off
        cursor.execute('''
            SELECT COUNT(DISTINCT session_id) as total_sessions
            FROM conversation_logs
            WHERE bot_id = ? AND created_at >= ?
        ''', (bot_id, cutoff_date))
        total_sessions_row = cursor.fetchone()
        total_sessions = total_sessions_row['total_sessions'] if total_sessions_row else 0
        
        conn.close()
        
        step_analytics = []
        for row in rows:
            drop_off_rate = 0
            if total_sessions > 0:
                drop_off_rate = ((total_sessions - row['unique_sessions']) / total_sessions) * 100
            
            step_analytics.append({
                'step_index': row['step_index'],
                'step_type': row['step_type'] or 'unknown',
                'completion_count': row['completion_count'],
                'unique_sessions': row['unique_sessions'],
                'drop_off_rate': round(drop_off_rate, 2),
                'avg_latency': round(row['avg_latency'] or 0, 3)
            })
        
        return step_analytics
    except Exception as e:
        conn.close()
        print(f"Error getting step analytics: {e}")
        return []

def export_analytics_csv(bot_id=None, days=30):
    """Export analytics data as CSV"""
    import csv
    import io
    from datetime import datetime, timedelta
    
    conn = get_bot_db_connection()
    cursor = conn.cursor()
    try:
        cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
        
        if bot_id:
            cursor.execute('''
                SELECT 
                    bot_name,
                    user_message,
                    bot_response,
                    session_id,
                    step_index,
                    step_type,
                    intent,
                    confidence,
                    api_latency,
                    created_at
                FROM conversation_logs
                WHERE bot_id = ? AND created_at >= ?
                ORDER BY created_at DESC
            ''', (bot_id, cutoff_date))
        else:
            cursor.execute('''
                SELECT 
                    bot_name,
                    user_message,
                    bot_response,
                    session_id,
                    step_index,
                    step_type,
                    intent,
                    confidence,
                    api_latency,
                    created_at
                FROM conversation_logs
                WHERE created_at >= ?
                ORDER BY created_at DESC
            ''', (cutoff_date,))
        
        rows = cursor.fetchall()
        conn.close()
        
        # Create CSV in memory
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow(['Bot Name', 'User Message', 'Bot Response', 'Session ID', 'Step Index', 'Step Type', 'Intent', 'Confidence', 'API Latency (s)', 'Created At'])
        
        # Write data
        for row in rows:
            writer.writerow([
                row['bot_name'],
                row['user_message'],
                row['bot_response'],
                row['session_id'] or '',
                row['step_index'] or '',
                row['step_type'] or '',
                row['intent'] or '',
                row['confidence'] or '',
                row['api_latency'] or '',
                row['created_at']
            ])
        
        return output.getvalue()
    except Exception as e:
        conn.close()
        print(f"Error exporting analytics: {e}")
        return None

# Initialize database when module is imported
if __name__ != '__main__':
    init_bot_database()


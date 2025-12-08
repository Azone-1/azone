"""
Authentication and Session Management Module
Comprehensive user authentication with security features
"""

import sqlite3
import secrets
import hashlib
import hmac
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask import session, request, abort, g
import json

# Database file path
AUTH_DB_FILE = 'bots.db'  # Using same database

# Security constants
MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_DURATION = timedelta(minutes=30)
SESSION_TIMEOUT = timedelta(hours=2)
REMEMBER_ME_DURATION = timedelta(days=30)
PASSWORD_RESET_TOKEN_EXPIRY = timedelta(hours=1)
CSRF_TOKEN_EXPIRY = timedelta(hours=1)

def get_auth_db_connection():
    """Create and return a database connection"""
    conn = sqlite3.connect(AUTH_DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_auth_database():
    """Initialize authentication database with enhanced schema"""
    conn = get_auth_db_connection()
    cursor = conn.cursor()
    
    # Enhanced users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'viewer',
            is_active INTEGER DEFAULT 1,
            is_locked INTEGER DEFAULT 0,
            locked_until TEXT,
            failed_login_attempts INTEGER DEFAULT 0,
            last_login TEXT,
            last_password_change TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # User sessions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            session_token TEXT UNIQUE NOT NULL,
            ip_address TEXT,
            user_agent TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            expires_at TEXT NOT NULL,
            is_active INTEGER DEFAULT 1,
            remember_me INTEGER DEFAULT 0,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')
    
    # Password reset tokens
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS password_reset_tokens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            token TEXT UNIQUE NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            expires_at TEXT NOT NULL,
            used INTEGER DEFAULT 0,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')
    
    # Login attempts log
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS login_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            ip_address TEXT,
            user_agent TEXT,
            success INTEGER DEFAULT 0,
            failure_reason TEXT,
            attempted_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(username) REFERENCES users(username)
        )
    ''')
    
    # CSRF tokens
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS csrf_tokens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            token TEXT UNIQUE NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            expires_at TEXT NOT NULL
        )
    ''')
    
    # Create indexes
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_sessions_user ON user_sessions(user_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_sessions_token ON user_sessions(session_token)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_reset_tokens_user ON password_reset_tokens(user_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_reset_tokens_token ON password_reset_tokens(token)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_login_attempts_username ON login_attempts(username)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_csrf_session ON csrf_tokens(session_id)')
    
    conn.commit()
    conn.close()
    
    # Migrate existing users table if needed
    migrate_users_table()

def migrate_users_table():
    """Migrate existing users table to new schema"""
    conn = get_auth_db_connection()
    cursor = conn.cursor()
    
    try:
        # Check existing columns
        cursor.execute("PRAGMA table_info(users)")
        columns = [row[1] for row in cursor.fetchall()]
        
        # Add new columns if they don't exist
        new_columns = {
            'is_active': 'INTEGER DEFAULT 1',
            'is_locked': 'INTEGER DEFAULT 0',
            'locked_until': 'TEXT',
            'failed_login_attempts': 'INTEGER DEFAULT 0',
            'last_login': 'TEXT',
            'last_password_change': 'TEXT',
            'updated_at': 'TEXT DEFAULT CURRENT_TIMESTAMP'
        }
        
        for col_name, col_def in new_columns.items():
            if col_name not in columns:
                try:
                    cursor.execute(f'ALTER TABLE users ADD COLUMN {col_name} {col_def}')
                    print(f"Added column {col_name} to users table")
                except sqlite3.OperationalError as e:
                    print(f"Column {col_name} might already exist: {e}")
        
        conn.commit()
    except Exception as e:
        print(f"Migration error: {e}")
        conn.rollback()
    finally:
        conn.close()

def generate_csrf_token():
    """Generate a secure CSRF token"""
    return secrets.token_urlsafe(32)

def generate_password_reset_token():
    """Generate a secure password reset token"""
    return secrets.token_urlsafe(32)

def generate_session_token():
    """Generate a secure session token"""
    return secrets.token_hex(32)

def hash_password(password):
    """Hash a password using bcrypt-like method"""
    return generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)

def verify_password(password_hash, password):
    """Verify a password against its hash"""
    return check_password_hash(password_hash, password)

def create_user(username, email, password, role='viewer'):
    """Create a new user account"""
    conn = get_auth_db_connection()
    cursor = conn.cursor()
    
    try:
        password_hash = hash_password(password)
        now = datetime.now().isoformat()
        
        cursor.execute('''
            INSERT INTO users (username, email, password_hash, role, is_active, created_at, updated_at)
            VALUES (?, ?, ?, ?, 1, ?, ?)
        ''', (username, email, password_hash, role, now, now))
        
        user_id = cursor.lastrowid
        conn.commit()
        return {'success': True, 'user_id': user_id}
    except sqlite3.IntegrityError as e:
        conn.rollback()
        if 'username' in str(e):
            return {'success': False, 'error': 'Username already exists'}
        elif 'email' in str(e):
            return {'success': False, 'error': 'Email already exists'}
        return {'success': False, 'error': 'User creation failed'}
    except Exception as e:
        conn.rollback()
        return {'success': False, 'error': str(e)}
    finally:
        conn.close()

def authenticate_user(username, password, ip_address=None, user_agent=None, remember_me=False):
    """Authenticate a user and create session"""
    conn = get_auth_db_connection()
    cursor = conn.cursor()
    
    try:
        # Get user
        cursor.execute('SELECT * FROM users WHERE username = ? OR email = ?', (username, username))
        user = cursor.fetchone()
        
        if not user:
            log_login_attempt(username, ip_address, user_agent, False, 'User not found')
            return {'success': False, 'error': 'Invalid username or password'}
        
        user_dict = dict(user)
        
        # Check if account is active
        if not user_dict.get('is_active', 1):
            log_login_attempt(username, ip_address, user_agent, False, 'Account inactive')
            return {'success': False, 'error': 'Account is inactive'}
        
        # Check if account is locked
        if user_dict.get('is_locked', 0):
            locked_until = user_dict.get('locked_until')
            if locked_until:
                locked_until_dt = datetime.fromisoformat(locked_until)
                if datetime.now() < locked_until_dt:
                    log_login_attempt(username, ip_address, user_agent, False, 'Account locked')
                    return {'success': False, 'error': f'Account is locked until {locked_until_dt.strftime("%Y-%m-%d %H:%M:%S")}'}
                else:
                    # Unlock account
                    cursor.execute('''
                        UPDATE users 
                        SET is_locked = 0, locked_until = NULL, failed_login_attempts = 0
                        WHERE id = ?
                    ''', (user_dict['id'],))
                    conn.commit()
        
        # Verify password
        if not verify_password(user_dict['password_hash'], password):
            # Increment failed attempts
            failed_attempts = user_dict.get('failed_login_attempts', 0) + 1
            cursor.execute('UPDATE users SET failed_login_attempts = ? WHERE id = ?', 
                          (failed_attempts, user_dict['id']))
            
            # Lock account if max attempts reached
            if failed_attempts >= MAX_LOGIN_ATTEMPTS:
                locked_until = (datetime.now() + LOCKOUT_DURATION).isoformat()
                cursor.execute('''
                    UPDATE users 
                    SET is_locked = 1, locked_until = ?, failed_login_attempts = ?
                    WHERE id = ?
                ''', (locked_until, failed_attempts, user_dict['id']))
                log_login_attempt(username, ip_address, user_agent, False, 'Account locked due to max attempts')
                conn.commit()
                return {'success': False, 'error': f'Too many failed attempts. Account locked for {LOCKOUT_DURATION.seconds // 60} minutes.'}
            
            conn.commit()
            log_login_attempt(username, ip_address, user_agent, False, 'Invalid password')
            return {'success': False, 'error': f'Invalid password. {MAX_LOGIN_ATTEMPTS - failed_attempts} attempts remaining.'}
        
        # Successful login - reset failed attempts
        now = datetime.now().isoformat()
        cursor.execute('''
            UPDATE users 
            SET failed_login_attempts = 0, last_login = ?, is_locked = 0, locked_until = NULL
            WHERE id = ?
        ''', (now, user_dict['id']))
        
        # Create session
        session_token = generate_session_token()
        if remember_me:
            expires_at = (datetime.now() + REMEMBER_ME_DURATION).isoformat()
        else:
            expires_at = (datetime.now() + SESSION_TIMEOUT).isoformat()
        
        cursor.execute('''
            INSERT INTO user_sessions (user_id, session_token, ip_address, user_agent, expires_at, remember_me)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_dict['id'], session_token, ip_address, user_agent, expires_at, 1 if remember_me else 0))
        
        conn.commit()
        log_login_attempt(username, ip_address, user_agent, True, None)
        
        return {
            'success': True,
            'user_id': user_dict['id'],
            'username': user_dict['username'],
            'email': user_dict['email'],
            'role': user_dict['role'],
            'session_token': session_token,
            'expires_at': expires_at
        }
    except Exception as e:
        conn.rollback()
        log_login_attempt(username, ip_address, user_agent, False, str(e))
        return {'success': False, 'error': 'Authentication failed'}
    finally:
        conn.close()

def get_user_by_id(user_id):
    """Get user by ID"""
    conn = get_auth_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        if user:
            return dict(user)
        return None
    finally:
        conn.close()

def get_user_by_username(username):
    """Get user by username"""
    conn = get_auth_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        if user:
            return dict(user)
        return None
    finally:
        conn.close()

def get_user_by_email(email):
    """Get user by email"""
    conn = get_auth_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        if user:
            return dict(user)
        return None
    finally:
        conn.close()

def validate_session(session_token):
    """Validate a session token"""
    conn = get_auth_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            SELECT s.*, u.* 
            FROM user_sessions s
            JOIN users u ON s.user_id = u.id
            WHERE s.session_token = ? AND s.is_active = 1 AND s.expires_at > ?
        ''', (session_token, datetime.now().isoformat()))
        
        result = cursor.fetchone()
        if result:
            return dict(result)
        return None
    finally:
        conn.close()

def invalidate_session(session_token):
    """Invalidate a session"""
    conn = get_auth_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('UPDATE user_sessions SET is_active = 0 WHERE session_token = ?', (session_token,))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        return False
    finally:
        conn.close()

def invalidate_user_sessions(user_id, keep_current_token=None):
    """Invalidate all sessions for a user (except current)"""
    conn = get_auth_db_connection()
    cursor = conn.cursor()
    
    try:
        if keep_current_token:
            cursor.execute('''
                UPDATE user_sessions 
                SET is_active = 0 
                WHERE user_id = ? AND session_token != ?
            ''', (user_id, keep_current_token))
        else:
            cursor.execute('UPDATE user_sessions SET is_active = 0 WHERE user_id = ?', (user_id,))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        return False
    finally:
        conn.close()

def create_password_reset_token(user_id):
    """Create a password reset token"""
    conn = get_auth_db_connection()
    cursor = conn.cursor()
    
    try:
        token = generate_password_reset_token()
        expires_at = (datetime.now() + PASSWORD_RESET_TOKEN_EXPIRY).isoformat()
        
        # Invalidate old tokens
        cursor.execute('UPDATE password_reset_tokens SET used = 1 WHERE user_id = ?', (user_id,))
        
        # Create new token
        cursor.execute('''
            INSERT INTO password_reset_tokens (user_id, token, expires_at)
            VALUES (?, ?, ?)
        ''', (user_id, token, expires_at))
        
        conn.commit()
        return token
    except Exception as e:
        conn.rollback()
        return None
    finally:
        conn.close()

def validate_password_reset_token(token):
    """Validate a password reset token"""
    conn = get_auth_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            SELECT prt.*, u.*
            FROM password_reset_tokens prt
            JOIN users u ON prt.user_id = u.id
            WHERE prt.token = ? AND prt.used = 0 AND prt.expires_at > ?
        ''', (token, datetime.now().isoformat()))
        
        result = cursor.fetchone()
        if result:
            return dict(result)
        return None
    finally:
        conn.close()

def use_password_reset_token(token):
    """Mark a password reset token as used"""
    conn = get_auth_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('UPDATE password_reset_tokens SET used = 1 WHERE token = ?', (token,))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        return False
    finally:
        conn.close()

def reset_password(user_id, new_password):
    """Reset a user's password"""
    conn = get_auth_db_connection()
    cursor = conn.cursor()
    
    try:
        password_hash = hash_password(new_password)
        now = datetime.now().isoformat()
        
        cursor.execute('''
            UPDATE users 
            SET password_hash = ?, last_password_change = ?, updated_at = ?
            WHERE id = ?
        ''', (password_hash, now, now, user_id))
        
        # Invalidate all sessions for security
        invalidate_user_sessions(user_id)
        
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        return False
    finally:
        conn.close()

def change_password(user_id, old_password, new_password):
    """Change a user's password (requires old password)"""
    conn = get_auth_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('SELECT password_hash FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        
        if not user or not verify_password(user['password_hash'], old_password):
            return {'success': False, 'error': 'Current password is incorrect'}
        
        return {'success': reset_password(user_id, new_password)}
    finally:
        conn.close()

def log_login_attempt(username, ip_address, user_agent, success, failure_reason=None):
    """Log a login attempt"""
    conn = get_auth_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO login_attempts (username, ip_address, user_agent, success, failure_reason)
            VALUES (?, ?, ?, ?, ?)
        ''', (username, ip_address, user_agent, 1 if success else 0, failure_reason))
        conn.commit()
    except Exception as e:
        conn.rollback()
    finally:
        conn.close()

def get_login_attempts(username=None, ip_address=None, limit=10):
    """Get recent login attempts"""
    conn = get_auth_db_connection()
    cursor = conn.cursor()
    
    try:
        if username:
            cursor.execute('''
                SELECT * FROM login_attempts 
                WHERE username = ? 
                ORDER BY attempted_at DESC 
                LIMIT ?
            ''', (username, limit))
        elif ip_address:
            cursor.execute('''
                SELECT * FROM login_attempts 
                WHERE ip_address = ? 
                ORDER BY attempted_at DESC 
                LIMIT ?
            ''', (ip_address, limit))
        else:
            cursor.execute('''
                SELECT * FROM login_attempts 
                ORDER BY attempted_at DESC 
                LIMIT ?
            ''', (limit,))
        
        return [dict(row) for row in cursor.fetchall()]
    finally:
        conn.close()

def cleanup_expired_sessions():
    """Clean up expired sessions"""
    conn = get_auth_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            UPDATE user_sessions 
            SET is_active = 0 
            WHERE expires_at < ?
        ''', (datetime.now().isoformat(),))
        
        cursor.execute('''
            DELETE FROM password_reset_tokens 
            WHERE expires_at < ? OR used = 1
        ''', (datetime.now().isoformat(),))
        
        cursor.execute('''
            DELETE FROM csrf_tokens 
            WHERE expires_at < ?
        ''', (datetime.now().isoformat(),))
        
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        return False
    finally:
        conn.close()

def create_csrf_token(session_id):
    """Create a CSRF token for a session"""
    conn = get_auth_db_connection()
    cursor = conn.cursor()
    
    try:
        token = generate_csrf_token()
        expires_at = (datetime.now() + CSRF_TOKEN_EXPIRY).isoformat()
        
        # Remove old tokens for this session
        cursor.execute('DELETE FROM csrf_tokens WHERE session_id = ?', (session_id,))
        
        # Create new token
        cursor.execute('''
            INSERT INTO csrf_tokens (session_id, token, expires_at)
            VALUES (?, ?, ?)
        ''', (session_id, token, expires_at))
        
        conn.commit()
        return token
    except Exception as e:
        conn.rollback()
        return None
    finally:
        conn.close()

def validate_csrf_token(session_id, token):
    """Validate a CSRF token"""
    conn = get_auth_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            SELECT * FROM csrf_tokens 
            WHERE session_id = ? AND token = ? AND expires_at > ?
        ''', (session_id, token, datetime.now().isoformat()))
        
        result = cursor.fetchone()
        return result is not None
    finally:
        conn.close()

# Initialize database on import
init_auth_database()


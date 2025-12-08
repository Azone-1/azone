# db_manager.py
# Database management for scheduled posts
import sqlite3
import os
from datetime import datetime

# Database file path
DB_FILE = 'web_scheduled_posts.db'

def get_db_connection():
    """Create and return a database connection"""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # This allows column access by name
    return conn

def init_database():
    """Initialize the database and create tables if they don't exist"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create scheduled_posts table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scheduled_posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            schedule_time TEXT NOT NULL,
            platforms TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"Database initialized: {DB_FILE}")

def insert_scheduled_post(content, schedule_time, platforms, status='pending'):
    """
    Insert a new scheduled post into the database
    
    Args:
        content (str): The post content
        schedule_time (str): Scheduled time (ISO format or datetime string)
        platforms (str): Comma-separated list of platforms (e.g., "Facebook,Twitter")
        status (str): Post status - 'pending', 'sent', or 'failed' (default: 'pending')
    
    Returns:
        int: The ID of the newly inserted post
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO scheduled_posts (content, schedule_time, platforms, status)
            VALUES (?, ?, ?, ?)
        ''', (content, schedule_time, platforms, status))
        
        post_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        print(f"Post inserted successfully with ID: {post_id}")
        return post_id
    except Exception as e:
        conn.close()
        print(f"Error inserting post: {e}")
        raise

def get_all_scheduled_posts():
    """
    Fetch ALL scheduled posts from the database (regardless of status)
    
    Returns:
        list: List of dictionaries containing post data
        Each dictionary contains: id, content, schedule_time, platforms, status, created_at
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            SELECT id, content, schedule_time, platforms, status, created_at
            FROM scheduled_posts
            ORDER BY schedule_time ASC
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        # Convert rows to list of dictionaries
        posts = []
        for row in rows:
            posts.append({
                'id': row['id'],
                'content': row['content'],
                'schedule_time': row['schedule_time'],
                'platforms': row['platforms'],
                'status': row['status'],
                'created_at': row['created_at']
            })
        
        print(f"Retrieved {len(posts)} posts from database")
        return posts
    except Exception as e:
        conn.close()
        print(f"Error fetching posts: {e}")
        return []

def get_posts_by_status(status):
    """
    Fetch posts filtered by status
    
    Args:
        status (str): 'pending', 'sent', or 'failed'
    
    Returns:
        list: List of dictionaries containing post data
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            SELECT id, content, schedule_time, platforms, status, created_at
            FROM scheduled_posts
            WHERE status = ?
            ORDER BY schedule_time ASC
        ''', (status,))
        
        rows = cursor.fetchall()
        conn.close()
        
        posts = []
        for row in rows:
            posts.append({
                'id': row['id'],
                'content': row['content'],
                'schedule_time': row['schedule_time'],
                'platforms': row['platforms'],
                'status': row['status'],
                'created_at': row['created_at']
            })
        
        return posts
    except Exception as e:
        conn.close()
        print(f"Error fetching posts by status: {e}")
        return []

def update_post_status(post_id, new_status):
    """
    Update the status of a scheduled post
    
    Args:
        post_id (int): The ID of the post to update
        new_status (str): New status - 'pending', 'sent', or 'failed'
    
    Returns:
        bool: True if update was successful, False otherwise
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            UPDATE scheduled_posts
            SET status = ?
            WHERE id = ?
        ''', (new_status, post_id))
        
        conn.commit()
        conn.close()
        
        return cursor.rowcount > 0
    except Exception as e:
        conn.close()
        print(f"Error updating post status: {e}")
        return False

# Initialize database when module is run directly
if __name__ == '__main__':
    init_database()
    print("Database setup complete!")


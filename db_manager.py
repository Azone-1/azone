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
    
    # Create leads table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            service TEXT NOT NULL,
            status TEXT DEFAULT 'New',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            created_by INTEGER
        )
    ''')
    
    # Create customers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            package TEXT DEFAULT '',
            status TEXT DEFAULT 'Active',
            join_date TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create projects table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            customer_id INTEGER,
            service TEXT NOT NULL,
            status TEXT DEFAULT 'todo',
            priority TEXT DEFAULT 'Medium',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(customer_id) REFERENCES customers(id)
        )
    ''')
    
    # Create indexes for better performance
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_leads_status ON leads(status)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_leads_service ON leads(service)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_customers_status ON customers(status)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_projects_status ON projects(status)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_projects_customer ON projects(customer_id)')
    
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

# ============================================
# Leads Functions
# ============================================

def get_leads(search='', service='', status='', page=1, per_page=50):
    """Get leads with filtering and pagination"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = 'SELECT * FROM leads WHERE 1=1'
    params = []
    
    if search:
        query += ' AND (name LIKE ? OR email LIKE ? OR phone LIKE ?)'
        search_term = f'%{search}%'
        params.extend([search_term, search_term, search_term])
    
    if service:
        query += ' AND service = ?'
        params.append(service)
    
    if status:
        query += ' AND status = ?'
        params.append(status)
    
    # Get total count
    count_query = query.replace('SELECT *', 'SELECT COUNT(*)')
    cursor.execute(count_query, params)
    total = cursor.fetchone()[0]
    
    # Add pagination
    query += ' ORDER BY created_at DESC LIMIT ? OFFSET ?'
    params.extend([per_page, (page - 1) * per_page])
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows], total

def create_lead(name, email, phone, service, status='New', created_by=None):
    """Create a new lead"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO leads (name, email, phone, service, status, created_by)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, email, phone, service, status, created_by))
        
        lead_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return lead_id
    except Exception as e:
        conn.close()
        raise

def update_lead(lead_id, **data):
    """Update a lead"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        updates = []
        params = []
        
        for key, value in data.items():
            if key in ['name', 'email', 'phone', 'service', 'status']:
                updates.append(f'{key} = ?')
                params.append(value)
        
        if not updates:
            conn.close()
            return False
        
        params.append(lead_id)
        query = f'UPDATE leads SET {", ".join(updates)} WHERE id = ?'
        cursor.execute(query, params)
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()
        return success
    except Exception as e:
        conn.close()
        raise

def delete_lead(lead_id):
    """Delete a lead"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('DELETE FROM leads WHERE id = ?', (lead_id,))
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()
        return success
    except Exception as e:
        conn.close()
        raise

# ============================================
# Customers Functions
# ============================================

def get_customers(search='', status='', package='', page=1, per_page=50):
    """Get customers with filtering and pagination"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = 'SELECT * FROM customers WHERE 1=1'
    params = []
    
    if search:
        query += ' AND (name LIKE ? OR email LIKE ? OR phone LIKE ?)'
        search_term = f'%{search}%'
        params.extend([search_term, search_term, search_term])
    
    if status:
        query += ' AND status = ?'
        params.append(status)
    
    if package:
        query += ' AND package = ?'
        params.append(package)
    
    # Get total count
    count_query = query.replace('SELECT *', 'SELECT COUNT(*)')
    cursor.execute(count_query, params)
    total = cursor.fetchone()[0]
    
    # Add pagination
    query += ' ORDER BY join_date DESC LIMIT ? OFFSET ?'
    params.extend([per_page, (page - 1) * per_page])
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows], total

def create_customer(name, email, phone, package='', status='Active'):
    """Create a new customer"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO customers (name, email, phone, package, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, email, phone, package, status))
        
        customer_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return customer_id
    except Exception as e:
        conn.close()
        raise

def update_customer(customer_id, **data):
    """Update a customer"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        updates = []
        params = []
        
        for key, value in data.items():
            if key in ['name', 'email', 'phone', 'package', 'status']:
                updates.append(f'{key} = ?')
                params.append(value)
        
        if not updates:
            conn.close()
            return False
        
        params.append(customer_id)
        query = f'UPDATE customers SET {", ".join(updates)} WHERE id = ?'
        cursor.execute(query, params)
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()
        return success
    except Exception as e:
        conn.close()
        raise

def delete_customer(customer_id):
    """Delete a customer"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('DELETE FROM customers WHERE id = ?', (customer_id,))
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()
        return success
    except Exception as e:
        conn.close()
        raise

# ============================================
# Projects Functions
# ============================================

def get_projects(search='', status='', service=''):
    """Get projects with filtering"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = 'SELECT * FROM projects WHERE 1=1'
    params = []
    
    if search:
        query += ' AND name LIKE ?'
        params.append(f'%{search}%')
    
    if status:
        query += ' AND status = ?'
        params.append(status)
    
    if service:
        query += ' AND service = ?'
        params.append(service)
    
    query += ' ORDER BY created_at DESC'
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]

def create_project(name, customer_id, service, status='todo', priority='Medium'):
    """Create a new project"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO projects (name, customer_id, service, status, priority)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, customer_id, service, status, priority))
        
        project_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return project_id
    except Exception as e:
        conn.close()
        raise

def update_project_status(project_id, status):
    """Update project status"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('UPDATE projects SET status = ? WHERE id = ?', (status, project_id))
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()
        return success
    except Exception as e:
        conn.close()
        raise

# ============================================
# Dashboard Functions
# ============================================

def get_dashboard_stats():
    """Get dashboard statistics"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # New leads (last 30 days)
        cursor.execute('''
            SELECT COUNT(*) FROM leads 
            WHERE created_at >= datetime('now', '-30 days')
        ''')
        new_leads = cursor.fetchone()[0]
        
        # Active projects
        cursor.execute('SELECT COUNT(*) FROM projects WHERE status != ?', ('completed',))
        active_projects = cursor.fetchone()[0]
        
        # Total customers
        cursor.execute('SELECT COUNT(*) FROM customers')
        total_customers = cursor.fetchone()[0]
        
        # Monthly revenue (placeholder - you can add payments table later)
        monthly_revenue = 0
        
        # Calculate trends (compare with previous period)
        # Leads trend (last 30 days vs previous 30 days)
        cursor.execute('''
            SELECT COUNT(*) FROM leads 
            WHERE created_at >= datetime('now', '-60 days')
            AND created_at < datetime('now', '-30 days')
        ''')
        prev_leads = cursor.fetchone()[0]
        leads_trend = ((new_leads - prev_leads) / prev_leads * 100) if prev_leads > 0 else 0
        
        # Projects trend
        cursor.execute('SELECT COUNT(*) FROM projects WHERE status != ? AND created_at >= datetime("now", "-30 days")', ('completed',))
        new_projects = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM projects WHERE status != ? AND created_at >= datetime("now", "-60 days") AND created_at < datetime("now", "-30 days")', ('completed',))
        prev_projects = cursor.fetchone()[0]
        projects_trend = ((new_projects - prev_projects) / prev_projects * 100) if prev_projects > 0 else 0
        
        # Customers trend
        cursor.execute('SELECT COUNT(*) FROM customers WHERE join_date >= datetime("now", "-30 days")')
        new_customers = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM customers WHERE join_date >= datetime("now", "-60 days") AND join_date < datetime("now", "-30 days")')
        prev_customers = cursor.fetchone()[0]
        customers_trend = ((new_customers - prev_customers) / prev_customers * 100) if prev_customers > 0 else 0
        
        revenue_trend = 0  # Placeholder for revenue trend
        
        conn.close()
        
        return {
            'new_leads': new_leads,
            'active_projects': active_projects,
            'total_customers': total_customers,
            'monthly_revenue': monthly_revenue,
            'leads_trend': leads_trend,
            'projects_trend': projects_trend,
            'customers_trend': customers_trend,
            'revenue_trend': revenue_trend
        }
    except Exception as e:
        conn.close()
        raise

def get_chart_data(period='30days'):
    """Get chart data for dashboard"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Calculate days based on period
        days_map = {
            '7days': 7,
            '30days': 30,
            '90days': 90,
            'year': 365
        }
        days = days_map.get(period, 30)
        
        # Get service popularity data
        cursor.execute('''
            SELECT service, COUNT(*) as count 
            FROM leads 
            WHERE created_at >= datetime('now', '-' || ? || ' days')
            GROUP BY service
            ORDER BY count DESC
        ''', (days,))
        
        rows = cursor.fetchall()
        labels = [row['service'] for row in rows]
        data = [row['count'] for row in rows]
        
        conn.close()
        
        return {
            'labels': labels,
            'datasets': [{
                'label': 'Service Popularity',
                'data': data
            }]
        }
    except Exception as e:
        conn.close()
        raise

# Initialize database when module is run directly
if __name__ == '__main__':
    init_database()
    print("Database setup complete!")


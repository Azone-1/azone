#!/usr/bin/env python
"""
Sample Data Creator for AZone CRM
Run this script to create sample leads, customers, and projects for testing
"""

import db_manager
from datetime import datetime, timedelta
import random

def create_sample_data():
    """Create sample data for testing"""
    print("Creating sample data...")
    
    # Initialize database
    db_manager.init_database()
    
    # Sample services
    services = [
        "Bot Reply Packages",
        "Auto Post Packages",
        "Content Packs",
        "Video Packs",
        "AI Tools & Automation",
        "Payment Integration"
    ]
    
    # Sample statuses
    lead_statuses = ["New", "Contacted", "Converted"]
    customer_statuses = ["Active", "Inactive"]
    project_statuses = ["todo", "in-progress", "in-review", "completed"]
    priorities = ["Low", "Medium", "High"]
    
    # Create sample leads (last 60 days)
    print("Creating sample leads...")
    for i in range(30):
        days_ago = random.randint(0, 60)
        created_at = (datetime.now() - timedelta(days=days_ago)).isoformat()
        
        db_manager.create_lead(
            name=f"Lead {i+1}",
            email=f"lead{i+1}@example.com",
            phone=f"09{random.randint(100000000, 999999999)}",
            service=random.choice(services),
            status=random.choice(lead_statuses),
            created_by=1
        )
    print("✓ Created 30 sample leads")
    
    # Create sample customers
    print("Creating sample customers...")
    for i in range(15):
        days_ago = random.randint(0, 90)
        join_date = (datetime.now() - timedelta(days=days_ago)).isoformat()
        
        db_manager.create_customer(
            name=f"Customer {i+1}",
            email=f"customer{i+1}@example.com",
            phone=f"09{random.randint(100000000, 999999999)}",
            package=random.choice(services),
            status=random.choice(customer_statuses)
        )
    print("✓ Created 15 sample customers")
    
    # Create sample projects
    print("Creating sample projects...")
    for i in range(20):
        db_manager.create_project(
            name=f"Project {i+1}",
            customer_id=random.randint(1, 15),
            service=random.choice(services),
            status=random.choice(project_statuses),
            priority=random.choice(priorities)
        )
    print("✓ Created 20 sample projects")
    
    print("\n✅ Sample data created successfully!")
    print("\nYou can now:")
    print("1. Start the server: python web_app.py")
    print("2. Login with: admin / admin123")
    print("3. View the dashboard at: http://localhost:5000/dashboard")

if __name__ == '__main__':
    create_sample_data()

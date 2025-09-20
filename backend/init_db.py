#!/usr/bin/env python3
"""
Database initialization script for MySQL
Run this script to create tables and seed initial data
"""

import os
import sys
from datetime import datetime

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import db, Order, InvitationLog, Package, AdminAccount

def init_database():
    """Initialize database with tables and seed data"""
    app = create_app('production')
    
    with app.app_context():
        print("Creating database tables...")
        
        # Create all tables
        db.create_all()
        
        # Add default packages if they don't exist
        packages_config = app.config['PACKAGES']
        for package_id, package_data in packages_config.items():
            existing_package = Package.query.get(package_id)
            if not existing_package:
                package = Package(
                    id=package_id,
                    name=package_data['name'],
                    price=package_data['price'],
                    duration=package_data['duration'],
                    description=package_data['description']
                )
                db.session.add(package)
                print(f"Added package: {package_data['name']}")
        
        # Add sample admin accounts (you should change these)
        sample_admins = [
            {
                'email': 'admin1@example.com',
                'password': 'change_this_password_1'
            },
            {
                'email': 'admin2@example.com', 
                'password': 'change_this_password_2'
            }
        ]
        
        for admin_data in sample_admins:
            existing_admin = AdminAccount.query.filter_by(email=admin_data['email']).first()
            if not existing_admin:
                admin = AdminAccount(
                    email=admin_data['email'],
                    password=admin_data['password'],
                    is_active=True
                )
                db.session.add(admin)
                print(f"Added admin account: {admin_data['email']}")
        
        db.session.commit()
        print("Database initialization completed successfully!")
        
        # Show summary
        package_count = Package.query.count()
        admin_count = AdminAccount.query.count()
        print(f"\nSummary:")
        print(f"- Packages: {package_count}")
        print(f"- Admin accounts: {admin_count}")
        print(f"\nIMPORTANT: Please update admin passwords in the database!")

if __name__ == '__main__':
    init_database()

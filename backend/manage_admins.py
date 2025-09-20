#!/usr/bin/env python3
"""
Admin account management script
Usage:
  python manage_admins.py list
  python manage_admins.py add admin@example.com password123
  python manage_admins.py disable admin@example.com
  python manage_admins.py enable admin@example.com
  python manage_admins.py reset-failures admin@example.com
"""

import os
import sys
from datetime import datetime

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import db, AdminAccount

def list_admins():
    """List all admin accounts"""
    admins = AdminAccount.query.order_by(AdminAccount.id).all()
    
    if not admins:
        print("No admin accounts found.")
        return
    
    print(f"{'ID':<4} {'Email':<30} {'Active':<8} {'Failures':<10} {'Last Used':<20}")
    print("-" * 80)
    
    for admin in admins:
        last_used = admin.last_used.strftime('%Y-%m-%d %H:%M') if admin.last_used else 'Never'
        print(f"{admin.id:<4} {admin.email:<30} {'Yes' if admin.is_active else 'No':<8} {admin.failed_attempts:<10} {last_used:<20}")

def add_admin(email, password):
    """Add new admin account"""
    existing = AdminAccount.query.filter_by(email=email).first()
    if existing:
        print(f"Admin with email {email} already exists.")
        return
    
    admin = AdminAccount(
        email=email,
        password=password,
        is_active=True
    )
    
    db.session.add(admin)
    db.session.commit()
    
    print(f"Admin account {email} added successfully.")

def disable_admin(email):
    """Disable admin account"""
    admin = AdminAccount.query.filter_by(email=email).first()
    if not admin:
        print(f"Admin with email {email} not found.")
        return
    
    admin.is_active = False
    db.session.commit()
    
    print(f"Admin account {email} disabled.")

def enable_admin(email):
    """Enable admin account"""
    admin = AdminAccount.query.filter_by(email=email).first()
    if not admin:
        print(f"Admin with email {email} not found.")
        return
    
    admin.is_active = True
    admin.failed_attempts = 0  # Reset failures when enabling
    db.session.commit()
    
    print(f"Admin account {email} enabled and failures reset.")

def reset_failures(email):
    """Reset failure count for admin"""
    admin = AdminAccount.query.filter_by(email=email).first()
    if not admin:
        print(f"Admin with email {email} not found.")
        return
    
    admin.failed_attempts = 0
    db.session.commit()
    
    print(f"Failure count reset for admin {email}.")

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    
    app = create_app('production')
    
    with app.app_context():
        command = sys.argv[1].lower()
        
        if command == 'list':
            list_admins()
        elif command == 'add':
            if len(sys.argv) != 4:
                print("Usage: python manage_admins.py add <email> <password>")
                return
            add_admin(sys.argv[2], sys.argv[3])
        elif command == 'disable':
            if len(sys.argv) != 3:
                print("Usage: python manage_admins.py disable <email>")
                return
            disable_admin(sys.argv[2])
        elif command == 'enable':
            if len(sys.argv) != 3:
                print("Usage: python manage_admins.py enable <email>")
                return
            enable_admin(sys.argv[2])
        elif command == 'reset-failures':
            if len(sys.argv) != 3:
                print("Usage: python manage_admins.py reset-failures <email>")
                return
            reset_failures(sys.argv[2])
        else:
            print(f"Unknown command: {command}")
            print(__doc__)

if __name__ == '__main__':
    main()

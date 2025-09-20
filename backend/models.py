from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

db = SQLAlchemy()

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    customer_email = db.Column(db.String(255), nullable=False, index=True)
    full_name = db.Column(db.String(255), nullable=True)
    phone_number = db.Column(db.String(20), nullable=True)
    package_id = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_status = db.Column(db.String(50), nullable=False, default='pending', index=True)
    invitation_status = db.Column(db.String(50), nullable=False, default='pending', index=True)
    checkout_url = db.Column(db.String(512), nullable=True)
    payment_method = db.Column(db.String(64), nullable=True)
    reference = db.Column(db.String(128), nullable=True, index=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    invitation_logs = db.relationship('InvitationLog', backref='order', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Order {self.order_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'customer_email': self.customer_email,
            'full_name': self.full_name,
            'phone_number': self.phone_number,
            'package_id': self.package_id,
            'amount': float(self.amount),
            'payment_status': self.payment_status,
            'invitation_status': self.invitation_status,
            'checkout_url': self.checkout_url,
            'payment_method': self.payment_method,
            'reference': self.reference,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class InvitationLog(db.Model):
    __tablename__ = 'invitation_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False, index=True)
    attempt_timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(50), nullable=False)  # 'success', 'failure', 'retry'
    error_message = db.Column(db.Text, nullable=True)
    screenshot_path = db.Column(db.String(255), nullable=True)
    retry_count = db.Column(db.Integer, nullable=False, default=0)
    
    def __repr__(self):
        return f'<InvitationLog {self.id} - Order {self.order_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'attempt_timestamp': self.attempt_timestamp.isoformat() if self.attempt_timestamp else None,
            'status': self.status,
            'error_message': self.error_message,
            'screenshot_path': self.screenshot_path,
            'retry_count': self.retry_count
        }

class Package(db.Model):
    __tablename__ = 'packages'
    
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    duration = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Package {self.id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': float(self.price),
            'duration': self.duration,
            'description': self.description,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class AdminAccount(db.Model):
    __tablename__ = 'admin_accounts'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True, index=True)
    password = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True, index=True)
    last_used = db.Column(db.DateTime, nullable=True, index=True)
    failed_attempts = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<AdminAccount {self.email}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'is_active': self.is_active,
            'last_used': self.last_used.isoformat() if self.last_used else None,
            'failed_attempts': self.failed_attempts,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

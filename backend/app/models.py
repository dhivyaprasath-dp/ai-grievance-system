from .extensions import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='citizen')  # citizen, officer, admin
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    petitions = db.relationship('Petition', backref='user', lazy=True, cascade='all, delete-orphan')
    notifications = db.relationship('Notification', backref='user', lazy=True, cascade='all, delete-orphan')


class Department(db.Model):
    __tablename__ = 'departments'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    email = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    petitions = db.relationship('Petition', backref='department', lazy=True)


class Petition(db.Model):
    __tablename__ = 'petitions'
    
    id = db.Column(db.Integer, primary_key=True)
    petition_id = db.Column(db.String(20), unique=True, nullable=False)  # e.g., PET-2025-0001
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Petition content
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    
    # AI-generated fields
    category = db.Column(db.String(50))  # Auto-classified category
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    priority = db.Column(db.String(20), default='medium')  # low, medium, high
    sentiment_score = db.Column(db.Float)  # -1 to 1
    urgency_level = db.Column(db.String(20))  # normal, urgent, critical
    
    # Status tracking
    status = db.Column(db.String(30), default='submitted')  # submitted, in_review, in_progress, resolved, rejected
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    resolved_at = db.Column(db.DateTime)
    
    # Additional fields
    attachment_path = db.Column(db.String(255))
    resolution_comment = db.Column(db.Text)
    
    # Relationships
    status_history = db.relationship('PetitionStatus', backref='petition', lazy=True, cascade='all, delete-orphan')
    notifications = db.relationship('Notification', backref='petition', lazy=True, cascade='all, delete-orphan')


class PetitionStatus(db.Model):
    __tablename__ = 'petition_status'
    
    id = db.Column(db.Integer, primary_key=True)
    petition_id = db.Column(db.Integer, db.ForeignKey('petitions.id'), nullable=False)
    status = db.Column(db.String(30), nullable=False)
    comment = db.Column(db.Text)
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to user who updated
    updater = db.relationship('User', foreign_keys=[updated_by])


class Notification(db.Model):
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    petition_id = db.Column(db.Integer, db.ForeignKey('petitions.id'))
    message = db.Column(db.Text, nullable=False)
    read_status = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import json

db = SQLAlchemy()

class User(db.Model):
    """User model for storing user login information"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationship with medical history
    medical_histories = db.relationship('MedicalHistory', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'age': self.age,
            'gender': self.gender,
            'created_at': self.created_at.isoformat(),
            'is_active': self.is_active
        }


class MedicalHistory(db.Model):
    """Medical History model for storing user health records"""
    __tablename__ = 'medical_histories'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Symptom-based diagnosis
    symptoms = db.Column(db.JSON)  # List of symptoms
    symptom_predictions = db.Column(db.JSON)  # Disease predictions from symptoms
    
    # Image-based diagnosis (Skin/X-Ray)
    image_path = db.Column(db.String(255))
    image_type = db.Column(db.String(50))  # 'skin' or 'xray'
    image_predictions = db.Column(db.JSON)  # Disease predictions from image
    
    # Risk assessment
    risk_factors = db.Column(db.JSON)  # Risk factors provided by user
    risk_assessment = db.Column(db.JSON)  # Risk assessment result
    
    # General health information
    blood_type = db.Column(db.String(10))
    allergies = db.Column(db.Text)
    medications = db.Column(db.Text)
    medical_conditions = db.Column(db.JSON)  # Chronic conditions, past surgeries, etc.
    
    # Vital signs
    blood_pressure = db.Column(db.String(20))  # e.g., "120/80"
    heart_rate = db.Column(db.Integer)
    temperature = db.Column(db.Float)
    weight = db.Column(db.Float)  # in kg
    height = db.Column(db.Float)  # in cm
    
    # Consultation notes
    consultation_notes = db.Column(db.Text)
    doctor_name = db.Column(db.String(100))
    
    # Record metadata
    record_type = db.Column(db.String(50))  # 'symptom_check', 'image_analysis', 'risk_assessment', 'general'
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert medical history to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'symptoms': self.symptoms,
            'symptom_predictions': self.symptom_predictions,
            'image_type': self.image_type,
            'image_predictions': self.image_predictions,
            'risk_assessment': self.risk_assessment,
            'blood_type': self.blood_type,
            'allergies': self.allergies,
            'medications': self.medications,
            'medical_conditions': self.medical_conditions,
            'blood_pressure': self.blood_pressure,
            'heart_rate': self.heart_rate,
            'temperature': self.temperature,
            'weight': self.weight,
            'height': self.height,
            'record_type': self.record_type,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class Session(db.Model):
    """Session model for tracking user login sessions"""
    __tablename__ = 'sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    token = db.Column(db.String(500), unique=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    ip_address = db.Column(db.String(50))
    user_agent = db.Column(db.String(255))
    
    def is_valid(self):
        """Check if session is still valid"""
        return self.is_active and datetime.utcnow() < self.expires_at

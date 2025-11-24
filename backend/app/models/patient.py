"""
Patient Model
"""
from datetime import datetime
from app import db
import uuid


class Patient(db.Model):
    """Patient model for healthcare management"""
    
    __tablename__ = 'patients'
    
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String, nullable=True) # Placeholder for Supabase Auth ID
    
    # Personal Information
    username = db.Column(db.String(100), unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)

    last_name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(20))
    blood_type = db.Column(db.String(5))
    
    # Contact Information
    email = db.Column(db.String(255), unique=True)
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    city = db.Column(db.String(100))
    country = db.Column(db.String(100))
    
    # Medical Information
    allergies = db.Column(db.JSON)
    chronic_conditions = db.Column(db.JSON)
    current_medications = db.Column(db.JSON)
    emergency_contact = db.Column(db.JSON)
    
    # Insurance Information
    insurance_provider = db.Column(db.String(255))
    insurance_policy_number = db.Column(db.String(100))
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    password_hash = db.Column(db.String(128), nullable=True)

    
    # Relationships (simplified for restoration)
    # appointments = db.relationship('Appointment', backref='patient', lazy='dynamic')
    # medical_records = db.relationship('MedicalRecord', backref='patient', lazy='dynamic')
    
    def __repr__(self):
        return f'<Patient {self.first_name} {self.last_name}>'
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'gender': self.gender,
            'blood_type': self.blood_type,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'city': self.city,
            'country': self.country,
            'allergies': self.allergies,
            'chronic_conditions': self.chronic_conditions,
            'current_medications': self.current_medications,
            'emergency_contact': self.emergency_contact,
            'insurance_provider': self.insurance_provider,
            'insurance_policy_number': self.insurance_policy_number,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_active': self.is_active
        }

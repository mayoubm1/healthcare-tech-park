"""
Healthcare Provider Model
"""
from datetime import datetime
from app import db
import uuid


class HealthcareProvider(db.Model):
    """Healthcare provider model"""
    
    __tablename__ = 'healthcare_providers'
    
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=True)
    
    # Personal Information
    username = db.Column(db.String(100), unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)

    last_name = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(50))  # Dr., Prof., etc.
    
    # Professional Information
    specialization = db.Column(db.String(255), nullable=False)
    license_number = db.Column(db.String(100), unique=True, nullable=False)
    years_of_experience = db.Column(db.Integer)
    qualifications = db.Column(db.JSON)
    certifications = db.Column(db.JSON)
    
    # Contact Information
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    office_address = db.Column(db.Text)
    
    # Availability
    working_hours = db.Column(db.JSON)  # {"monday": {"start": "09:00", "end": "17:00"}, ...}
    consultation_fee = db.Column(db.Numeric(10, 2))
    accepts_insurance = db.Column(db.Boolean, default=True)
    
    # Ratings & Reviews
    average_rating = db.Column(db.Numeric(3, 2), default=0.0)
    total_reviews = db.Column(db.Integer, default=0)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    password_hash = db.Column(db.String(128), nullable=True)

    
    # Relationships
    appointments = db.relationship('Appointment', backref='provider', lazy='dynamic')
    
    def __repr__(self):
        return f'<HealthcareProvider {self.title} {self.first_name} {self.last_name}>'
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'title': self.title,
            'specialization': self.specialization,
            'license_number': self.license_number,
            'years_of_experience': self.years_of_experience,
            'qualifications': self.qualifications,
            'certifications': self.certifications,
            'email': self.email,
            'phone': self.phone,
            'office_address': self.office_address,
            'working_hours': self.working_hours,
            'consultation_fee': float(self.consultation_fee) if self.consultation_fee else None,
            'accepts_insurance': self.accepts_insurance,
            'average_rating': float(self.average_rating) if self.average_rating else 0.0,
            'total_reviews': self.total_reviews,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_active': self.is_active,
            'is_verified': self.is_verified
        }


"""
Appointment Model
"""
from datetime import datetime
from app import db
import uuid


class Appointment(db.Model):
    """Appointment model for scheduling"""
    
    __tablename__ = 'appointments'
    
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = db.Column(db.String, db.ForeignKey('patients.id'), nullable=False)
    provider_id = db.Column(db.String, db.ForeignKey('healthcare_providers.id'), nullable=False)
    
    # Appointment Details
    appointment_date = db.Column(db.DateTime, nullable=False)
    duration_minutes = db.Column(db.Integer, default=30)
    appointment_type = db.Column(db.String(50))  # in-person, telemedicine, follow-up
    status = db.Column(db.String(20), default='scheduled')  # scheduled, confirmed, completed, cancelled, no-show
    
    # Consultation Details
    reason = db.Column(db.Text)
    notes = db.Column(db.Text)
    diagnosis = db.Column(db.Text)
    prescription = db.Column(db.JSON)
    
    # Telemedicine
    is_telemedicine = db.Column(db.Boolean, default=False)
    meeting_link = db.Column(db.String(500))
    meeting_id = db.Column(db.String(100))
    
    # Payment
    consultation_fee = db.Column(db.Numeric(10, 2))
    payment_status = db.Column(db.String(20), default='pending')  # pending, paid, refunded
    payment_method = db.Column(db.String(50))
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    cancelled_at = db.Column(db.DateTime)
    cancellation_reason = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Appointment {self.id} - {self.appointment_date}>'
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'provider_id': self.provider_id,
            'appointment_date': self.appointment_date.isoformat() if self.appointment_date else None,
            'duration_minutes': self.duration_minutes,
            'appointment_type': self.appointment_type,
            'status': self.status,
            'reason': self.reason,
            'notes': self.notes,
            'diagnosis': self.diagnosis,
            'prescription': self.prescription,
            'is_telemedicine': self.is_telemedicine,
            'meeting_link': self.meeting_link,
            'meeting_id': self.meeting_id,
            'consultation_fee': float(self.consultation_fee) if self.consultation_fee else None,
            'payment_status': self.payment_status,
            'payment_method': self.payment_method,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'cancelled_at': self.cancelled_at.isoformat() if self.cancelled_at else None,
            'cancellation_reason': self.cancellation_reason
        }


"""
Medical Record Model
"""
from datetime import datetime
from app import db
import uuid


class MedicalRecord(db.Model):
    """Medical record model for patient health records"""
    
    __tablename__ = 'medical_records'
    
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = db.Column(db.String, db.ForeignKey('patients.id'), nullable=False)
    provider_id = db.Column(db.String, db.ForeignKey('healthcare_providers.id'))
    appointment_id = db.Column(db.String, db.ForeignKey('appointments.id'))
    
    # Record Details
    record_type = db.Column(db.String(50), nullable=False)  # consultation, lab_result, imaging, prescription, vaccination
    record_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Medical Data
    chief_complaint = db.Column(db.Text)
    diagnosis = db.Column(db.Text)
    treatment_plan = db.Column(db.Text)
    medications = db.Column(db.JSON)
    lab_results = db.Column(db.JSON)
    vital_signs = db.Column(db.JSON)  # {"blood_pressure": "120/80", "temperature": "98.6", ...}
    
    # Documents
    attachments = db.Column(db.JSON)  # Array of file URLs
    notes = db.Column(db.Text)
    
    # Privacy & Access
    is_confidential = db.Column(db.Boolean, default=False)
    access_level = db.Column(db.String(20), default='standard')  # standard, restricted, confidential
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.String)  # User ID who created the record
    
    def __repr__(self):
        return f'<MedicalRecord {self.id} - {self.record_type}>'
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'provider_id': self.provider_id,
            'appointment_id': self.appointment_id,
            'record_type': self.record_type,
            'record_date': self.record_date.isoformat() if self.record_date else None,
            'chief_complaint': self.chief_complaint,
            'diagnosis': self.diagnosis,
            'treatment_plan': self.treatment_plan,
            'medications': self.medications,
            'lab_results': self.lab_results,
            'vital_signs': self.vital_signs,
            'attachments': self.attachments,
            'notes': self.notes,
            'is_confidential': self.is_confidential,
            'access_level': self.access_level,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'created_by': self.created_by
        }


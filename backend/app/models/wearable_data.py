from datetime import datetime
from app import db
import uuid

class WearableData(db.Model):
    __tablename__ = 'wearable_data'

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = db.Column(db.String, db.ForeignKey('patients.id'), nullable=False)
    
    # Wearable Device Information
    device_type = db.Column(db.String(100), nullable=False) # e.g., 'Fitbit', 'Apple Watch', 'Oura Ring'
    data_type = db.Column(db.String(100), nullable=False) # e.g., 'heart_rate', 'sleep_patterns', 'activity_levels'
    value = db.Column(db.JSON) # Stores the actual data, e.g., {'timestamp': '...', 'reading': '...'}
    recorded_at = db.Column(db.DateTime, nullable=False)
    
    # Metadata
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    patient = db.relationship('Patient', backref=db.backref('wearable_data', lazy=True))

    def __repr__(self):
        return f'<WearableData {self.id} for Patient {self.patient_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'device_type': self.device_type,
            'data_type': self.data_type,
            'value': self.value,
            'recorded_at': self.recorded_at.isoformat(),
            'uploaded_at': self.uploaded_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

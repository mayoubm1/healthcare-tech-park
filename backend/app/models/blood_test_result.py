from datetime import datetime
from app import db
import uuid

class BloodTestResult(db.Model):
    __tablename__ = 'blood_test_results'

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = db.Column(db.String, db.ForeignKey('patients.id'), nullable=False)
    
    # Test Information
    test_name = db.Column(db.String(255), nullable=False) # e.g., 'Comprehensive Metabolic Panel', 'Hormone Panel'
    test_date = db.Column(db.DateTime, default=datetime.utcnow)
    results = db.Column(db.JSON) # Stores key-value pairs of test parameters and their values
    interpretation = db.Column(db.Text) # Doctor's interpretation of the results
    
    # Metadata
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    patient = db.relationship('Patient', backref=db.backref('blood_test_results', lazy=True))

    def __repr__(self):
        return f'<BloodTestResult {self.test_name} for Patient {self.patient_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'test_name': self.test_name,
            'test_date': self.test_date.isoformat(),
            'results': self.results,
            'interpretation': self.interpretation,
            'uploaded_at': self.uploaded_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

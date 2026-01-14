from datetime import datetime
from app import db
import uuid

class MicrobiomeData(db.Model):
    __tablename__ = 'microbiome_data'

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = db.Column(db.String, db.ForeignKey('patients.id'), nullable=False)
    
    # Microbiome Information
    gut_microbiome_profile = db.Column(db.JSON) # Stores sequencing results and analysis
    digestive_health_insights = db.Column(db.JSON) # Recommendations for digestive health
    immune_function_insights = db.Column(db.JSON) # Impact on immune system
    brain_gut_axis_insights = db.Column(db.JSON) # Connection to brain function
    
    # Metadata
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    patient = db.relationship('Patient', backref=db.backref('microbiome_data', lazy=True))

    def __repr__(self):
        return f'<MicrobiomeData {self.id} for Patient {self.patient_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'gut_microbiome_profile': self.gut_microbiome_profile,
            'digestive_health_insights': self.digestive_health_insights,
            'immune_function_insights': self.immune_function_insights,
            'brain_gut_axis_insights': self.brain_gut_axis_insights,
            'uploaded_at': self.uploaded_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

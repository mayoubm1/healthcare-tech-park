from datetime import datetime
from app import db
import uuid

class GenomicData(db.Model):
    __tablename__ = 'genomic_data'

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = db.Column(db.String, db.ForeignKey('patients.id'), nullable=False)
    
    # Genomic Information
    genetic_profile = db.Column(db.JSON) # Stores raw or processed genetic data
    predispositions = db.Column(db.JSON) # e.g., {'disease_risk': {'diabetes': 'high'}, 'drug_response': {'warfarin': 'slow_metabolizer'}}
    nutrition_insights = db.Column(db.JSON) # Dietary recommendations based on genetics
    treatment_personalization = db.Column(db.JSON) # How genetics influence treatment choices
    
    # Metadata
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    patient = db.relationship('Patient', backref=db.backref('genomic_data', lazy=True))

    def __repr__(self):
        return f'<GenomicData {self.id} for Patient {self.patient_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'genetic_profile': self.genetic_profile,
            'predispositions': self.predispositions,
            'nutrition_insights': self.nutrition_insights,
            'treatment_personalization': self.treatment_personalization,
            'uploaded_at': self.uploaded_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

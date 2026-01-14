from datetime import datetime
from app import db
import uuid

class NutritionPlan(db.Model):
    __tablename__ = 'nutrition_plans'

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = db.Column(db.String, db.ForeignKey('patients.id'), nullable=False)
    
    # Nutrition Plan Details
    plan_name = db.Column(db.String(255), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    dietary_recommendations = db.Column(db.JSON) # e.g., {'meals': [...], 'restrictions': [...], 'supplements': [...]} 
    meal_plan = db.Column(db.Text) # Detailed meal plan description
    notes = db.Column(db.Text)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    patient = db.relationship('Patient', backref=db.backref('nutrition_plans', lazy=True))

    def __repr__(self):
        return f'<NutritionPlan {self.plan_name} for Patient {self.patient_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'plan_name': self.plan_name,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'dietary_recommendations': self.dietary_recommendations,
            'meal_plan': self.meal_plan,
            'notes': self.notes,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

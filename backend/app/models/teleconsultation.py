"""
Teleconsultation Model
"""
from datetime import datetime
from app import db
import uuid


class Teleconsultation(db.Model):
    """Teleconsultation model for telemedicine services"""
    
    __tablename__ = 'teleconsultations'
    
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    appointment_id = db.Column(db.String, db.ForeignKey('appointments.id'), nullable=False)
    patient_id = db.Column(db.String, db.ForeignKey('patients.id'), nullable=False)
    provider_id = db.Column(db.String, db.ForeignKey('healthcare_providers.id'), nullable=False)
    
    # Session Details
    session_start = db.Column(db.DateTime)
    session_end = db.Column(db.DateTime)
    duration_minutes = db.Column(db.Integer)
    status = db.Column(db.String(20), default='scheduled')  # scheduled, in_progress, completed, cancelled
    
    # Platform Details
    platform = db.Column(db.String(50), default='internal')  # internal, zoom, teams, etc.
    meeting_link = db.Column(db.String(500))
    meeting_id = db.Column(db.String(100))
    meeting_password = db.Column(db.String(100))
    
    # Technical Details
    connection_quality = db.Column(db.String(20))  # excellent, good, fair, poor
    technical_issues = db.Column(db.JSON)
    
    # Session Data
    session_notes = db.Column(db.Text)
    recording_url = db.Column(db.String(500))
    transcript = db.Column(db.Text)
    
    # Chat Messages
    chat_history = db.Column(db.JSON)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Teleconsultation {self.id} - {self.status}>'
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'appointment_id': self.appointment_id,
            'patient_id': self.patient_id,
            'provider_id': self.provider_id,
            'session_start': self.session_start.isoformat() if self.session_start else None,
            'session_end': self.session_end.isoformat() if self.session_end else None,
            'duration_minutes': self.duration_minutes,
            'status': self.status,
            'platform': self.platform,
            'meeting_link': self.meeting_link,
            'meeting_id': self.meeting_id,
            'connection_quality': self.connection_quality,
            'technical_issues': self.technical_issues,
            'session_notes': self.session_notes,
            'recording_url': self.recording_url,
            'chat_history': self.chat_history,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


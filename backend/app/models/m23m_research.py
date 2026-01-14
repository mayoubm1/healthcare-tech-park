from .. import db

class M23MResearch(db.Model):
    __tablename__ = 'm23m_research'

    id = db.Column(db.Integer, primary_key=True)
    research_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    research_data = db.Column(db.Text, nullable=True)
    collaboration_status = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f'<M23MResearch {self.research_name}>'


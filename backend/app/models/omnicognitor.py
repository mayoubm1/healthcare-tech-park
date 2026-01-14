from .. import db

class OmniCognitor(db.Model):
    __tablename__ = 'omnicognitor'

    id = db.Column(db.Integer, primary_key=True)
    agent_name = db.Column(db.String(100), nullable=False)
    capabilities = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<OmniCognitor {self.agent_name}>'


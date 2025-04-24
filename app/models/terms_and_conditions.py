from app import db
from datetime import datetime, timezone

class TermsAndConditions(db.Model):
    __tablename__ = 'terms_and_conditions'

    id = db.Column(db.Integer, primary_key=True)
    version = db.Column(db.String(10), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<TermsAndConditions {self.version}>'

    def serialize(self):
        return {
            'id': self.id,
            'version': self.version,
            'created_at': self.created_at.isoformat(),
            'content': self.content
        }
from .. import db
from datetime import datetime

class Parameter(db.Model):
    __tablename__ = 'parameters'

    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer,nullable=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def serialize(self):
        return {
            'id': self.id,
            'parent_id': self.parent_id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat()
        }
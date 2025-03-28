from .. import db
from datetime import datetime

class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.Integer,nullable=False)
    user = db.Column(db.String(150), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def serialize(self):
        return {
            'id': self.id,
            'type_id': self.parent_id,
            'user': self.name,
            'title':self.title,
            'description':self.description,
            'created_at': self.created_at.isoformat()
        }
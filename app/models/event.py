from .. import db
from datetime import datetime, timezone

class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.Integer, db.ForeignKey('parameters.id'), nullable=True)
    user = db.Column(db.String(150), db.ForeignKey('users.user'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    start_date = db.Column(db.DateTime, nullable=False)
    
    user_rel = db.relationship('User', back_populates='events')
    type = db.relationship('Parameter')
    
    def serialize(self):
        return {
            'id': self.id,
            'type_id': self.type_id,
            'type_name': self.type.name if self.type else None,
            'user': self.user,
            'title':self.title,
            'description':self.description,
            'created_at': self.created_at.isoformat(),
            'start_date': self.start_date.isoformat()
        }
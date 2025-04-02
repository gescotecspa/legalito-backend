from .. import db
from datetime import datetime

class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    folio_id = db.Column(db.Integer, db.ForeignKey('folios.id'), nullable=True)
    rit = db.Column(db.String(100), nullable=True)
    subject = db.Column(db.String(255), nullable=False)
    sender = db.Column(db.String(255), nullable=False)
    received_date = db.Column(db.DateTime, nullable=False)
    body = db.Column(db.Text, nullable=True)
    processed_at = db.Column(db.DateTime, default=datetime.utcnow)
    marked_as_invitation = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(50), default='pending')
    user = db.Column(db.String(150), nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'folio_id': self.folio_id,
            'rit': self.rit,
            'subject': self.subject,
            'sender': self.sender,
            'received_date': self.received_date.isoformat(),
            'body': self.body,
            'processed_at': self.processed_at.isoformat(),
            'marked_as_invitation': self.marked_as_invitation,
            'status': self.status,
            'user':self.user
        }

from .. import db
from datetime import datetime

class Folio(db.Model):
    __tablename__ = 'folios'

    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'), nullable=False)
    folio_number = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    notifications = db.relationship('Notification', backref='folio', lazy=True)

    def serialize(self):
        return {
            'id': self.id,
            'case_id': self.case_id,
            'folio_number': self.folio_number,
            'description': self.description,
            'created_at': self.created_at.isoformat()
        }
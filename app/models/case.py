from .. import db
from datetime import datetime

class Case(db.Model):
    __tablename__ = 'cases'

    id = db.Column(db.Integer, primary_key=True)
    rit = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='active')
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    folios = db.relationship('Folio', backref='case', lazy=True)
    client = db.relationship('Client', back_populates='cases')

    def serialize(self, include_client=True):
        data = {
            'id': self.id,
            'rit': self.rit,
            'name': self.name,
            'status': self.status,
            'client_id': self.client_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

        if include_client:
            data['client'] = self.client.serialize(include_cases=False) if self.client else None

        return data

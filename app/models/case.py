from .. import db
from datetime import datetime

class Case(db.Model):
    __tablename__ = 'cases'

    id = db.Column(db.Integer, primary_key=True)
    rit = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    folios = db.relationship('Folio', backref='case', lazy=True)

    def serialize(self):
        return {
            'id': self.id,
            'rit': self.rit,
            'name': self.name,
            'status': self.status,
            'created_at': self.created_at.isoformat()
        }
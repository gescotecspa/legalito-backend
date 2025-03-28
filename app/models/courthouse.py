from .. import db
from datetime import datetime

class Courthouse(db.Model):
    __tablename__ = 'courthouses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    type_id = db.Column(db.Integer)
    address = db.Column(db.String(250), nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(150), nullable=False)
    website = db.Column(db.String(150), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'type_id': self.type_id,
            'address': self.address,
            'phone_number': self.phone_number,
            'email': self.email,
            'website': self.website,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
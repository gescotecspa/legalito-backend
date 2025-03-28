from .. import db
from datetime import datetime

class Assistant(db.Model):
    __tablename__ = 'assistants'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)
    type_id = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    image_url = db.Column(db.String(250), nullable=True)
    region_id = db.Column(db.Integer, nullable=True)

    def serialize(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone_number': self.phone_number,
            'type_id': self.type_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'image_url': self.image_url,
            'region_id': self.region_id,
        }
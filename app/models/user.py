from .. import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'

    user = db.Column(db.String(150), primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    password_hash = db.Column(db.String(250), nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)
    birth_date = db.Column(db.DateTime, default=datetime.utcnow)
    image_url = db.Column(db.String(200), nullable=True)
    status = db.Column(db.String(20), nullable=True)
    activation_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, default=datetime.utcnow)
    suspended_at = db.Column(db.DateTime, default=datetime.utcnow)
    suspension_reason = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def serialize(self):
        return {
            'user': self.user,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'password_hash': self.password_hash,
            'phone_number': self.phone_number,
            'birth_date': self.birth_date.isoformat(),
            'image_url': self.image_url,
            'status': self.status,
            'activation_date': self.activation_date.isoformat(),
            'last_login': self.last_login.isoformat(),
            'suspended_at': self.suspended_at.isoformat(),
            'suspension_reason': self.suspension_reason,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
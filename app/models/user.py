from .. import db
from datetime import datetime, timedelta

class User(db.Model):
    __tablename__ = 'users'

    user = db.Column(db.String(150), primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)
    birth_date = db.Column(db.DateTime, nullable=True)
    image_url = db.Column(db.String(200), nullable=True)
    status = db.Column(db.String(20), nullable=True)
    activation_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    suspended_at = db.Column(db.DateTime, nullable=True)
    suspension_reason = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    reset_code = db.Column(db.String(6), nullable=True)  
    reset_code_expiration = db.Column(db.DateTime, nullable=True)
    
    email_accounts = db.relationship('EmailAccount', back_populates='user_rel', cascade='all, delete-orphan')
    events = db.relationship('Event', back_populates='user_rel', cascade='all, delete-orphan')
    
    def set_reset_code(self, code):
        """Guarda el código de recuperación con una expiración de 10 minutos."""
        self.reset_code = code
        self.reset_code_expiration = datetime.utcnow() + timedelta(minutes=15)
        db.session.commit()
        
    def serialize(self):
        return {
            'user': self.user,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'password_hash': self.password_hash,
            'phone_number': self.phone_number,
            'birth_date': self.birth_date.isoformat() if self.birth_date else None,
            'image_url': self.image_url,
            'status': self.status,
            'activation_date': self.activation_date.isoformat(),
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'suspended_at': self.suspended_at.isoformat() if self.suspended_at else None,
            'suspension_reason': self.suspension_reason,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'reset_code': self.reset_code,
            'reset_code_expiration': self.reset_code_expiration.isoformat() if self.reset_code_expiration else None
        }
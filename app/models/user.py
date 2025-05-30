from .. import db
from datetime import datetime, timedelta, timezone
import enum

class IdentificationType(enum.Enum):
    RUT = "RUT"
    RUN = "RUN"
    DNI = "DNI"
    LC  = "LC"
    
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
    activation_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    suspended_at = db.Column(db.DateTime, nullable=True)
    suspension_reason = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    reset_code = db.Column(db.String(6), nullable=True)  
    reset_code_expiration = db.Column(db.DateTime, nullable=True)
    status_id = db.Column(db.Integer, db.ForeignKey('statuses.id'), nullable=True)
    deleted_at = db.Column(db.DateTime, nullable=True)
    
    # ← Nuevo campo para RUT / DNI / RUN / LC
    identification = db.Column(db.String(50), unique=True, nullable=True)
    identification_type = db.Column(
        db.Enum(IdentificationType, name="identification_type_enum"),
        nullable=True
    )
    terms_and_conditions_id = db.Column(db.Integer, db.ForeignKey('terms_and_conditions.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    
    status = db.relationship('Status')
    email_accounts = db.relationship('EmailAccount', back_populates='user_rel', cascade='all, delete-orphan')
    events = db.relationship('Event', back_populates='user_rel', cascade='all, delete-orphan')
    
    # Cambiado aquí para usar lazy='joined'
    terms_and_conditions = db.relationship('TermsAndConditions', lazy='joined')

    def set_reset_code(self, code):
        """Guarda el código de recuperación con una expiración de 10 minutos."""
        self.reset_code = code
        self.reset_code_expiration = datetime.utcnow() + timedelta(minutes=15)
        db.session.commit()
        
    def serialize(self):
        terms_info = {
            'terms_id': self.terms_and_conditions.id if self.terms_and_conditions else None,
            'terms_version': self.terms_and_conditions.version if self.terms_and_conditions else None
        }
        return {
            'user': self.user,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'password_hash': self.password_hash,
            'phone_number': self.phone_number,
            'birth_date': self.birth_date.isoformat() if self.birth_date else None,
            'image_url': self.image_url,
            'activation_date': self.activation_date.isoformat(),
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'status': self.status.serialize() if self.status else None,
            'suspended_at': self.suspended_at.isoformat() if self.suspended_at else None,
            'suspension_reason': self.suspension_reason,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'deleted_at': self.deleted_at.isoformat() if self.deleted_at else None,
            'reset_code': self.reset_code,
            'reset_code_expiration': self.reset_code_expiration.isoformat() if self.reset_code_expiration else None,
            'identification': self.identification,
            'identification_type': self.identification_type.value if self.identification_type else None,
            'terms_and_conditions': terms_info
        }

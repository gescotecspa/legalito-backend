from .. import db

class EmailAccount(db.Model):
    __tablename__ = 'email_accounts'

    id = db.Column(db.Integer, primary_key=True)
    provider = db.Column(db.String(50), nullable=False)  # Ejemplo: Gmail, Outlook, Yahoo
    imap_server = db.Column(db.String(100), nullable=False)
    email_address = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)  # Guardar token o contraseña cifrada
    active = db.Column(db.Boolean, default=True)
    user = db.Column(db.String(150), db.ForeignKey('users.user'), nullable=False)
    user_rel = db.relationship('User', back_populates='email_accounts')
    

    def serialize(self):
        return {
            'id': self.id,
            'provider': self.provider,
            'imap_server': self.imap_server,
            'email_address': self.email_address,
            'password': self.password,
            'active': self.active,
            'user':self.user
        }
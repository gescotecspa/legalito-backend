from datetime import datetime

from .. import db


class Client(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    owner_user = db.Column(db.String(150), db.ForeignKey('users.user'), nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False)
    identification = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(150), nullable=True)
    phone_number = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), nullable=False, default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    cases = db.relationship('Case', back_populates='client')

    def serialize(self, include_cases=False):
        data = {
            'id': self.id,
            'owner_user': self.owner_user,
            'name': self.name,
            'identification': self.identification,
            'email': self.email,
            'phone_number': self.phone_number,
            'address': self.address,
            'notes': self.notes,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

        if include_cases:
            data['cases'] = [case.serialize(include_client=False) for case in self.cases]

        return data

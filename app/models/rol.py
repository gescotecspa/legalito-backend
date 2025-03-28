from .. import db

class Rol(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(100), nullable=True)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }
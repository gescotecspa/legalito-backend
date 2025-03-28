from .. import db
from datetime import datetime

class Favorite(db.Model):
    __tablename__ = 'favorites'

    assistant_id = db.Column(db.Integer, primary_key=True, nullable=False)
    user = db.Column(db.String(150), primary_key=True, nullable=False)
   

    def serialize(self):
        return {
            'assistant_id': self.assistant_id,
            'user': self.user,
        }
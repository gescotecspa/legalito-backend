from .. import db
from datetime import datetime

class CaseUser(db.Model):
    __tablename__ = 'cases_users'

    case_id = db.Column(db.Integer, primary_key=True, nullable=False)
    user = db.Column(db.String(150), primary_key=True, nullable=False)
   

    def serialize(self):
        return {
            'case_id': self.case_id,
            'user': self.user,
        }
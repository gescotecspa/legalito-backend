from datetime import datetime

from .. import db


class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    owner_user = db.Column(db.String(150), db.ForeignKey('users.user'), nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), nullable=False, default='pending')
    priority = db.Column(db.String(50), nullable=False, default='normal')
    due_date = db.Column(db.DateTime, nullable=True)
    assignee_user = db.Column(db.String(150), nullable=True)
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'), nullable=True, index=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=True, index=True)
    completed_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    case = db.relationship('Case')
    client = db.relationship('Client')

    def serialize(self, include_relations=True):
        data = {
            'id': self.id,
            'owner_user': self.owner_user,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'priority': self.priority,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'assignee_user': self.assignee_user,
            'case_id': self.case_id,
            'client_id': self.client_id,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

        if include_relations:
            data['case'] = self.case.serialize(include_client=True) if self.case else None
            data['client'] = self.client.serialize(include_cases=False) if self.client else None

        return data

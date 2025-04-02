from app import db
from app.models import Notification
from datetime import datetime

class NotificationNotFoundException(Exception):
    pass

def create_notification(data):
    required_fields = ['subject', 'sender', 'received_date']
    for field in required_fields:
        if not data.get(field):
            raise ValueError(f"'{field}' is a required field.")

    print(data)
    print(type(data.get('received_date')))
    print(type(data.get('marked_as_invitation')))

    notification = Notification(
        folio_id=data.get('folio_id'),
        rit=data.get('rit'),
        subject=data['subject'],
        sender=data['sender'],
        received_date=datetime.fromisoformat(data['received_date']),
        body=data.get('body'),
        processed_at=datetime.utcnow(),
        marked_as_invitation=data.get('marked_as_invitation', False),
        status=data.get('status', 'pending'),
        user=data.get('user')
    )
    print(notification)
    try:
        db.session.add(notification)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)
        return False
    return notification
    

def list_notifications():
    return Notification.query.all()

def delete_notification(notification_id):
    notification = Notification.query.get(notification_id)
    if not notification:
        raise NotificationNotFoundException(f"Notification with id {notification_id} not found.")

    db.session.delete(notification)
    db.session.commit()

def list_notifications_by_user(user):
    return Notification.query.filter_by(uer = user).order_by(Notification.received_date.asc()).all()
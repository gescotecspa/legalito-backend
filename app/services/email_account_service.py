from app import db
from app.models import EmailAccount

def add_email_account(data):
    
    account = EmailAccount(
        provider=data['provider'],
        imap_server=data['imap_server'],
        email_address=data['email_address'],
        password=data['password'],
        active=True,
        user = data['user']
    )
    db.session.add(account)
    db.session.commit()
    return account

def list_email_accounts():
    accounts = EmailAccount.query.all()
    return accounts

def get_email_account(user):
    account = EmailAccount.query.filter_by(user=user).first()
    return account

def delete_email_accounts(email,user):

    EmailAccount.query.filter_by(email_address=email, user=user).delete()

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return False

    return True
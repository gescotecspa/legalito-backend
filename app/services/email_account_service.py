from app import db
from app.models import EmailAccount, User
from flask import current_app


class EmailAccountOwnershipException(Exception):
    pass


def add_email_account(data):
    user_email = data['user']

    # Validar que el usuario exista
    user = User.query.get(user_email)
    if not user:
        raise ValueError(f"El usuario '{user_email}' no existe.")

    # Validar que no exista ya una cuenta con ese email_address ya que debe ser unica segun la tabla de postgres
    existing_account = EmailAccount.query.filter_by(email_address=data['email_address']).first()
    if existing_account:
        raise ValueError(f"Ya existe una cuenta utilizando el correo '{data['email_address']}'.")

    account = EmailAccount(
        provider=data['provider'],
        imap_server=data['imap_server'],
        email_address=data['email_address'],
        password=data['password'],
        active=True,
        user=user_email
    )
    db.session.add(account)
    db.session.commit()
    return account

def list_email_accounts():
    accounts = EmailAccount.query.all()
    return accounts

def get_email_accounts_by_user(user):
    accounts = EmailAccount.query.filter_by(user=user).all()
    return accounts

def get_user_active_email(user,email):
    account = EmailAccount.query.filter_by(email_address=email, user=user).first()
    return account

def delete_email_accounts(email, user):
    try:
        account = EmailAccount.query.filter_by(email_address=email, user=user).first()
        if not account:
            return False  # No se encontró la cuenta

        db.session.delete(account)
        db.session.commit()
        return True

    except Exception as e:
        db.session.rollback()
        current_app.logger.exception("Error deleting email account")
        return False
    
def toggle_email_account_status(email, user):
    try:
        account = EmailAccount.query.filter_by(email_address=email, user=user).first()
        if not account:
            return False

        account.active = not account.active 
        db.session.commit()
        return account.active

    except Exception as e:
        db.session.rollback()
        current_app.logger.exception("Error toggling email account status")
        return None
    
def get_email_account_by_id(account_id):
    return db.session.get(EmailAccount, account_id)


def get_email_account_by_id_for_user(account_id, user):
    account = db.session.get(EmailAccount, account_id)
    if not account:
        return None
    if account.user != user:
        raise EmailAccountOwnershipException(
            "Account not found or does not belong to this user"
        )
    return account

def update_email_account(account_id, user, data):
    account = db.session.get(EmailAccount, account_id)
    if not account:
        return None
    if account.user != user:
        raise EmailAccountOwnershipException(
            "Account not found or does not belong to this user"
        )

    new_email_address = data.get('email_address', account.email_address)
    if new_email_address != account.email_address:
        existing_account = EmailAccount.query.filter_by(email_address=new_email_address).first()
        if existing_account:
            raise ValueError(f"Ya existe una cuenta utilizando el correo '{new_email_address}'.")

    account.provider = data.get('provider', account.provider)
    account.imap_server = data.get('imap_server', account.imap_server)
    account.email_address = new_email_address
    account.password = data.get('password', account.password)

    db.session.commit()
    return account

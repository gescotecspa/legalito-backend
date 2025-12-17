from app import db
from app.models import EmailAccount, User

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
        print(f"Error eliminando la cuenta: {e}")
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
        print(f"Error cambiando el estado de la cuenta: {e}")
        return None
    
def get_email_account_by_id(account_id):
    return EmailAccount.query.get(account_id)

def update_email_account(account_id, data):
    account = EmailAccount.query.get(account_id)
    if not account:
        return None

    account.provider = data.get('provider', account.provider)
    account.imap_server = data.get('imap_server', account.imap_server)
    account.email_address = data.get('email_address', account.email_address)
    account.password = data.get('password', account.password)

    db.session.commit()
    return account
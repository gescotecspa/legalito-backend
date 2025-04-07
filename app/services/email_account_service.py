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

def get_email_account(user):
    account = EmailAccount.query.filter_by(user=user).first()
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
from datetime import datetime

from app import db
from app.models import Client


class ClientNotFoundException(Exception):
    pass


class ClientOwnershipException(Exception):
    pass


def _normalize_optional(value):
    if value is None:
        return None
    value = str(value).strip()
    return value or None


def create_client(user, data):
    if not user:
        raise ValueError("User parameter is required.")

    name = _normalize_optional(data.get('name'))
    if not name:
        raise ValueError("'name' is required.")

    client = Client(
        owner_user=user,
        name=name,
        identification=_normalize_optional(data.get('identification')),
        email=_normalize_optional(data.get('email')),
        phone_number=_normalize_optional(data.get('phone_number')),
        address=_normalize_optional(data.get('address')),
        notes=_normalize_optional(data.get('notes')),
        status=_normalize_optional(data.get('status')) or 'active',
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    db.session.add(client)
    db.session.commit()
    return client


def list_clients_by_user(user):
    if not user:
        raise ValueError("User parameter is required.")

    return (
        Client.query
        .filter_by(owner_user=user)
        .order_by(Client.name.asc())
        .all()
    )


def get_client_for_user(client_id, user):
    if not user:
        raise ValueError("User parameter is required.")

    client = db.session.get(Client, client_id)
    if not client:
        raise ClientNotFoundException(f"Client with id {client_id} not found.")
    if client.owner_user != user:
        raise ClientOwnershipException("Client not found or does not belong to this user.")

    return client


def update_client(client_id, user, data):
    client = get_client_for_user(client_id, user)

    if 'name' in data:
        name = _normalize_optional(data.get('name'))
        if not name:
            raise ValueError("'name' is required.")
        client.name = name

    for field in ('identification', 'email', 'phone_number', 'address', 'notes', 'status'):
        if field in data:
            setattr(client, field, _normalize_optional(data.get(field)))

    client.updated_at = datetime.utcnow()
    db.session.commit()
    return client

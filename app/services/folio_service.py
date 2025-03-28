from app import db
from app.models import Folio
from datetime import datetime

class FolioNotFoundException(Exception):
    pass

def create_folio(data):
    required_fields = ['case_id', 'folio_number']
    for field in required_fields:
        if not data.get(field):
            raise ValueError(f"'{field}' is a required field.")

    folio = Folio(
        case_id=data['case_id'],
        folio_number=data['folio_number'],
        description=data.get('description'),
        created_at=datetime.utcnow()
    )

    db.session.add(folio)
    db.session.commit()

    return folio

def list_folios():
    return Folio.query.all()

def delete_folio(folio_id):
    folio = Folio.query.get(folio_id)
    if not folio:
        raise FolioNotFoundException(f"Folio with id {folio_id} not found.")

    db.session.delete(folio)
    db.session.commit()

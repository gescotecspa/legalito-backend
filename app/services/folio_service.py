from datetime import datetime

from app import db
from app.models import Case, Folio


class FolioNotFoundException(Exception):
    pass


def create_folio_service(data):
    required_fields = ['case_id', 'folio_number']
    for field in required_fields:
        if not data.get(field):
            raise ValueError(f"'{field}' is a required field.")

    case = db.session.get(Case, data['case_id'])
    if not case:
        raise ValueError("Case not found.")

    folio = Folio(
        case_id=data['case_id'],
        folio_number=data['folio_number'],
        description=data.get('description'),
        created_at=datetime.utcnow()
    )

    db.session.add(folio)
    db.session.commit()

    return folio


def list_folios_service():
    return Folio.query.all()


def delete_folio_service(folio_id):
    folio = db.session.get(Folio, folio_id)
    if not folio:
        raise FolioNotFoundException(f"Folio with id {folio_id} not found.")

    db.session.delete(folio)
    db.session.commit()

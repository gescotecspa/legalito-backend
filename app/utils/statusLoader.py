from app.models.status import Status
from app import db

def initialize_statuses():
    default_statuses = [
        {'code': 'active', 'label': 'Activo'},
        {'code': 'suspended', 'label': 'Suspendido'},
        {'code': 'deleted', 'label': 'Eliminado'},
            # Agregás más y se insertan automáticamente
        # {'code': 'pending', 'label': 'Pendiente'},
        # {'code': 'inactive', 'label': 'Inactivo'},
    ]

    for status_data in default_statuses:
        if not Status.query.filter_by(code=status_data['code']).first():
            new_status = Status(**status_data)
            db.session.add(new_status)

    db.session.commit()
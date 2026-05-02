import unittest

from flask import Flask

from app import db
import app.models  # noqa: F401
from app.extensions import jwt
from app.models.case import Case
from app.models.folio import Folio
from app.services.folio_service import (
    FolioNotFoundException,
    create_folio_service,
    delete_folio_service,
)


class FolioServiceTests(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config.update(
            TESTING=True,
            SECRET_KEY="test-secret",
            JWT_SECRET_KEY="jwt-test-secret",
            SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
        )

        db.init_app(self.app)
        jwt.init_app(self.app)

        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

        self.case = Case(rit="RIT-001", name="Caso base", status="active")
        db.session.add(self.case)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_create_folio_service_when_case_does_not_exist_raises_value_error(self):
        with self.assertRaises(ValueError):
            create_folio_service({"case_id": 999, "folio_number": "F-001"})

    def test_create_folio_service_when_data_is_valid_creates_folio(self):
        folio = create_folio_service(
            {
                "case_id": self.case.id,
                "folio_number": "F-001",
                "description": "Descripcion",
            }
        )

        self.assertIsNotNone(folio.id)
        self.assertEqual(folio.folio_number, "F-001")

    def test_delete_folio_service_when_folio_does_not_exist_raises_not_found(self):
        with self.assertRaises(FolioNotFoundException):
            delete_folio_service(999)

    def test_delete_folio_service_removes_existing_folio(self):
        folio = Folio(case_id=self.case.id, folio_number="F-001", description="Descripcion")
        db.session.add(folio)
        db.session.commit()

        delete_folio_service(folio.id)

        deleted = db.session.get(Folio, folio.id)
        self.assertIsNone(deleted)


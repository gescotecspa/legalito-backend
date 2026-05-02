import unittest
from datetime import datetime, timedelta, timezone

from flask import Flask

from app import db
import app.models  # noqa: F401
from app.extensions import bcrypt, jwt
from app.models.status import Status
from app.models.terms_and_conditions import TermsAndConditions
from app.models.user import User
from app.services.terms_and_conditions_service import (
    TermsAndConditionsNotFoundException,
    TermsAndConditionsService,
    TermsUserNotFoundException,
)


class TermsAndConditionsServiceTests(unittest.TestCase):
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
        bcrypt.init_app(self.app)
        jwt.init_app(self.app)

        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

        active_status = Status(code="active", label="Activo")
        old_terms = TermsAndConditions(
            version="v1",
            content="Terminos v1",
            created_at=datetime.now(timezone.utc) - timedelta(days=1),
        )
        new_terms = TermsAndConditions(
            version="v2",
            content="Terminos v2",
            created_at=datetime.now(timezone.utc),
        )
        db.session.add_all([active_status, old_terms, new_terms])
        db.session.commit()

        self.user = User(
            user="terms-user@example.com",
            email="terms-user@example.com",
            first_name="Terms",
            last_name="User",
            password_hash="hash",
            status_id=active_status.id,
            terms_and_conditions_id=old_terms.id,
        )
        db.session.add(self.user)
        db.session.commit()

        self.latest_terms_id = new_terms.id

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_accept_terms_when_user_exists_updates_latest_terms(self):
        updated_user = TermsAndConditionsService.accept_terms(self.user.user)

        self.assertEqual(updated_user.terms_and_conditions_id, self.latest_terms_id)
        self.assertIsNotNone(updated_user.updated_at)

    def test_accept_terms_when_user_does_not_exist_raises_user_not_found(self):
        with self.assertRaises(TermsUserNotFoundException):
            TermsAndConditionsService.accept_terms("missing@example.com")

    def test_accept_terms_when_no_terms_exist_raises_terms_not_found(self):
        db.session.query(TermsAndConditions).delete()
        db.session.commit()

        with self.assertRaises(TermsAndConditionsNotFoundException):
            TermsAndConditionsService.accept_terms(self.user.user)

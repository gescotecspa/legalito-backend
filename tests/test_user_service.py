import unittest
from datetime import datetime, timedelta, timezone

from flask import Flask

from app import db
import app.models  # noqa: F401
from app.extensions import bcrypt, jwt
from app.models.status import Status
from app.models.terms_and_conditions import TermsAndConditions
from app.services.terms_and_conditions_service import (
    TermsAndConditionsNotFoundException,
    TermsVersionMismatchException,
)
from app.services.user_service import register_user


class UserServiceTests(unittest.TestCase):
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

        self.active_status = Status(code="active", label="Activo")
        self.old_terms = TermsAndConditions(
            version="v1",
            content="Terminos v1",
            created_at=datetime.now(timezone.utc) - timedelta(days=1),
        )
        self.latest_terms = TermsAndConditions(
            version="v2",
            content="Terminos v2",
            created_at=datetime.now(timezone.utc),
        )
        db.session.add_all([self.active_status, self.old_terms, self.latest_terms])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_register_user_when_terms_id_matches_latest_creates_user(self):
        user = register_user(
            "user@example.com",
            "Secret123!",
            "Ada",
            "Lovelace",
            self.latest_terms.id,
            self.latest_terms.version,
            True,
        )

        self.assertEqual(user["email"], "user@example.com")
        self.assertEqual(user["terms_and_conditions_id"], self.latest_terms.id)
        self.assertEqual(user["terms_version"], "v2")

    def test_register_user_when_terms_id_is_not_latest_raises_version_mismatch(self):
        with self.assertRaises(TermsVersionMismatchException):
            register_user(
                "user@example.com",
                "Secret123!",
                "Ada",
                "Lovelace",
                self.old_terms.id,
                self.old_terms.version,
                True,
            )

    def test_register_user_when_terms_version_is_not_latest_raises_version_mismatch(self):
        with self.assertRaises(TermsVersionMismatchException):
            register_user(
                "user@example.com",
                "Secret123!",
                "Ada",
                "Lovelace",
                self.latest_terms.id,
                "v0",
                True,
            )

    def test_register_user_when_no_terms_are_available_raises_terms_not_found(self):
        db.session.query(TermsAndConditions).delete()
        db.session.commit()

        with self.assertRaises(TermsAndConditionsNotFoundException):
            register_user(
                "user@example.com",
                "Secret123!",
                "Ada",
                "Lovelace",
                999,
                "v0",
                True,
            )

    def test_register_user_when_terms_are_not_accepted_raises_value_error(self):
        with self.assertRaises(ValueError):
            register_user(
                "user@example.com",
                "Secret123!",
                "Ada",
                "Lovelace",
                self.latest_terms.id,
                self.latest_terms.version,
                False,
            )

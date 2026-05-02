import unittest

from flask import Flask

from app import db
import app.models  # noqa: F401
from app.extensions import bcrypt, jwt
from app.models.email_account import EmailAccount
from app.models.status import Status
from app.models.terms_and_conditions import TermsAndConditions
from app.models.user import User
from app.services.email_account_service import (
    EmailAccountOwnershipException,
    update_email_account,
)


class EmailAccountServiceTests(unittest.TestCase):
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
        default_terms = TermsAndConditions(version="v1", content="Terminos")
        db.session.add_all([active_status, default_terms])
        db.session.commit()

        owner = User(
            user="owner@example.com",
            email="owner@example.com",
            first_name="Owner",
            last_name="User",
            password_hash="hash",
            status_id=active_status.id,
            terms_and_conditions_id=default_terms.id,
        )
        other = User(
            user="other@example.com",
            email="other@example.com",
            first_name="Other",
            last_name="User",
            password_hash="hash",
            status_id=active_status.id,
            terms_and_conditions_id=default_terms.id,
        )
        db.session.add_all([owner, other])
        db.session.commit()

        self.account = EmailAccount(
            provider="gmail",
            imap_server="imap.gmail.com",
            email_address="account@example.com",
            password="secret",
            active=True,
            user=owner.user,
        )
        self.other_account = EmailAccount(
            provider="outlook",
            imap_server="imap.outlook.com",
            email_address="other-account@example.com",
            password="secret",
            active=True,
            user=other.user,
        )
        db.session.add_all([self.account, self.other_account])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_update_email_account_when_account_belongs_to_other_user_raises_ownership_exception(self):
        with self.assertRaises(EmailAccountOwnershipException):
            update_email_account(
                self.account.id,
                "other@example.com",
                {"provider": "gmail-updated"},
            )

    def test_update_email_account_when_email_address_is_already_used_raises_value_error(self):
        with self.assertRaises(ValueError):
            update_email_account(
                self.account.id,
                "owner@example.com",
                {"email_address": "other-account@example.com"},
            )

    def test_update_email_account_when_data_is_valid_updates_account(self):
        updated = update_email_account(
            self.account.id,
            "owner@example.com",
            {
                "provider": "gmail-updated",
                "imap_server": "imap.new.com",
                "email_address": "new-account@example.com",
            },
        )

        self.assertEqual(updated.provider, "gmail-updated")
        self.assertEqual(updated.imap_server, "imap.new.com")
        self.assertEqual(updated.email_address, "new-account@example.com")

    def test_email_account_serialize_does_not_expose_password(self):
        serialized = self.account.serialize()

        self.assertNotIn("password", serialized)

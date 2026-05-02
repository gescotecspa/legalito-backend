import unittest
from datetime import datetime, timedelta, timezone
from unittest.mock import patch

from flask import Flask

from app import db
import app.models  # noqa: F401
from app.extensions import bcrypt, jwt
from app.integrations.mailjet_email import MailjetDeliveryException
from app.models.status import Status
from app.models.terms_and_conditions import TermsAndConditions
from app.models.user import User
from app.services.auth_service import (
    ExpiredResetCodeException,
    InactiveAccountException,
    InvalidCredentialsException,
    InvalidResetCodeException,
    PasswordResetDeliveryException,
    UserNotFoundException,
    login_user,
    request_password_reset,
    reset_password_with_code,
)


# Specs relacionadas:
# UC-001, APIs Auth README
class LoginUserTests(unittest.TestCase):
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
        self.suspended_status = Status(code="suspended", label="Suspendido")
        self.default_terms = TermsAndConditions(
            version="v1",
            content="Terminos de prueba",
        )
        db.session.add_all([self.active_status, self.suspended_status, self.default_terms])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def _create_user(self, email="user@example.com", password="secret123", status=None):
        user = User(
            user=email,
            email=email,
            first_name="Ada",
            last_name="Lovelace",
            password_hash=bcrypt.generate_password_hash(password).decode("utf-8"),
            status_id=(status or self.active_status).id,
        )
        db.session.add(user)
        db.session.commit()
        return user

    def test_login_user_when_credentials_are_valid_returns_token_and_serialized_user(self):
        user = self._create_user()

        result = login_user(user.email, "secret123")

        self.assertIn("access_token", result)
        self.assertEqual(result["user"]["user"], user.user)
        self.assertEqual(result["user"]["status"]["code"], "active")
        self.assertNotIn("password_hash", result["user"])
        self.assertNotIn("reset_code", result["user"])
        self.assertIsNotNone(db.session.get(User, user.user).last_login)

    def test_login_user_when_email_does_not_exist_raises_invalid_credentials(self):
        with self.assertRaises(InvalidCredentialsException):
            login_user("missing@example.com", "secret123")

    def test_login_user_when_password_is_invalid_raises_invalid_credentials(self):
        user = self._create_user()

        with self.assertRaises(InvalidCredentialsException):
            login_user(user.email, "wrong-password")

    def test_login_user_when_status_is_not_active_raises_inactive_account(self):
        user = self._create_user(email="inactive@example.com", status=self.suspended_status)

        with self.assertRaises(InactiveAccountException):
            login_user(user.email, "secret123")

    @patch("app.services.auth_service.send_reset_email")
    def test_request_password_reset_when_user_exists_sets_code_and_sends_email(self, send_reset_email_mock):
        user = self._create_user()

        result = request_password_reset(user.email)

        updated_user = db.session.get(User, user.user)
        self.assertEqual(result["message"], "A recovery code has been sent to your email")
        self.assertIsNotNone(updated_user.reset_code)
        self.assertEqual(len(updated_user.reset_code), 6)
        self.assertIsNotNone(updated_user.reset_code_expiration)
        send_reset_email_mock.assert_called_once_with(user.email, user.first_name, updated_user.reset_code)

    def test_request_password_reset_when_user_does_not_exist_raises_user_not_found(self):
        with self.assertRaises(UserNotFoundException):
            request_password_reset("missing@example.com")

    @patch("app.services.auth_service.send_reset_email")
    def test_request_password_reset_when_mailjet_fails_raises_delivery_exception_and_does_not_persist_code(
        self,
        send_reset_email_mock,
    ):
        user = self._create_user(email="delivery@example.com")
        send_reset_email_mock.side_effect = MailjetDeliveryException(
            "Mailjet delivery failed"
        )

        with self.assertRaises(PasswordResetDeliveryException):
            request_password_reset(user.email)

        updated_user = db.session.get(User, user.user)
        self.assertIsNone(updated_user.reset_code)
        self.assertIsNone(updated_user.reset_code_expiration)

    def test_reset_password_with_code_when_code_is_valid_updates_password_and_clears_reset_fields(self):
        user = self._create_user()
        user.reset_code = "123456"
        user.reset_code_expiration = datetime.utcnow() + timedelta(minutes=15)
        db.session.commit()

        result = reset_password_with_code(user.email, "123456", "new-secret")

        updated_user = db.session.get(User, user.user)
        self.assertEqual(result["message"], "Password successfully updated")
        self.assertTrue(bcrypt.check_password_hash(updated_user.password_hash, "new-secret"))
        self.assertIsNone(updated_user.reset_code)
        self.assertIsNone(updated_user.reset_code_expiration)
        self.assertIsNotNone(updated_user.updated_at)

    def test_reset_password_with_code_when_code_is_invalid_raises_invalid_reset_code(self):
        user = self._create_user()
        user.reset_code = "123456"
        user.reset_code_expiration = datetime.utcnow() + timedelta(minutes=15)
        db.session.commit()

        with self.assertRaises(InvalidResetCodeException):
            reset_password_with_code(user.email, "654321", "new-secret")

    def test_reset_password_with_code_when_code_is_expired_raises_expired_reset_code(self):
        user = self._create_user()
        user.reset_code = "123456"
        user.reset_code_expiration = datetime.utcnow() - timedelta(minutes=1)
        db.session.commit()

        with self.assertRaises(ExpiredResetCodeException):
            reset_password_with_code(user.email, "123456", "new-secret")

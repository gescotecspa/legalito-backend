import unittest
from unittest.mock import patch

from flask import Flask

from app import db
import app.models  # noqa: F401
from app.api.auth import auth_bp
from app.extensions import bcrypt, jwt
from app.services.auth_service import (
    ExpiredResetCodeException,
    InactiveAccountException,
    InvalidCredentialsException,
    InvalidResetCodeException,
    PasswordResetDeliveryException,
    UserNotFoundException as AuthUserNotFoundException,
)
from app.services.user_service import EmailAlreadyExistsException
from app.utils.rate_limit import rate_limiter


# Specs relacionadas:
# UC-001, APIs Auth README
class AuthApiTests(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config.update(
            TESTING=True,
            SECRET_KEY="test-secret",
            JWT_SECRET_KEY="jwt-test-secret",
            SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            AUTH_LOGIN_RATE_LIMIT_ATTEMPTS=1,
            AUTH_LOGIN_RATE_LIMIT_WINDOW_SECONDS=300,
            AUTH_FORGOT_PASSWORD_RATE_LIMIT_ATTEMPTS=1,
            AUTH_FORGOT_PASSWORD_RATE_LIMIT_WINDOW_SECONDS=300,
            AUTH_RESET_PASSWORD_RATE_LIMIT_ATTEMPTS=1,
            AUTH_RESET_PASSWORD_RATE_LIMIT_WINDOW_SECONDS=300,
        )

        db.init_app(self.app)
        bcrypt.init_app(self.app)
        jwt.init_app(self.app)
        self.app.register_blueprint(auth_bp, url_prefix="/api")

        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()
        rate_limiter.reset()
        self.client = self.app.test_client()

    def tearDown(self):
        rate_limiter.reset()
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_login_when_email_or_password_is_missing_returns_bad_request(self):
        response = self.client.post("/api/auth/login", json={"email": "user@example.com"})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()["error"], "Email and password are required")

    @patch("app.api.auth.login_user", side_effect=InvalidCredentialsException("Email o contraseña incorrectos"))
    def test_login_when_credentials_are_invalid_returns_unauthorized(self, _login_user_mock):
        response = self.client.post(
            "/api/auth/login",
            json={"email": "user@example.com", "password": "wrong-password"},
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.get_json()["error"], "Email o contraseña incorrectos")

    @patch("app.api.auth.login_user", side_effect=InactiveAccountException("La cuenta no está activa"))
    def test_login_when_account_is_inactive_returns_forbidden(self, _login_user_mock):
        response = self.client.post(
            "/api/auth/login",
            json={"email": "user@example.com", "password": "secret123"},
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.get_json()["error"], "La cuenta no está activa")

    @patch(
        "app.api.auth.login_user",
        return_value={"access_token": "token", "user": {"email": "user@example.com"}},
    )
    def test_login_when_rate_limit_is_exceeded_returns_too_many_requests(self, login_user_mock):
        first_response = self.client.post(
            "/api/auth/login",
            json={"email": "user@example.com", "password": "secret123"},
        )
        second_response = self.client.post(
            "/api/auth/login",
            json={"email": "user@example.com", "password": "secret123"},
        )

        self.assertEqual(first_response.status_code, 200)
        self.assertEqual(second_response.status_code, 429)
        self.assertEqual(
            second_response.get_json()["error"],
            "Too many login attempts. Please try again later.",
        )
        self.assertIn("Retry-After", second_response.headers)
        login_user_mock.assert_called_once_with("user@example.com", "secret123")

    def test_register_when_request_is_not_json_returns_unsupported_media_type(self):
        response = self.client.post(
            "/api/auth/register",
            data="email=user@example.com",
            content_type="text/plain",
        )

        self.assertEqual(response.status_code, 415)
        self.assertEqual(response.get_json()["error"], "El request debe ser JSON")

    @patch("app.api.auth.register_user", side_effect=EmailAlreadyExistsException("El email ya está registrado"))
    def test_register_when_email_already_exists_returns_conflict(self, _register_user_mock):
        response = self.client.post(
            "/api/auth/register",
            json={
                "email": "user@example.com",
                "password": "secret123",
                "firstName": "Ada",
                "lastName": "Lovelace",
            },
        )

        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.get_json()["error"], "El email ya está registrado")

    @patch("app.api.auth.request_password_reset", side_effect=AuthUserNotFoundException("User not found"))
    def test_forgot_password_when_user_is_missing_returns_not_found(self, _request_password_reset_mock):
        response = self.client.post("/api/auth/forgot-password", json={"email": "missing@example.com"})

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json()["error"], "User not found")

    @patch(
        "app.api.auth.request_password_reset",
        side_effect=PasswordResetDeliveryException("No se pudo enviar el correo de recuperacion"),
    )
    def test_forgot_password_when_mail_delivery_fails_returns_bad_gateway(self, _request_password_reset_mock):
        response = self.client.post("/api/auth/forgot-password", json={"email": "user@example.com"})

        self.assertEqual(response.status_code, 502)
        self.assertEqual(
            response.get_json()["error"],
            "No se pudo enviar el correo de recuperacion",
        )

    @patch(
        "app.api.auth.request_password_reset",
        return_value={"message": "A recovery code has been sent to your email"},
    )
    def test_forgot_password_when_rate_limit_is_exceeded_returns_too_many_requests(
        self,
        request_password_reset_mock,
    ):
        first_response = self.client.post("/api/auth/forgot-password", json={"email": "user@example.com"})
        second_response = self.client.post("/api/auth/forgot-password", json={"email": "user@example.com"})

        self.assertEqual(first_response.status_code, 200)
        self.assertEqual(second_response.status_code, 429)
        self.assertEqual(
            second_response.get_json()["error"],
            "Too many password recovery attempts. Please try again later.",
        )
        self.assertIn("Retry-After", second_response.headers)
        request_password_reset_mock.assert_called_once_with("user@example.com")

    def test_reset_password_when_fields_are_missing_returns_bad_request(self):
        response = self.client.post("/api/auth/reset-password", json={"email": "user@example.com"})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json()["error"],
            "Email, reset code, and new password are required",
        )

    @patch("app.api.auth.reset_password_with_code", side_effect=InvalidResetCodeException("Incorrect code"))
    def test_reset_password_when_code_is_invalid_returns_bad_request(self, _reset_password_mock):
        response = self.client.post(
            "/api/auth/reset-password",
            json={
                "email": "user@example.com",
                "reset_code": "123456",
                "password": "new-secret",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()["error"], "Incorrect code")

    @patch("app.api.auth.reset_password_with_code", side_effect=ExpiredResetCodeException("Code expired"))
    def test_reset_password_when_code_is_expired_returns_bad_request(self, _reset_password_mock):
        response = self.client.post(
            "/api/auth/reset-password",
            json={
                "email": "user@example.com",
                "reset_code": "123456",
                "password": "new-secret",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()["error"], "Code expired")

    @patch(
        "app.api.auth.reset_password_with_code",
        return_value={"message": "Password successfully updated"},
    )
    def test_reset_password_when_rate_limit_is_exceeded_returns_too_many_requests(
        self,
        reset_password_mock,
    ):
        payload = {
            "email": "user@example.com",
            "reset_code": "123456",
            "password": "new-secret",
        }

        first_response = self.client.post("/api/auth/reset-password", json=payload)
        second_response = self.client.post("/api/auth/reset-password", json=payload)

        self.assertEqual(first_response.status_code, 200)
        self.assertEqual(second_response.status_code, 429)
        self.assertEqual(
            second_response.get_json()["error"],
            "Too many password reset attempts. Please try again later.",
        )
        self.assertIn("Retry-After", second_response.headers)
        reset_password_mock.assert_called_once_with(
            "user@example.com",
            "123456",
            "new-secret",
        )

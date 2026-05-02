import unittest
from unittest.mock import patch

from flask import Flask

from app.api.users import users_bp
from app.extensions import jwt
from app.services.user_service import UserNotFoundException


class UsersApiTests(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config.update(
            TESTING=True,
            SECRET_KEY="test-secret",
            JWT_SECRET_KEY="jwt-test-secret",
        )
        jwt.init_app(self.app)
        self.app.register_blueprint(users_bp, url_prefix="/api")
        self.client = self.app.test_client()

    def test_delete_account_when_email_or_password_is_missing_returns_bad_request(self):
        response = self.client.post("/api/users/delete-account", json={"email": "user@example.com"})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()["error"], "Email y contraseña son requeridos")

    @patch("app.api.users.delete_user", side_effect=UserNotFoundException())
    def test_delete_account_when_user_does_not_exist_returns_not_found(self, _delete_user_mock):
        response = self.client.post(
            "/api/users/delete-account",
            json={"email": "user@example.com", "password": "Secret123!"},
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json()["error"], "Usuario no encontrado")

    @patch("app.api.users.delete_user", side_effect=ValueError("Contraseña incorrecta"))
    def test_delete_account_when_password_is_invalid_returns_unauthorized(self, _delete_user_mock):
        response = self.client.post(
            "/api/users/delete-account",
            json={"email": "user@example.com", "password": "wrong"},
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.get_json()["error"], "Contraseña incorrecta")

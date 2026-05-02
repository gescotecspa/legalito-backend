import unittest
from types import SimpleNamespace
from unittest.mock import patch

from flask import Flask
from flask_jwt_extended import create_access_token

from app.api.courthouses import courthouses_bp
from app.extensions import jwt


class CourthousesApiTests(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config.update(
            TESTING=True,
            SECRET_KEY="test-secret",
            JWT_SECRET_KEY="jwt-test-secret",
        )
        jwt.init_app(self.app)
        self.app.register_blueprint(courthouses_bp, url_prefix="/api")
        self.client = self.app.test_client()
        with self.app.app_context():
            self.auth_headers = {
                "Authorization": f"Bearer {create_access_token(identity='courthouse-user@example.com')}"
            }

    def test_list_courthouses_when_request_is_unauthenticated_returns_unauthorized(self):
        response = self.client.get("/api/courthouses")

        self.assertEqual(response.status_code, 401)

    @patch(
        "app.api.courthouses.list_courthouses_service",
        return_value=[SimpleNamespace(serialize=lambda: {"id": 1, "name": "Juzgado Civil"})],
    )
    def test_list_courthouses_returns_serialized_courthouses(self, list_courthouses_mock):
        response = self.client.get("/api/courthouses", headers=self.auth_headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()[0]["name"], "Juzgado Civil")
        list_courthouses_mock.assert_called_once_with()

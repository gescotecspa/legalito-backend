import unittest
from types import SimpleNamespace
from unittest.mock import patch

from flask import Flask

from app.api.roles import roles_bp


class RolesApiTests(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config.update(TESTING=True, SECRET_KEY="test-secret")
        self.app.register_blueprint(roles_bp, url_prefix="/api")
        self.client = self.app.test_client()

    @patch(
        "app.api.roles.list_roles_service",
        return_value=[SimpleNamespace(serialize=lambda: {"id": 1, "name": "Admin"})],
    )
    def test_list_roles_returns_serialized_roles(self, list_roles_mock):
        response = self.client.get("/api/roles")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()[0]["name"], "Admin")
        list_roles_mock.assert_called_once_with()

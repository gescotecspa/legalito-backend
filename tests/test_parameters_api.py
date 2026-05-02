import unittest
from types import SimpleNamespace
from unittest.mock import patch

from flask import Flask

from app.api.parameters import parameters_bp


class ParametersApiTests(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config.update(TESTING=True, SECRET_KEY="test-secret")
        self.app.register_blueprint(parameters_bp, url_prefix="/api")
        self.client = self.app.test_client()

    @patch(
        "app.api.parameters.list_parameters_service",
        return_value=[SimpleNamespace(serialize=lambda: {"id": 1, "name": "Estado"})],
    )
    def test_list_parameters_returns_serialized_parameters(self, list_parameters_mock):
        response = self.client.get("/api/parameters")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()[0]["id"], 1)
        list_parameters_mock.assert_called_once_with()

    @patch(
        "app.api.parameters.list_parameters_by_parent_service",
        return_value=[SimpleNamespace(serialize=lambda: {"id": 2, "parent_id": 1, "name": "Activo"})],
    )
    def test_list_parameters_by_parent_returns_serialized_parameters(self, list_by_parent_mock):
        response = self.client.get("/api/parameters/byparent/1")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()[0]["parent_id"], 1)
        list_by_parent_mock.assert_called_once_with(1)

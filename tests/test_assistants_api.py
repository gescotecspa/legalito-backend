import unittest
from types import SimpleNamespace
from unittest.mock import patch

from flask import Flask
from flask_jwt_extended import create_access_token

from app.api.assistants import assistants_bp
from app.extensions import jwt
from app.services.assistant_service import AssistantNotFoundException


class AssistantsApiTests(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config.update(
            TESTING=True,
            SECRET_KEY="test-secret",
            JWT_SECRET_KEY="jwt-test-secret",
        )
        jwt.init_app(self.app)
        self.app.register_blueprint(assistants_bp, url_prefix="/api")
        self.client = self.app.test_client()
        with self.app.app_context():
            self.auth_headers = {
                "Authorization": f"Bearer {create_access_token(identity='assistants-user@example.com')}"
            }

    def test_add_favorite_when_request_is_unauthenticated_returns_unauthorized(self):
        response = self.client.post("/api/assistants/favorite/add", json={"assistantId": 1})

        self.assertEqual(response.status_code, 401)

    @patch(
        "app.api.assistants.list_assistants_service",
        return_value=[SimpleNamespace(serialize=lambda: {"id": 1, "first_name": "Ada"})],
    )
    def test_list_assistants_returns_serialized_assistants(self, list_assistants_mock):
        response = self.client.get(
            "/api/assistants",
            headers=self.auth_headers,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()[0]["id"], 1)
        list_assistants_mock.assert_called_once_with()

    @patch(
        "app.api.assistants.list_assistants_by_filter_service",
        return_value=[{"id": 2, "first_name": "Grace"}],
    )
    def test_list_assistants_by_filter_returns_filtered_items(self, list_by_filter_mock):
        response = self.client.get(
            "/api/assistants/filter/1/2",
            headers=self.auth_headers,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()[0]["id"], 2)
        list_by_filter_mock.assert_called_once_with(1, 2)

    @patch("app.api.assistants.list_assistants_favorite_service", return_value=[{"id": 5}])
    def test_list_favorite_assistants_uses_authenticated_user(self, list_favorites_mock):
        response = self.client.post(
            "/api/assistants/favorites",
            json={"user": "forged@example.com"},
            headers=self.auth_headers,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()[0]["id"], 5)
        list_favorites_mock.assert_called_once_with("assistants-user@example.com")

    @patch("app.api.assistants.add_favorite_assistant_service", return_value=True)
    def test_add_favorite_when_jwt_is_present_uses_authenticated_user(
        self,
        add_favorite_mock,
    ):
        response = self.client.post(
            "/api/assistants/favorite/add",
            json={"assistantId": 5, "user": "forged@example.com"},
            headers=self.auth_headers,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.get_json())
        add_favorite_mock.assert_called_once_with(5, "assistants-user@example.com")

    def test_add_favorite_when_assistant_id_is_missing_returns_bad_request(self):
        response = self.client.post(
            "/api/assistants/favorite/add",
            json={},
            headers=self.auth_headers,
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()["error"], "Assistant parameter is required.")

    @patch(
        "app.api.assistants.delete_favorite_assistant_service",
        side_effect=AssistantNotFoundException("Favorite assistant not found"),
    )
    def test_delete_favorite_when_favorite_is_missing_returns_not_found(self, _delete_favorite_mock):
        response = self.client.delete(
            "/api/assistants/favorite/delete",
            json={"assistantId": 5},
            headers=self.auth_headers,
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json()["error"], "Favorite assistant not found")

    @patch("app.api.assistants.delete_favorite_assistant_service", return_value=True)
    def test_delete_favorite_when_jwt_is_present_uses_authenticated_user(
        self,
        delete_favorite_mock,
    ):
        response = self.client.delete(
            "/api/assistants/favorite/delete",
            json={"assistantId": 5, "user": "forged@example.com"},
            headers=self.auth_headers,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.get_json())
        delete_favorite_mock.assert_called_once_with(5, "assistants-user@example.com")

    @patch(
        "app.api.assistants.get_assistant_service",
        return_value=SimpleNamespace(serialize=lambda: {"id": 7, "first_name": "Ada"}),
    )
    def test_get_assistant_profile_returns_serialized_assistant(self, get_assistant_mock):
        response = self.client.get(
            "/api/assistants/profile/7",
            headers=self.auth_headers,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["id"], 7)
        get_assistant_mock.assert_called_once_with(7)

    @patch("app.api.assistants.get_assistant_service", return_value=None)
    def test_get_assistant_profile_when_assistant_is_missing_returns_not_found(self, get_assistant_mock):
        response = self.client.get(
            "/api/assistants/profile/9",
            headers=self.auth_headers,
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json()["error"], "Assistant not found")
        get_assistant_mock.assert_called_once_with(9)

import unittest
from types import SimpleNamespace
from unittest.mock import patch

from flask import Flask
from flask_jwt_extended import create_access_token

from app.api.notifications import notifications_bp
from app.extensions import jwt
from app.services.notification_service import NotificationNotFoundException


class NotificationsApiTests(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config.update(
            TESTING=True,
            SECRET_KEY="test-secret",
            JWT_SECRET_KEY="jwt-test-secret",
        )
        jwt.init_app(self.app)
        self.app.register_blueprint(notifications_bp, url_prefix="/api")
        self.client = self.app.test_client()
        with self.app.app_context():
            self.auth_headers = {
                "Authorization": f"Bearer {create_access_token(identity='notifications-user@example.com')}"
            }

    def test_list_notifications_by_user_when_request_is_unauthenticated_returns_unauthorized(self):
        response = self.client.post("/api/notifications/byUser", json={})

        self.assertEqual(response.status_code, 401)

    @patch("app.api.notifications.get_notifications_by_user", return_value=[])
    def test_list_notifications_by_user_when_jwt_is_present_returns_ok(
        self,
        get_notifications_mock,
    ):
        response = self.client.post(
            "/api/notifications/byUser",
            json={},
            headers=self.auth_headers,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [])
        get_notifications_mock.assert_called_once_with("notifications-user@example.com")

    @patch(
        "app.api.notifications.get_notification",
        return_value=SimpleNamespace(serialize=lambda: {"id": 7, "user": "notifications-user@example.com"}),
    )
    def test_get_notification_by_id_when_jwt_is_present_uses_authenticated_user(
        self,
        get_notification_mock,
    ):
        response = self.client.get(
            "/api/notifications/7",
            headers=self.auth_headers,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["id"], 7)
        get_notification_mock.assert_called_once_with(7, "notifications-user@example.com")

    @patch(
        "app.api.notifications.delete_notification",
        side_effect=NotificationNotFoundException("Notification with id 9 not found."),
    )
    def test_delete_notification_when_it_does_not_belong_to_user_returns_not_found(
        self,
        delete_notification_mock,
    ):
        response = self.client.delete(
            "/api/notifications/9",
            headers=self.auth_headers,
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.get_json()["error"],
            "Notification with id 9 not found.",
        )
        delete_notification_mock.assert_called_once_with(9, "notifications-user@example.com")

    @patch("app.api.notifications.dismiss", return_value=True)
    def test_dismiss_notification_when_body_has_forged_user_uses_authenticated_user(
        self,
        dismiss_mock,
    ):
        response = self.client.post(
            "/api/notifications/dismiss",
            json={"id": 12, "user": "forged@example.com"},
            headers=self.auth_headers,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.get_json())
        dismiss_mock.assert_called_once_with(12, "notifications-user@example.com")

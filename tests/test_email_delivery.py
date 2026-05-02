import unittest
from unittest.mock import patch

from flask import Flask

from app.integrations.email_delivery import EmailDeliveryException, send_reset_email


class EmailDeliveryTests(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__, template_folder="app/templates")
        self.app.config.update(
            TESTING=True,
            SECRET_KEY="test-secret",
            EMAIL_DELIVERY_METHOD="local",
        )
        self.ctx = self.app.app_context()
        self.ctx.push()

    def tearDown(self):
        self.ctx.pop()

    @patch("app.integrations.email_delivery.send_reset_email_via_local_smtp", return_value={"status": 200})
    def test_send_reset_email_when_method_is_local_uses_local_provider(self, local_provider_mock):
        result = send_reset_email("user@example.com", "Ada", "123456")

        self.assertEqual(result["status"], 200)
        local_provider_mock.assert_called_once_with("user@example.com", "Ada", "123456")

    @patch("app.integrations.email_delivery.send_reset_email_via_api", return_value={"status": 200})
    def test_send_reset_email_when_method_is_api_uses_api_provider(self, api_provider_mock):
        self.app.config["EMAIL_DELIVERY_METHOD"] = "api"

        result = send_reset_email("user@example.com", "Ada", "123456")

        self.assertEqual(result["status"], 200)
        api_provider_mock.assert_called_once_with("user@example.com", "Ada", "123456")

    def test_send_reset_email_when_method_is_unknown_raises_delivery_exception(self):
        self.app.config["EMAIL_DELIVERY_METHOD"] = "unsupported"

        with self.assertRaises(EmailDeliveryException):
            send_reset_email("user@example.com", "Ada", "123456")

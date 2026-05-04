import unittest
from unittest.mock import MagicMock, patch

from flask import Flask

from app.integrations.email_delivery import EmailDeliveryException, send_reset_email
from app.integrations.local_smtp_email import (
    LocalSmtpDeliveryException,
    send_reset_email as send_reset_email_via_local_smtp,
)


class EmailDeliveryTests(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__, template_folder="app/templates")
        self.app.config.update(
            TESTING=True,
            SECRET_KEY="test-secret",
            EMAIL_DELIVERY_METHOD="local",
            SMTP_SERVER="smtp.example.com",
            SMTP_PORT=587,
            SMTP_USERNAME="smtp-user",
            SMTP_PASSWORD="smtp-pass",
            SMTP_DEFAULT_SENDER="noreply@example.com",
            SMTP_USE_TLS=True,
            SMTP_USE_SSL=False,
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

    @patch("app.integrations.email_delivery.send_reset_email_via_local_smtp", return_value={"status": 200})
    def test_send_reset_email_defaults_to_local_provider(self, local_provider_mock):
        self.app.config["EMAIL_DELIVERY_METHOD"] = None

        result = send_reset_email("user@example.com", "Ada", "123456")

        self.assertEqual(result["status"], 200)
        local_provider_mock.assert_called_once_with("user@example.com", "Ada", "123456")

    @patch("app.integrations.local_smtp_email.load_reset_email_template", return_value="<p>reset</p>")
    @patch("app.integrations.local_smtp_email.smtplib.SMTP")
    def test_local_smtp_delivery_uses_starttls_by_default(self, smtp_mock, template_mock):
        server = MagicMock()
        smtp_mock.return_value.__enter__.return_value = server

        result = send_reset_email_via_local_smtp("user@example.com", "Ada", "123456")

        self.assertEqual(result["status"], 200)
        template_mock.assert_called_once_with("Ada", "123456")
        server.starttls.assert_called_once_with()
        server.login.assert_called_once_with("smtp-user", "smtp-pass")
        server.sendmail.assert_called_once()

    @patch("app.integrations.local_smtp_email.load_reset_email_template", return_value="<p>reset</p>")
    @patch("app.integrations.local_smtp_email.smtplib.SMTP_SSL")
    @patch("app.integrations.local_smtp_email.smtplib.SMTP")
    def test_local_smtp_delivery_uses_ssl_client_without_starttls(self, smtp_mock, smtp_ssl_mock, template_mock):
        self.app.config["SMTP_USE_TLS"] = False
        self.app.config["SMTP_USE_SSL"] = True
        server = MagicMock()
        smtp_ssl_mock.return_value.__enter__.return_value = server

        result = send_reset_email_via_local_smtp("user@example.com", "Ada", "123456")

        self.assertEqual(result["status"], 200)
        template_mock.assert_called_once_with("Ada", "123456")
        smtp_mock.assert_not_called()
        server.starttls.assert_not_called()
        server.login.assert_called_once_with("smtp-user", "smtp-pass")
        server.sendmail.assert_called_once()

    def test_local_smtp_delivery_requires_smtp_server_config(self):
        self.app.config["SMTP_SERVER"] = None

        with self.assertRaises(LocalSmtpDeliveryException):
            send_reset_email_via_local_smtp("user@example.com", "Ada", "123456")

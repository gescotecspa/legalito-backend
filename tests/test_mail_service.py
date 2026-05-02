import unittest
from types import SimpleNamespace
from unittest.mock import patch

from flask import Flask

from app.services.mail_service import (
    ActiveEmailAccountNotFoundException,
    MailReadIntegrationException,
    SenderFilterNotFoundException,
    read_mails_for_user,
)


class MailServiceTests(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.ctx = self.app.app_context()
        self.ctx.push()

    def tearDown(self):
        self.ctx.pop()

    @patch("app.services.mail_service.list_parameters_by_parent", return_value=[])
    def test_read_mails_for_user_when_sender_filter_is_missing_raises_exception(
        self,
        _list_parameters_mock,
    ):
        with self.assertRaises(SenderFilterNotFoundException):
            read_mails_for_user("account@example.com", "user@example.com")

    @patch(
        "app.services.mail_service.list_parameters_by_parent",
        return_value=[SimpleNamespace(name="tribunal@example.com")],
    )
    @patch("app.services.mail_service.get_user_active_email", return_value=None)
    def test_read_mails_for_user_when_account_is_missing_raises_exception(
        self,
        _get_user_active_email_mock,
        _list_parameters_mock,
    ):
        with self.assertRaises(ActiveEmailAccountNotFoundException):
            read_mails_for_user("account@example.com", "user@example.com")

    @patch(
        "app.services.mail_service.list_parameters_by_parent",
        return_value=[SimpleNamespace(name="tribunal@example.com")],
    )
    @patch(
        "app.services.mail_service.get_user_active_email",
        return_value=SimpleNamespace(
            imap_server="imap.example.com",
            email_address="account@example.com",
            password="secret",
        ),
    )
    @patch(
        "app.services.mail_service.read_unread_emails_for_account",
        return_value=[{"error": "imap failure"}],
    )
    def test_read_mails_for_user_when_imap_fails_raises_integration_exception(
        self,
        _read_unread_mails_mock,
        _get_user_active_email_mock,
        _list_parameters_mock,
    ):
        with self.assertRaises(MailReadIntegrationException):
            read_mails_for_user("account@example.com", "user@example.com")

    @patch(
        "app.services.mail_service.list_parameters_by_parent",
        return_value=[SimpleNamespace(name="tribunal@example.com")],
    )
    @patch(
        "app.services.mail_service.get_user_active_email",
        return_value=SimpleNamespace(
            imap_server="imap.example.com",
            email_address="account@example.com",
            password="secret",
        ),
    )
    @patch(
        "app.services.mail_service.read_unread_emails_for_account",
        return_value=[
            {
                "subject": "Citacion 01/05/2026 10:00",
                "from": "tribunal@example.com",
                "body": "Lugar: Sala 1",
            }
        ],
    )
    @patch("app.services.mail_service.create_notification", return_value=True)
    @patch(
        "app.services.mail_service.create_and_send_ics_file",
        return_value="Invitacion enviada",
    )
    def test_read_mails_for_user_when_email_contains_invitation_returns_extracted_event(
        self,
        _send_ics_mock,
        _create_notification_mock,
        _read_unread_mails_mock,
        _get_user_active_email_mock,
        _list_parameters_mock,
    ):
        result = read_mails_for_user("account@example.com", "user@example.com")

        self.assertEqual(result["email_address"], "account@example.com")
        self.assertEqual(len(result["extracted_events"]), 1)

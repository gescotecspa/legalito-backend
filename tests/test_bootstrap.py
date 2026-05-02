import os
import unittest
from contextlib import contextmanager
from unittest.mock import MagicMock, patch


class AppFactoryTests(unittest.TestCase):
    @patch.dict(
        os.environ,
        {
            "DATABASE_URL": "sqlite:///:memory:",
            "SECRET_KEY": "test-secret",
            "JWT_SECRET_KEY": "jwt-test-secret",
        },
        clear=False,
    )
    @patch("app.cli.initialize_statuses")
    @patch("app.cli.initialize_terms_and_conditions")
    def test_create_app_when_initialized_does_not_run_setup_side_effects(
        self,
        initialize_terms_mock,
        initialize_statuses_mock,
    ):
        from app import create_app

        app = create_app()

        self.assertIsNotNone(app)
        self.assertIn("setup-initial-data", app.cli.commands)
        self.assertIn("recreate-db", app.cli.commands)
        initialize_statuses_mock.assert_not_called()
        initialize_terms_mock.assert_not_called()

    @patch.dict(
        os.environ,
        {
            "SECRET_KEY": "",
            "JWT_SECRET_KEY": "",
        },
        clear=False,
    )
    def test_create_app_when_secret_key_is_missing_raises_runtime_error(self):
        from app import create_app

        with self.assertRaises(RuntimeError):
            create_app()


class CliCommandTests(unittest.TestCase):
    @patch.dict(
        os.environ,
        {
            "DATABASE_URL": "sqlite:///:memory:",
            "SECRET_KEY": "test-secret",
            "JWT_SECRET_KEY": "jwt-test-secret",
        },
        clear=False,
    )
    def setUp(self):
        from app import create_app

        self.app = create_app()
        self.runner = self.app.test_cli_runner()

    @patch("app.cli.initialize_statuses")
    @patch("app.cli.initialize_terms_and_conditions")
    def test_setup_initial_data_runs_seed_loaders(self, initialize_terms_mock, initialize_statuses_mock):
        result = self.runner.invoke(args=["setup-initial-data"])

        self.assertEqual(result.exit_code, 0, msg=result.output)
        initialize_statuses_mock.assert_called_once_with()
        initialize_terms_mock.assert_called_once_with()

    @patch("app.cli.migrate_upgrade")
    @patch("app.cli.initialize_statuses")
    @patch("app.cli.initialize_terms_and_conditions")
    @patch("app.cli.db")
    def test_recreate_db_runs_schema_reset_migrations_and_seed_loaders(
        self,
        db_mock,
        initialize_terms_mock,
        initialize_statuses_mock,
        migrate_upgrade_mock,
    ):
        executed_sql = []

        class ConnectionStub:
            def execute(self, statement):
                executed_sql.append(str(statement))

        @contextmanager
        def begin_stub():
            yield ConnectionStub()

        db_mock.engine.begin.side_effect = begin_stub

        result = self.runner.invoke(args=["recreate-db", "--yes"])

        self.assertEqual(result.exit_code, 0, msg=result.output)
        self.assertEqual(
            executed_sql,
            ["DROP SCHEMA public CASCADE", "CREATE SCHEMA public"],
        )
        migrate_upgrade_mock.assert_called_once_with()
        initialize_statuses_mock.assert_called_once_with()
        initialize_terms_mock.assert_called_once_with()

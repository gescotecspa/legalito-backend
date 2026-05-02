import click
from sqlalchemy import text
from flask_migrate import upgrade as migrate_upgrade

from app import db
from app.utils.statusLoader import initialize_statuses
from app.utils.termsLoader import initialize_terms_and_conditions


def register_cli_commands(app):
    @app.cli.command("setup-initial-data")
    def setup_initial_data():
        """Carga datos base requeridos para entornos locales o no productivos."""
        initialize_statuses()
        initialize_terms_and_conditions()
        app.logger.info("Initial data setup completed")

    @app.cli.command("recreate-db")
    @click.option(
        "--yes",
        is_flag=True,
        help="Confirma sin pedir validacion interactiva.",
    )
    def recreate_db(yes):
        """Recrea el esquema completo, aplica migraciones y carga datos base."""
        if not yes:
            click.confirm(
                "Esto eliminara todo el esquema actual de la base configurada. Quieres continuar?",
                abort=True,
            )

        app.logger.warning("Dropping and recreating public schema")

        with db.engine.begin() as connection:
            connection.execute(text("DROP SCHEMA public CASCADE"))
            connection.execute(text("CREATE SCHEMA public"))

        app.logger.info("Running database migrations")
        migrate_upgrade()

        app.logger.info("Loading initial data")
        initialize_statuses()
        initialize_terms_and_conditions()

        app.logger.info("Database recreation completed")

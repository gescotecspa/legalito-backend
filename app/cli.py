from app.utils.statusLoader import initialize_statuses


def register_cli_commands(app):
    @app.cli.command("setup-initial-data")
    def setup_initial_data():
        """Carga datos base requeridos para entornos locales o no productivos."""
        initialize_statuses()
        app.logger.info("Initial data setup completed")

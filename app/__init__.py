import logging
import os

from flask import Flask, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app.extensions import bcrypt, jwt


# Inicializamos SQLAlchemy
db = SQLAlchemy()
migrate = Migrate()


def _parse_allowed_origins(value):
    return {origin.strip() for origin in value.split(",") if origin.strip()}


def register_cors_headers(app):
    allowed_origins = _parse_allowed_origins(app.config.get("CORS_ALLOWED_ORIGINS", ""))

    @app.after_request
    def add_cors_headers(response):
        origin = request.headers.get("Origin")

        if origin in allowed_origins:
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Credentials"] = "true"
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, PATCH, DELETE, OPTIONS"
            response.headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type"
            response.headers["Access-Control-Max-Age"] = "3600"
            response.headers.add("Vary", "Origin")

        return response


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    configured_secret_key = os.getenv("SECRET_KEY")
    if configured_secret_key is not None:
        app.config["SECRET_KEY"] = configured_secret_key

    if not app.config.get('SECRET_KEY'):
        raise RuntimeError("SECRET_KEY must be configured")

    configured_jwt_secret = os.getenv("JWT_SECRET_KEY")
    if configured_jwt_secret is not None:
        app.config["JWT_SECRET_KEY"] = configured_jwt_secret
    elif not app.config.get("JWT_SECRET_KEY"):
        app.config["JWT_SECRET_KEY"] = app.config["SECRET_KEY"]

    # Configurar logging para que se muestren todos los logs de Flask
    logging.basicConfig(level=logging.DEBUG)
    app.logger.setLevel(logging.DEBUG)

    # Inicializamos la base de datos
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    register_cors_headers(app)
    # Importar y registrar blueprints después de que la app esté configurada
    from .api import register_blueprints
    register_blueprints(app)

    from .cli import register_cli_commands
    register_cli_commands(app)

    return app

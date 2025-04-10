from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.extensions import bcrypt, jwt
from flask_migrate import Migrate
import logging
# Inicializamos SQLAlchemy
db = SQLAlchemy()
migrate = Migrate()
def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Configurar logging para que se muestren todos los logs de Flask
    logging.basicConfig(level=logging.DEBUG)
    app.logger.setLevel(logging.DEBUG)

    # Inicializamos la base de datos
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    # Importar y registrar blueprints después de que la app esté configurada
    from .api import register_blueprints
    register_blueprints(app)

    with app.app_context():
        db.create_all()

    return app

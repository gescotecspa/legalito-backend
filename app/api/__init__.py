from .health import health_bp
from .email_accounts import email_accounts_bp
from .mails import mails_bp
from .events import events_bp
from .cases import case_bp
from .notifications import notifications_bp
from .folios import folios_bp
from .parameters import parameters_bp
from .roles import roles_bp
from .assistants import assistants_bp
from .courthouses import courthouses_bp
from .users import users_bp
from .auth import auth_bp

def register_blueprints(app):
    app.register_blueprint(health_bp, url_prefix='/api')
    app.register_blueprint(email_accounts_bp, url_prefix='/api')
    app.register_blueprint(mails_bp, url_prefix='/api')
    app.register_blueprint(events_bp, url_prefix='/api')
    app.register_blueprint(case_bp, url_prefix='/api')
    app.register_blueprint(notifications_bp, url_prefix='/api')
    app.register_blueprint(folios_bp, url_prefix='/api')
    app.register_blueprint(parameters_bp, url_prefix='/api')
    app.register_blueprint(roles_bp, url_prefix='/api')
    app.register_blueprint(assistants_bp, url_prefix='/api')
    app.register_blueprint(courthouses_bp, url_prefix='/api')
    app.register_blueprint(users_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/api')
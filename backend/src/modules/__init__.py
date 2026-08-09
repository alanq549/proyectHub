# modules/__init__.py
from flask import Blueprint

# Main blueprint for all modules
modules_bp = Blueprint('modules', __name__, url_prefix='/api/v1')

from .auth.routes import auth_bp
from .users.routes import users_bp
from .calls.routes import calls_bp
from .projects.routes import projects_bp
from .documents.routes import documents_bp
from .history.routes import history_bp

modules_bp.register_blueprint(auth_bp)
modules_bp.register_blueprint(users_bp)
modules_bp.register_blueprint(calls_bp, url_prefix='/calls')
modules_bp.register_blueprint(projects_bp, url_prefix='/projects')
modules_bp.register_blueprint(documents_bp, url_prefix='/documents')
modules_bp.register_blueprint(history_bp, url_prefix='/history')

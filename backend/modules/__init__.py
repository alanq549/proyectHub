from flask import Blueprint

# Main blueprint for all modules
modules_bp = Blueprint('modules', __name__, url_prefix='/api/v1')

# Import and register blueprints for each module
from .auth.routes import auth_bp
from .users.routes import users_bp

modules_bp.register_blueprint(auth_bp)
modules_bp.register_blueprint(users_bp)

# src/modules/auth/routes.py
from flask_jwt_extended import jwt_required
from . import auth_bp
from .auth_controller import AuthController

@auth_bp.route('/register', methods=['POST'])
def register():
    return AuthController.register()

@auth_bp.route('/login', methods=['POST'])
def login():
    return AuthController.login()

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    return AuthController.refresh()

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    return AuthController.logout()

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    return AuthController.get_current_user()

@auth_bp.route('/me', methods=['PUT'])
@jwt_required()
def update_current_user():
    return AuthController.update_current_user()
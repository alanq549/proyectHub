# src/modules/users/routes.py
from flask_jwt_extended import jwt_required
from src.middleware.auth import admin_required
from . import users_bp
from .user_controller import UserController

@users_bp.route('', methods=['GET'])
@admin_required()
def get_users():
    return UserController.get_users()


@users_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    return UserController.get_user(user_id)


@users_bp.route('', methods=['POST'])
@admin_required()
def create_user():
    return UserController.create_user()


@users_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    return UserController.update_user(user_id)


# FIX CRÍTICO 1: Endpoint dedicado y seguro para cambio de contraseña
@users_bp.route('/me/password', methods=['PUT'])
@jwt_required()
def change_password():
    return UserController.change_password()


@users_bp.route('/<int:user_id>', methods=['DELETE'])
@admin_required()
def delete_user(user_id):
    return UserController.delete_user(user_id)
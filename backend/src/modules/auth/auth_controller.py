from flask import request, jsonify
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)
from .auth_service import AuthService
from modules.users.user_repository import UserRepository # Needed for /me endpoint

class AuthController:
    @staticmethod
    def register():
        data = request.get_json() or {}
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not username or not email or not password:
            return jsonify({'error': 'Todos los campos son obligatorios'}), 400

        try:
            user = AuthService.register_user(username, email, password)
            return jsonify({
                'message': 'Usuario registrado exitosamente',
                'user': user.to_dict()
            }), 201
        except ValueError as e:
            return jsonify({'error': str(e)}), 400

    @staticmethod
    def login():
        data = request.get_json() or {}
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({'error': 'Email y contraseña son obligatorios'}), 400

        try:
            result = AuthService.authenticate_user(email, password)
            return jsonify({
                'message': 'Inicio de sesión exitoso',
                **result
            }), 200
        except ValueError as e:
            return jsonify({'error': str(e)}), 401
        except PermissionError as e:
            return jsonify({'error': str(e)}), 403

    @staticmethod
    @jwt_required(refresh=True)
    def refresh():
        current_user_id = get_jwt_identity()
        new_access_token = AuthService.refresh_access_token(current_user_id)
        return jsonify({'access_token': new_access_token}), 200

    @staticmethod
    @jwt_required()
    def logout():
        return jsonify({'message': 'Sesión cerrada exitosamente'}), 200

    @staticmethod
    @jwt_required()
    def get_current_user():
        current_user_id = get_jwt_identity()
        user = UserRepository.get_by_id(current_user_id)

        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404

        return jsonify(user.to_dict()), 200
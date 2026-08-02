# src/modules/auth/auth_controller.py
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from .auth_service import AuthService
from src.modules.users.user_repository import UserRepository

class AuthController:
    @staticmethod
    def _extract_data():
        data = {}
        json_data = request.get_json(silent=True)
        if json_data:
            data.update(json_data)
        form_data = request.form
        if form_data:
            data.update(form_data.to_dict())
        return data

    @staticmethod
    def register():
        data = AuthController._extract_data()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        first_name = data.get('first_name')
        last_name = data.get('last_name')

        if not username or not email or not password:
            return jsonify({'error': 'Nombre de usuario, email y contraseña son obligatorios'}), 400

        try:
            user = AuthService.register_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            return jsonify({
                'message': 'Usuario registrado exitosamente',
                'user': user.to_dict()
            }), 201
        except ValueError as e:
            return jsonify({'error': str(e)}), 400

    @staticmethod
    def login():
        data = AuthController._extract_data()
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
    def refresh():
        current_user_id = get_jwt_identity()
        new_access_token = AuthService.refresh_access_token(current_user_id)
        return jsonify({'access_token': new_access_token}), 200

    @staticmethod
    def logout():
        return jsonify({'message': 'Sesión cerrada exitosamente'}), 200

    @staticmethod
    def get_current_user():
        current_user_id = get_jwt_identity()
        user = UserRepository.get_by_id(current_user_id)

        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404

        return jsonify(user.to_dict()), 200

    @staticmethod
    def update_current_user():
        from src.modules.users.user_service import UserService

        current_user_id = get_jwt_identity()
        data = AuthController._extract_data()
        file = request.files.get('file')

        if file and not file.filename:
            file = None

        try:
            user = UserService.update_user(
                current_user_id,
                data,
                file=file,
                is_admin=False
            )
            return jsonify({
                'message': 'Perfil actualizado exitosamente',
                'user': user
            }), 200
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except PermissionError as e:
            return jsonify({'error': str(e)}), 403
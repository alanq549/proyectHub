# src/modules/users/user_controller.py
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity
from .user_service import UserService
from src.modules.users.user_repository import UserRepository

class UserController:
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
    def _is_admin():
        current_user_id = get_jwt_identity()
        current_user = UserRepository.get_by_id(current_user_id)
        return current_user is not None and current_user.role == 'admin'

    @staticmethod
    def get_users():
        users = UserService.get_all_users()
        return jsonify(users), 200

    @staticmethod
    def get_user(user_id):
        current_user_id = get_jwt_identity()
        is_admin = UserController._is_admin()

        if not is_admin and current_user_id != user_id:
            return jsonify({'error': 'Acceso denegado: No tienes permisos para consultar este usuario'}), 403

        try:
            user = UserService.get_user_by_id(user_id)
            return jsonify(user), 200
        except ValueError as e:
            return jsonify({'error': str(e)}), 404

    @staticmethod
    def create_user():
        data = UserController._extract_data()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        role = data.get('role', 'user')

        # AGREGADO: Extraer el archivo enviado en la solicitud multipart/form-data
        file = request.files.get('file')
        if file and not file.filename:
            file = None

        if not username or not email or not password:
            return jsonify({'error': 'Nombre de usuario, correo y contraseña son obligatorios'}), 400

        try:
            # AGREGADO: Pasar 'file=file' al servicio
            user = UserService.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                role=role,
                file=file
            )
            
            return jsonify({
                'message': 'Usuario creado exitosamente',
                'user': user
            }), 201
        except ValueError as e:
            return jsonify({'error': str(e)}), 400

    @staticmethod
    def update_user(user_id):
        current_user_id = int(get_jwt_identity())
        is_admin = UserController._is_admin()

        if not is_admin and current_user_id != user_id:

            return jsonify({'error': 'Acceso denegado: No tienes permisos para modificar este usuario'}), 403

        data = UserController._extract_data()
        file = request.files.get('file')

        if file and not file.filename:
            file = None

        try:
            user = UserService.update_user(user_id, data, file=file, is_admin=is_admin)
            return jsonify({
                'message': 'Usuario actualizado exitosamente',
                'user': user
            }), 200
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except PermissionError as e:
            return jsonify({'error': str(e)}), 403

    # FIX CRÍTICO 1: Controlador para cambio de contraseña seguro
    @staticmethod
    def change_password():
        current_user_id = get_jwt_identity()
        data = UserController._extract_data()
        
        current_password = data.get('current_password')
        new_password = data.get('new_password')

        if not current_password or not new_password:
            return jsonify({'error': 'Debe proporcionar la contraseña actual y la nueva contraseña'}), 400

        try:
            UserService.change_password(current_user_id, current_password, new_password)
            return jsonify({'message': 'Contraseña actualizada exitosamente'}), 200
        except ValueError as e:
            return jsonify({'error': str(e)}), 400

    @staticmethod
    def delete_user(user_id):
        try:
            UserService.delete_user(user_id)
            return jsonify({'message': 'Usuario eliminado exitosamente'}), 200
        except ValueError as e:
            return jsonify({'error': str(e)}), 404
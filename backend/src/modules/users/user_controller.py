from flask import request, jsonify
from flask_jwt_extended import jwt_required
from .user_service import UserService

class UserController:
    @staticmethod
    @jwt_required()
    def get_users():
        users = UserService.get_all_users()
        return jsonify(users), 200

    @staticmethod
    @jwt_required()
    def get_user(user_id):
        try:
            user = UserService.get_user_by_id(user_id)
            return jsonify(user), 200
        except ValueError as e:
            return jsonify({'error': str(e)}), 404

    @staticmethod
    @jwt_required()
    def create_user():
        data = request.get_json() or {}
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not username or not email or not password:
            return jsonify({'error': 'Nombre de usuario, correo y contraseña son obligatorios'}), 400

        try:
            user = UserService.create_user(username, email, password)
            return jsonify({
                'message': 'Usuario creado exitosamente',
                'user': user
            }), 201
        except ValueError as e:
            return jsonify({'error': str(e)}), 400

    @staticmethod
    @jwt_required()
    def update_user(user_id):
        data = request.get_json() or {}
        try:
            user = UserService.update_user(user_id, data)
            return jsonify({
                'message': 'Usuario actualizado exitosamente',
                'user': user
            }), 200
        except ValueError as e:
            return jsonify({'error': str(e)}), 400

    @staticmethod
    @jwt_required()
    def delete_user(user_id):
        try:
            UserService.delete_user(user_id)
            return jsonify({'message': 'Usuario eliminado exitosamente'}), 200
        except ValueError as e:
            return jsonify({'error': str(e)}), 404
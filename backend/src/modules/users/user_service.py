# modules/users/user_service.py
from models.user import User
from .user_repository import UserRepository

class UserService:

    @staticmethod
    def get_all_users():
        users = UserRepository.get_all()
        return [user.to_dict() for user in users]

    @staticmethod
    def get_user_by_id(user_id):
        user = UserRepository.get_by_id(user_id)
        if not user:
            raise ValueError('Usuario no encontrado')
        return user.to_dict()

    @staticmethod
    def create_user(username, email, password):
        if UserRepository.get_by_email(email):
            raise ValueError('El correo electrónico ya está registrado')

        if UserRepository.get_by_username(username):
            raise ValueError('El nombre de usuario ya está en uso')

        user = User(username=username, email=email)
        user.set_password(password)

        UserRepository.add(user)

        return user.to_dict()

    @staticmethod
    def update_user(user_id, data):
        user = UserRepository.get_by_id(user_id)
        if not user:
            raise ValueError('Usuario no encontrado')

        if 'username' in data and data['username'] != user.username:
            if UserRepository.get_by_username(data['username']):
                raise ValueError('El nombre de usuario ya está en uso')
            user.username = data['username']

        if 'email' in data and data['email'] != user.email:
            if UserRepository.get_by_email(data['email']):
                raise ValueError('El correo electrónico ya está registrado')
            user.email = data['email']

        if 'password' in data and data['password']:
            user.set_password(data['password'])

        if 'is_active' in data:
            user.is_active = bool(data['is_active'])

        UserRepository.update()
        return user.to_dict()

    @staticmethod
    def delete_user(user_id):
        user = UserRepository.get_by_id(user_id)
        if not user:
            raise ValueError('Usuario no encontrado')

        UserRepository.delete(user)
        return True
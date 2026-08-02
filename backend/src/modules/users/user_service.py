# modules/users/user_service.py
from src.models.user import User
from src.modules.users.user_repository import UserRepository
from src.services.storage_service import StorageService

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
    def create_user(username, email, password, first_name=None, last_name=None, role='user'):
        if UserRepository.get_by_email(email):
            raise ValueError('El correo electrónico ya está registrado')

        if UserRepository.get_by_username(username):
            raise ValueError('El nombre de usuario ya está en uso')

        if role not in ('user', 'admin'):
            raise ValueError('Rol inválido. Los valores permitidos son: user, admin')

        user = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            role=role
        )
        user.set_password(password)

        UserRepository.add(user)

        return user.to_dict()

    @staticmethod
    def update_user(user_id, data, file=None, is_admin=False):
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

        if 'first_name' in data:
            user.first_name = data['first_name']

        if 'last_name' in data:
            user.last_name = data['last_name']

        if 'password' in data and data['password']:
            user.set_password(data['password'])

        if 'is_active' in data:
            user.is_active = bool(data['is_active'])

        if 'role' in data and data['role']:
            if not is_admin:
                raise PermissionError('Solo un administrador puede modificar el rol de un usuario')
            if data['role'] not in ('user', 'admin'):
                raise ValueError('Rol inválido. Los valores permitidos son: user, admin')
            user.role = data['role']

        if file is not None:
            try:
                profile_url = StorageService.upload_file(file, folder='profiles')
                user.profile_picture_url = profile_url
            except ValueError:
                pass

        UserRepository.update()
        return user.to_dict()

    @staticmethod
    def delete_user(user_id):
        user = UserRepository.get_by_id(user_id)
        if not user:
            raise ValueError('Usuario no encontrado')

        UserRepository.delete(user)
        return True
# modules/users/user_service.py
from src.models.user import User
from src.modules.users.user_repository import UserRepository
from src.services.storage_service import StorageService
from extensions.db import db
from src.utils.logger import log_activity  # Helper centralizado

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
    def create_user(username, email, password, first_name=None, last_name=None, role='user', is_active=True, file=None, current_user_id=None):
        if UserRepository.get_by_email(email):
            raise ValueError('El correo electrónico ya está registrado')

        if UserRepository.get_by_username(username):
            raise ValueError('El nombre de usuario ya está en uso')

        if role not in ('user', 'admin'):
            raise ValueError('Rol inválido. Los valores permitidos son: user, admin')

        # Convertir a booleano real por si viene como string desde FormData
        if isinstance(is_active, str):
            is_active = is_active.lower() in ('true', '1', 't')

        user = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            role=role,
            is_active=is_active
        )
        user.set_password(password)

        if file is not None:
            try:
                profile_url = StorageService.upload_file(file, folder='profiles')
                user.profile_picture_url = profile_url
            except ValueError:
                pass

        UserRepository.add(user)
        db.session.flush()

        # Registrar actividad en la bitácora
        actor_id = current_user_id if current_user_id else user.id
        log_activity(
            user_id=actor_id,
            action='USER_CREATED',
            entity_type='User',
            entity_id=user.id,
            description=f"Se creó el usuario '{user.username}' (Rol: {user.role})."
        )
        db.session.commit()

        return user.to_dict()

    @staticmethod
    def update_user(user_id, data, file=None, is_admin=False, current_user_id=None):
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

        if 'is_active' in data:
            val = data['is_active']
            if isinstance(val, str):
                user.is_active = val.lower() in ('true', '1', 't')
            else:
                user.is_active = bool(val)

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
        db.session.flush()

        actor_id = current_user_id if current_user_id else user.id
        log_activity(
            user_id=actor_id,
            action='USER_UPDATED',
            entity_type='User',
            entity_id=user.id,
            description=f"Se actualizaron los datos del usuario '{user.username}'."
        )
        db.session.commit()

        return user.to_dict()

    @staticmethod
    def change_password(user_id, current_password, new_password):
        user = UserRepository.get_by_id(user_id)
        if not user:
            raise ValueError('Usuario no encontrado')

        if not user.check_password(current_password):
            raise ValueError('La contraseña actual es incorrecta')

        if len(new_password) < 6:
            raise ValueError('La nueva contraseña debe tener al menos 6 caracteres')

        user.set_password(new_password)
        UserRepository.update()
        db.session.flush()

        log_activity(
            user_id=user.id,
            action='PASSWORD_CHANGED',
            entity_type='User',
            entity_id=user.id,
            description=f"El usuario '{user.username}' cambió su contraseña."
        )
        db.session.commit()

        return True

    @staticmethod
    def delete_user(user_id, current_user_id=None):
        user = UserRepository.get_by_id(user_id)
        if not user:
            raise ValueError('Usuario no encontrado')

        username = user.username
        UserRepository.delete(user)
        db.session.flush()

        actor_id = current_user_id if current_user_id else user_id
        log_activity(
            user_id=actor_id,
            action='USER_DELETED',
            entity_type='User',
            entity_id=user_id,
            description=f"Se eliminó al usuario '{username}'."
        )
        db.session.commit()

        return True
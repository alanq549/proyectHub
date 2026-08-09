# src/modules/auth/auth_service.py
# AuthService para manejar la autenticación de usuarios
from src.models.user import User
from src.modules.users.user_repository import UserRepository
from flask_jwt_extended import create_access_token, create_refresh_token
from extensions.db import db
from src.utils.logger import log_activity  # Helper centralizado
import os

class AuthService:

    @staticmethod
    def register_user(username, email, password, first_name=None, last_name=None):
        if UserRepository.get_by_email(email):
            raise ValueError('El correo electrónico ya está registrado')

        if UserRepository.get_by_username(username):
            raise ValueError('El nombre de usuario ya está en uso')

        existing_users_count = User.query.count() if hasattr(User.query, 'count') else len(UserRepository.get_all())

        default_role = 'user'
        if existing_users_count == 0 and os.getenv('BOOTSTRAP_FIRST_USER_AS_ADMIN', 'true').lower() == 'true':
            default_role = 'admin'

        user = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            role=default_role
        )
        user.set_password(password)

        UserRepository.add(user)
        db.session.flush() # Asegura que el user.id esté disponible

        # Registrar en la bitácora
        log_activity(
            user_id=user.id,
            action='USER_REGISTERED',
            entity_type='User',
            entity_id=user.id,
            description=f"El usuario '{user.username}' se ha registrado exitosamente."
        )
        db.session.commit()

        return user

    @staticmethod
    def authenticate_user(email, password):
        user = UserRepository.get_by_email(email)

        if not user or not user.check_password(password):
            raise ValueError('Credenciales inválidas')

        if not user.is_active:
            raise PermissionError('El usuario está inactivo')

        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))

        # Registrar inicio de sesión en la bitácora
        log_activity(
            user_id=user.id,
            action='USER_LOGIN',
            entity_type='User',
            entity_id=user.id,
            description=f"El usuario '{user.username}' inició sesión."
        )
        db.session.commit()

        return {
            'user': user.to_dict(),
            'access_token': access_token,
            'refresh_token': refresh_token
        }

    @staticmethod
    def refresh_access_token(user_id):
        return create_access_token(identity=str(user_id))

    @staticmethod
    def get_user_by_id(user_id):
        user = UserRepository.get_by_id(user_id)
        if not user:
            raise ValueError('Usuario no encontrado')
        return user.to_dict()

    @staticmethod
    def update_password(user_id, old_password, new_password):
        user = UserRepository.get_by_id(user_id)
        if not user:
            raise ValueError('Usuario no encontrado')
        if not user.check_password(old_password):
            raise ValueError('Contraseña antigua incorrecta')
        
        user.set_password(new_password)
        UserRepository.update(user)

        # Registrar cambio de contraseña en la bitácora
        log_activity(
            user_id=user.id,
            action='PASSWORD_UPDATED',
            entity_type='User',
            entity_id=user.id,
            description=f"El usuario '{user.username}' actualizó su contraseña."
        )
        db.session.commit()
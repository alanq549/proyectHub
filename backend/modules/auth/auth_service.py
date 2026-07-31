from models.user import User
from extensions.db import db
from flask_jwt_extended import create_access_token, create_refresh_token

class AuthService:

    @staticmethod
    def register_user(username, email, password):
        # Validar si ya existe usuario o email
        if User.query.filter_by(email=email).first():
            raise ValueError('El correo electrónico ya está registrado')

        if User.query.filter_by(username=username).first():
            raise ValueError('El nombre de usuario ya está en uso')

        # Crear nuevo usuario
        user = User(username=username, email=email)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        return user

    @staticmethod
    def authenticate_user(email, password):
        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            raise ValueError('Credenciales inválidas')

        if not user.is_active:
            raise PermissionError('El usuario está inactivo')

        # Generar tokens
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))

        return {
            'user': user.to_dict(),
            'access_token': access_token,
            'refresh_token': refresh_token
        }

    @staticmethod
    def refresh_access_token(user_id):
        return create_access_token(identity=str(user_id))
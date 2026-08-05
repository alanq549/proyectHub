from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from src.modules.users.user_repository import UserRepository


def admin_required():
    """
    Decorador para proteger endpoints que requieren rol 'admin'.
    Retorna 403 Forbidden si el usuario no tiene permisos.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            verify_jwt_in_request()

            current_user_id = get_jwt_identity()
            current_user = UserRepository.get_by_id(current_user_id)

            if not current_user or current_user.role != "admin":
                return jsonify(
                    {"error": "Acceso denegado: Requiere rol de administrador"}
                ), 403

            return f(*args, **kwargs)

        return decorated_function

    return decorator
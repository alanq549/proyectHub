from . import users_bp
from .user_controller import UserController

@users_bp.route('', methods=['GET'])
def get_users():
    return UserController.get_users()


@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return UserController.get_user(user_id)


@users_bp.route('', methods=['POST'])
def create_user():
    return UserController.create_user()


@users_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    return UserController.update_user(user_id)


@users_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    return UserController.delete_user(user_id)
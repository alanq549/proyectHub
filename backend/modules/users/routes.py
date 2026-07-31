from . import users_bp
from flask import jsonify

@users_bp.route('/profile', methods=['GET'])
def get_user_profile():
    return jsonify({'message': 'User profile route placeholder'}), 200

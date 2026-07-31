from . import auth_bp
from flask import jsonify

@auth_bp.route('/login', methods=['POST'])
def login():
    return jsonify({'message': 'Login route placeholder'}), 200

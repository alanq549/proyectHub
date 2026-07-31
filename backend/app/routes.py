from flask import Blueprint, jsonify

# Ejemplo de Blueprint
bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return jsonify({'message': 'Welcome to ProjectHub API!'})

# Aquí se definirán las rutas y la lógica de negocio asociada
# Ejemplo:
# @bp.route('/users', methods=['GET'])
# def get_users():
#    # Lógica para obtener usuarios
#    pass

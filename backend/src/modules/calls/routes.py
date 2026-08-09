#src/modules/calls/routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.middleware.auth import admin_required
from src.models.user import User
from .call_controller import CallController
from .call_service import CallService

calls_bp = Blueprint('calls', __name__)

# --- RUTAS DE CONVOCATORIAS ---
@calls_bp.route('/', methods=['GET'])
@jwt_required()
def get_calls():
    return CallController.get_all()

@calls_bp.route('/<int:call_id>', methods=['GET'])
@jwt_required()
def get_call(call_id):
    return CallController.get_by_id(call_id)

@calls_bp.route('/<int:call_id>/workspace', methods=['GET'])
@jwt_required()
def get_call_workspace(call_id):
    return CallController.get_workspace(call_id)

@calls_bp.route('/', methods=['POST'])
@admin_required()
def create_call():
    return CallController.create()

@calls_bp.route('/<int:call_id>', methods=['PUT'])
@admin_required()
def update_call(call_id):
    return CallController.update(call_id)

@calls_bp.route('/<int:call_id>', methods=['DELETE'])
@admin_required()
def delete_call(call_id):
    return CallController.delete(call_id)

# --- INSCRIPCIÓN Y EVALUACIÓN DE POSTULACIONES ---
@calls_bp.route('/<int:call_id>/join', methods=['POST'])
@jwt_required()
def join_call(call_id):
    user_id = get_jwt_identity()
    data, error, status = CallService.join_call(call_id, user_id)
    if error and status != 201:
        return jsonify({"error": error}), status
    return jsonify({"message": "Inscripción realizada con éxito", "data": data}), status

@calls_bp.route('/<int:call_id>/requirements', methods=['POST'])
@admin_required()
def add_requirement(call_id):
    data = request.get_json() or {}
    req, error = CallService.add_requirement(call_id, data)
    if error:
        return jsonify({"error": error}), 400
    return jsonify({"message": "Requisito agregado", "data": req}), 201

@calls_bp.route('/participants/<int:participant_id>/status', methods=['PATCH'])
@admin_required()
def update_participant_status(participant_id):
    data = request.get_json() or {}
    status = data.get("status")
    updated, error = CallService.update_application_status(participant_id, status)
    if error:
        return jsonify({"error": error}), 400
    return jsonify({"message": "Estado actualizado", "data": updated}), 200
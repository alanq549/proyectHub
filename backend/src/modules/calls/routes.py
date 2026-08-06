# src/modules/calls/routes.py
from flask import Blueprint
from flask_jwt_extended import jwt_required
from src.middleware.auth import admin_required
from .call_controller import CallController

calls_bp = Blueprint('calls', __name__)

@calls_bp.route('/', methods=['GET'])
@jwt_required()
def get_calls():
    return CallController.get_all()

@calls_bp.route('/<int:call_id>', methods=['GET'])
@jwt_required()
def get_call(call_id):
    return CallController.get_by_id(call_id)

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
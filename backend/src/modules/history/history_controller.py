# src/modules/history/history_controller.py
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.modules.history.history_service import HistoryService
from src.models.user import User

class HistoryController:
    def __init__(self):
        self.service = HistoryService()

    @jwt_required()
    def get_history(self):
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)

        entity_type = request.args.get('entity_type', type=str)
        entity_id = request.args.get('entity_id', type=int)
        limit = request.args.get('limit', default=50, type=int)

        logs = self.service.get_history(
            current_user, 
            entity_type=entity_type, 
            entity_id=entity_id, 
            limit=limit
        )

        return jsonify({
            'status': 'success',
            'data': [log.to_dict() for log in logs]
        }), 200
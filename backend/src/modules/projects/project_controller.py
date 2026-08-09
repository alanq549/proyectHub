from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.modules.projects.project_service import ProjectService
from src.models.user import User

class ProjectController:
    def __init__(self):
        self.service = ProjectService()

    @jwt_required()
    def get_projects(self):
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)

        call_id = request.args.get('call_id', type=int)
        status = request.args.get('status', type=str)

        projects = self.service.get_projects(current_user, call_id=call_id, status=status)
        return jsonify({
            'status': 'success',
            'data': [p.to_dict() for p in projects]
        }), 200

    @jwt_required()
    def get_project_by_id(self, id):
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)

        project, error, status_code = self.service.get_project_by_id(id, current_user)
        if error:
            return jsonify({'status': 'error', 'message': error}), status_code

        return jsonify({
            'status': 'success',
            'data': project.to_dict()
        }), 200

    @jwt_required()
    def create_project(self):
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        data = request.get_json() or {}

        project, error, status_code = self.service.create_project(data, current_user)
        if error:
            return jsonify({'status': 'error', 'message': error}), status_code

        return jsonify({
            'status': 'success',
            'message': 'Proyecto creado exitosamente',
            'data': project.to_dict()
        }), status_code

    @jwt_required()
    def update_project(self, id):
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        data = request.get_json() or {}

        project, error, status_code = self.service.update_project(id, data, current_user)
        if error:
            return jsonify({'status': 'error', 'message': error}), status_code

        return jsonify({
            'status': 'success',
            'message': 'Proyecto actualizado exitosamente',
            'data': project.to_dict()
        }), status_code

    @jwt_required()
    def delete_project(self, id):
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)

        _, error, status_code = self.service.delete_project(id, current_user)
        if error:
            return jsonify({'status': 'error', 'message': error}), status_code

        return jsonify({
            'status': 'success',
            'message': 'Proyecto eliminado exitosamente'
        }), status_code
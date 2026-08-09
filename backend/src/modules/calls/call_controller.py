# src/modules/calls/call_controller.py
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import User
from .call_service import CallService


class CallController:

    @staticmethod
    def get_all():
        calls = CallService.get_all_calls()
        return jsonify({"data": calls}), 200

    @staticmethod
    def get_by_id(call_id):
        call, error = CallService.get_call_by_id(call_id)

        if error:
            return jsonify({"error": error}), 404

        return jsonify({"data": call}), 200

    @staticmethod
    def create():
        data = request.get_json() or {}

        call, error = CallService.create_call(data)

        if error:
            return jsonify({"error": error}), 400

        return (
            jsonify({"message": "Convocatoria creada exitosamente", "data": call}),
            201,
        )

    @staticmethod
    def update(call_id):
        data = request.get_json() or {}

        call, error = CallService.update_call(call_id, data)

        if error:
            status = 404 if error == "Convocatoria no encontrada" else 400
            return jsonify({"error": error}), status

        return (
            jsonify({"message": "Convocatoria actualizada exitosamente", "data": call}),
            200,
        )

    @staticmethod
    def delete(call_id):
        success, error = CallService.delete_call(call_id)

        if not success:
            return jsonify({"error": error}), 404

        return jsonify({"message": "Convocatoria eliminada exitosamente"}), 200

    @staticmethod
    @jwt_required()
    def get_workspace(id):
        print("====== ENTRÓ A GET WORKSPACE ======")
        print("CALL ID:", id)

        current_user_id = get_jwt_identity()
        print("USER ID:", current_user_id)

        current_user = User.query.get(current_user_id)
        print("USER:", current_user)

        if not current_user:
            print("USUARIO NO ENCONTRADO")
            return jsonify({"status": "error", "message": "Usuario no encontrado"}), 404

        print("ANTES DE CALL SERVICE")

        workspace_data, error, status_code = CallService.get_workspace(id, current_user)

        print("DESPUÉS DE CALL SERVICE")
        print("ERROR:", error)
        print("STATUS:", status_code)

        if error:
            return jsonify({"status": "error", "message": error}), status_code

        print("====== TERMINANDO WORKSPACE ======")

        return jsonify({"status": "success", "data": workspace_data}), 200
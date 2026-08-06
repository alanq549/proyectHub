# src/modules/calls/call_controller.py
from flask import request, jsonify
from .call_service import CallService

class CallController:
    @staticmethod
    def get_all():
        calls = CallService.get_all_calls()
        return jsonify({'data': calls}), 200

    @staticmethod
    def get_by_id(call_id):
        call, error = CallService.get_call_by_id(call_id)
        if error:
            return jsonify({'error': error}), 404
        return jsonify({'data': call}), 200

    @staticmethod
    def create():
        data = request.get_json() or {}
        call, error = CallService.create_call(data)
        if error:
            return jsonify({'error': error}), 400
        return jsonify({'message': 'Convocatoria creada exitosamente', 'data': call}), 201

    @staticmethod
    def update(call_id):
        data = request.get_json() or {}
        call, error = CallService.update_call(call_id, data)
        if error:
            status = 404 if error == "Convocatoria no encontrada" else 400
            return jsonify({'error': error}), status
        return jsonify({'message': 'Convocatoria actualizada exitosamente', 'data': call}), 200

    @staticmethod
    def delete(call_id):
        success, error = CallService.delete_call(call_id)
        if not success:
            return jsonify({'error': error}), 404
        return jsonify({'message': 'Convocatoria eliminada exitosamente'}), 200
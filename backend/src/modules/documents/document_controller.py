from flask import request, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.modules.documents.document_service import DocumentService
from src.models.user import User

class DocumentController:
    def __init__(self):
        self.service = DocumentService()

    @jwt_required()
    def get_documents(self):
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)

        project_id = request.args.get('project_id', type=int)
        call_id = request.args.get('call_id', type=int)

        docs = self.service.get_documents(current_user, project_id=project_id, call_id=call_id)
        return jsonify({
            'status': 'success',
            'data': [d.to_dict() for d in docs]
        }), 200

    @jwt_required()
    def get_document_by_id(self, id):
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)

        doc, error, status_code = self.service.get_document_by_id(id, current_user)
        if error:
            return jsonify({'status': 'error', 'message': error}), status_code

        return jsonify({
            'status': 'success',
            'data': doc.to_dict()
        }), 200

    @jwt_required()
    def upload_document(self):
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)

        if 'file' not in request.files:
            return jsonify({'status': 'error', 'message': 'No se encontró archivo en la petición'}), 400

        file = request.files['file']
        project_id = request.form.get('project_id', type=int)
        call_id = request.form.get('call_id', type=int)

        doc, error, status_code = self.service.upload_document(file, current_user, project_id, call_id)
        if error:
            return jsonify({'status': 'error', 'message': error}), status_code

        return jsonify({
            'status': 'success',
            'message': 'Documento subido correctamente',
            'data': doc.to_dict()
        }), status_code

    @jwt_required()
    def download_document(self, document_id):
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({'status': 'error', 'message': 'Usuario no encontrado'}), 404

        doc, file_location, err, status_code = self.service.download_document(document_id, current_user)
        if err:
            return jsonify({'status': 'error', 'message': err}), status_code

        # Si file_location es una URL remota de AWS S3
        if file_location.startswith('http://') or file_location.startswith('https://'):
            return redirect(file_location)

        # Si file_location es una ruta local en disco
        return send_file(
            file_location,
            as_attachment=True,
            download_name=doc.original_filename,
            mimetype=doc.mime_type
        )

    @jwt_required()
    def delete_document(self, id):
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)

        _, error, status_code = self.service.delete_document(id, current_user)
        if error:
            return jsonify({'status': 'error', 'message': error}), status_code

        return jsonify({
            'status': 'success',
            'message': 'Documento eliminado correctamente'
        }), status_code
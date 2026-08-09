from flask import Blueprint
from src.modules.documents.document_controller import DocumentController

documents_bp = Blueprint('documents', __name__)
controller = DocumentController()

@documents_bp.route('/', methods=['GET'])
def get_documents():
    return controller.get_documents()

@documents_bp.route('/<int:id>', methods=['GET'])
def get_document_by_id(id):
    return controller.get_document_by_id(id)

@documents_bp.route('/upload', methods=['POST'])
def upload_document():
    return controller.upload_document()

@documents_bp.route('/<int:id>/download', methods=['GET'])
def download_document(id):
    return controller.download_document(id)

@documents_bp.route('/<int:id>', methods=['DELETE'])
def delete_document(id):
    return controller.delete_document(id)
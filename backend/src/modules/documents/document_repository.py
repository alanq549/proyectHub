from extensions.db import db
from src.models.document import Document


class DocumentRepository:

    @staticmethod
    def get_all(user_id=None, project_id=None, call_id=None):
        query = Document.query

        if user_id:
            query = query.filter_by(user_id=user_id)

        if project_id:
            query = query.filter_by(project_id=project_id)

        if call_id:
            query = query.filter_by(call_id=call_id)

        return query.order_by(Document.created_at.desc()).all()

    @staticmethod
    def get_by_id(document_id):
        return Document.query.get(document_id)

    @staticmethod
    def get_by_project_id(project_id):
        return DocumentRepository.get_all(
            project_id=project_id
        )

    @staticmethod
    def get_by_call_and_user(call_id, user_id):
        return DocumentRepository.get_all(
            call_id=call_id,
            user_id=user_id
        )

    @staticmethod
    def create(doc_data):
        doc = Document(
            filename=doc_data['filename'],
            original_filename=doc_data['original_filename'],
            file_path=doc_data['file_path'],
            mime_type=doc_data['mime_type'],
            file_size=doc_data['file_size'],
            status=doc_data.get('status', 'uploaded'),
            user_id=doc_data['user_id'],
            project_id=doc_data.get('project_id'),
            call_id=doc_data.get('call_id')
        )

        db.session.add(doc)
        db.session.commit()

        return doc

    @staticmethod
    def update_status(document, status):
        document.status = status
        db.session.commit()
        return document

    @staticmethod
    def delete(document):
        db.session.delete(document)
        db.session.commit()
        return True
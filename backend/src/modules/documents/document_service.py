# src/modules/documents/document_service.py
import os
from flask import current_app
from extensions.db import db
from src.modules.documents.document_repository import DocumentRepository
from src.services.storage_service import StorageService
from src.utils.logger import log_activity  # Importación del helper centralizado

class DocumentService:
    def __init__(self):
        self.repository = DocumentRepository()

    def get_documents(self, current_user, project_id=None, call_id=None):
        if current_user.role == 'admin':
            return self.repository.get_all(project_id=project_id, call_id=call_id)
        return self.repository.get_all(user_id=current_user.id, project_id=project_id, call_id=call_id)

    def get_document_by_id(self, document_id, current_user):
        doc = self.repository.get_by_id(document_id)
        if not doc:
            return None, "Documento no encontrado", 404

        if current_user.role != 'admin' and doc.user_id != current_user.id:
            return None, "No tienes permiso para acceder a este documento", 403

        return doc, None, 200

    def download_document(self, document_id, current_user):
        """Obtiene la información del documento y su ruta o URL de descarga."""
        doc, err, status_code = self.get_document_by_id(document_id, current_user)
        if err:
            return None, None, err, status_code

        try:
            # StorageService retorna la ruta física (Local) o la presigned URL (S3)
            file_location = StorageService.download_file(doc.file_path)
            return doc, file_location, None, 200
        except ValueError as e:
            return None, None, str(e), 404
        except Exception as e:
            current_app.logger.error(f"Error al obtener ruta del archivo: {str(e)}")
            return None, None, "Error al recuperar el archivo del servidor", 500

    def upload_document(self, file, current_user, project_id=None, call_id=None):
        if not file or file.filename == '':
            return None, "No se ha proporcionado un archivo válido", 400

        original_filename = file.filename

        # Calcular tamaño del archivo antes de subirlo
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)  # Resetear el puntero al inicio

        folder = f"projects/{project_id}" if project_id else "documents"

        try:
            stored_path = StorageService.upload_file(file, folder=folder)
        except ValueError as err:
            return None, str(err), 400
        except Exception as e:
            current_app.logger.error(f"Error al subir archivo: {str(e)}")
            return None, "Error al guardar el archivo en el servidor", 500

        unique_filename = os.path.basename(stored_path)
        mime_type = file.mimetype or 'application/octet-stream'

        doc_data = {
            'filename': unique_filename,
            'original_filename': original_filename,
            'file_path': stored_path,
            'mime_type': mime_type,
            'file_size': file_size,
            'user_id': current_user.id,
            'project_id': project_id,
            'call_id': call_id,
            'status': 'uploaded'
        }

        document = self.repository.create(doc_data)
        
        # Aseguramos que el ID esté disponible en la transacción
        db.session.flush()

        # Registrar en Historial usando el helper
        log_entity_type = 'Project' if project_id else 'Document'
        log_entity_id = project_id if project_id else document.id

        log_activity(
            user_id=current_user.id,
            action='DOCUMENT_UPLOADED',
            entity_type=log_entity_type,
            entity_id=log_entity_id,
            description=f"Subiste el documento '{document.original_filename}' exitosamente."
        )
        db.session.commit()

        return document, None, 201

    def delete_document(self, document_id, current_user):
        doc = self.repository.get_by_id(document_id)
        if not doc:
            return None, "Documento no encontrado", 404

        if current_user.role != 'admin' and doc.user_id != current_user.id:
            return None, "No tienes permiso para eliminar este documento", 403

        original_name = doc.original_filename
        file_path = doc.file_path

        self.repository.delete(doc)

        try:
            StorageService.delete_file(file_path)
        except Exception as e:
            current_app.logger.error(f"Error al eliminar archivo físico: {str(e)}")

        # Registrar en Historial usando el helper
        log_entity_type = 'Project' if doc.project_id else 'Document'
        log_entity_id = doc.project_id if doc.project_id else document_id

        log_activity(
            user_id=current_user.id,
            action='DOCUMENT_DELETED',
            entity_type=log_entity_type,
            entity_id=log_entity_id,
            description=f"Elimino el documento '{original_name}'."
        )
        db.session.commit()

        return True, None, 200
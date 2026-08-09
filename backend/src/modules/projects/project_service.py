from src.modules.projects.project_repository import ProjectRepository
from src.models.project import Project
from src.utils.logger import log_activity  # Usando tu helper centralizado
from extensions.db import db

class ProjectService:
    def __init__(self):
        self.repository = ProjectRepository()

    def get_projects(self, current_user, call_id=None, status=None):
        if current_user.role == 'admin':
            return self.repository.get_all(call_id=call_id, status=status)
        return self.repository.get_all(user_id=current_user.id, call_id=call_id, status=status)

    def get_project_by_id(self, project_id, current_user):
        project = self.repository.get_by_id(project_id)
        if not project:
            return None, "Proyecto no encontrado", 404

        if current_user.role != 'admin' and project.user_id != current_user.id:
            return None, "No tienes permiso para ver este proyecto", 403

        return project, None, 200

    def create_project(self, data, current_user):
        title = data.get('title')
        if not title or not title.strip():
            return None, "El título del proyecto es obligatorio", 400

        status = data.get('status', 'draft')
        if status not in Project.VALID_STATUSES:
            return None, f"Estado inválido. Opciones permitidas: {', '.join(Project.VALID_STATUSES)}", 400

        project_data = {
            'title': title.strip(),
            'description': data.get('description', '').strip() if data.get('description') else None,
            'status': status,
            'user_id': current_user.id,
            'call_id': data.get('call_id')
        }

        project = self.repository.create(project_data)
        
        # Aseguramos el id si el repositorio no hizo commit previo
        db.session.flush()

        # Usando tu helper para registrar en la bitácora
        log_activity(
            user_id=current_user.id,
            action='PROJECT_CREATED',
            entity_type='Project',
            entity_id=project.id,
            description=f"Proyecto '{project.title}' creado."
        )
        db.session.commit()

        return project, None, 201

    def update_project(self, project_id, data, current_user):
        project = self.repository.get_by_id(project_id)
        if not project:
            return None, "Proyecto no encontrado", 404

        if current_user.role != 'admin' and project.user_id != current_user.id:
            return None, "No tienes permiso para actualizar este proyecto", 403

        if 'status' in data and data['status'] not in Project.VALID_STATUSES:
            return None, f"Estado inválido. Opciones permitidas: {', '.join(Project.VALID_STATUSES)}", 400

        # Manejar el feedback si viene en los datos del request
        if 'feedback' in data:
            project.feedback = data.get('feedback')

        old_status = project.status
        updated_project = self.repository.update(project, data)
        new_status = updated_project.status

        # Mensajes dinámicos según el cambio de estado
        description_text = f"Proyecto '{updated_project.title}' actualizado."
        
        if old_status != new_status:
            if new_status == 'submitted':
                description_text = f"Tu proyecto '{updated_project.title}' fue enviado para revisión."
            elif new_status == 'approved':
                description_text = f"¡Felicidades! Tu proyecto '{updated_project.title}' ha sido aprobado."
            elif new_status == 'rejected':
                description_text = f"Lo sentimos, tu proyecto '{updated_project.title}' ha sido rechazado."
            elif new_status == 'draft':
                description_text = f"El proyecto '{updated_project.title}' regresó a modo borrador."

        # Opcional: Agregar el comentario a la descripción del log si se envió retroalimentación
        if data.get('feedback'):
            description_text += f" Comentario: \"{data.get('feedback')}\""

        log_activity(
            user_id=current_user.id,
            action='PROJECT_UPDATED',
            entity_type='Project',
            entity_id=updated_project.id,
            description=description_text
        )
        db.session.commit()

        return updated_project, None, 200

    def delete_project(self, project_id, current_user):
        project = self.repository.get_by_id(project_id)
        if not project:
            return None, "Proyecto no encontrado", 404

        if current_user.role != 'admin' and project.user_id != current_user.id:
            return None, "No tienes permiso para eliminar este proyecto", 403

        project_title = project.title
        self.repository.delete(project)

        log_activity(
            user_id=current_user.id,
            action='PROJECT_DELETED',
            entity_type='Project',
            entity_id=project_id,
            description=f"Proyecto '{project_title}' eliminado."
        )
        db.session.commit()

        return True, None, 200
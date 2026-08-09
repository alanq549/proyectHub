# src/modules/calls/call_service.py
from datetime import datetime, timezone
from extensions.db import db
from .call_repository import CallRepository
from src.modules.projects.project_repository import ProjectRepository
from src.modules.documents.document_repository import DocumentRepository
from src.modules.history.history_repository import HistoryRepository
from src.utils.logger import log_activity  # Helper centralizado

class CallService:
    @staticmethod
    def _parse_date(date_str):
        """
        Parsea un string ISO a datetime y asegura que esté estrictamente en UTC.
        """
        if isinstance(date_str, datetime):
            parsed_dt = date_str
        else:
            try:
                parsed_dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            except (ValueError, TypeError):
                raise ValueError(f"Formato de fecha inválido: {date_str}")

        if parsed_dt.tzinfo is not None:
            return parsed_dt.astimezone(timezone.utc)
        return parsed_dt.replace(tzinfo=timezone.utc)

    @classmethod
    def get_all_calls(cls):
        calls = CallRepository.get_all()
        return [call.to_dict() for call in calls]

    @classmethod
    def get_call_by_id(cls, call_id):
        call = CallRepository.get_by_id(call_id)
        if not call:
            return None, "Convocatoria no encontrada"
        return call.to_dict(), None

    @classmethod
    def create_call(cls, data, current_user_id=None):
        if (
            not data.get("title")
            or not data.get("start_date")
            or not data.get("end_date")
        ):
            return None, "Los campos title, start_date y end_date son obligatorios"

        try:
            start_date = cls._parse_date(data["start_date"])
            end_date = cls._parse_date(data["end_date"])
        except ValueError as e:
            return None, str(e)

        if end_date < start_date:
            return (
                None,
                "La fecha de fin (end_date) debe ser posterior o igual a la fecha de inicio (start_date)",
            )

        payload = {
            "title": data["title"],
            "description": data.get("description"),
            "start_date": start_date,
            "end_date": end_date,
            "is_active": data.get("is_active", True),
        }

        call = CallRepository.create(payload)
        db.session.flush()

        if current_user_id:
            log_activity(
                user_id=current_user_id,
                action='CALL_CREATED',
                entity_type='Call',
                entity_id=call.id,
                description=f"Convocatoria '{call.title}' creada exitosamente."
            )
            db.session.commit()

        return call.to_dict(), None

    @classmethod
    def update_call(cls, call_id, data, current_user_id=None):
        call = CallRepository.get_by_id(call_id)
        if not call:
            return None, "Convocatoria no encontrada"

        try:
            start_date = (
                cls._parse_date(data["start_date"])
                if "start_date" in data
                else cls._parse_date(call.start_date)
            )
            end_date = (
                cls._parse_date(data["end_date"])
                if "end_date" in data
                else cls._parse_date(call.end_date)
            )
        except ValueError as e:
            return None, str(e)

        if end_date < start_date:
            return (
                None,
                "La fecha de fin debe ser posterior o igual a la fecha de inicio",
            )

        payload = dict(data)
        if "start_date" in data:
            payload["start_date"] = start_date
        if "end_date" in data:
            payload["end_date"] = end_date

        updated_call = CallRepository.update(call, payload)

        if current_user_id:
            log_activity(
                user_id=current_user_id,
                action='CALL_UPDATED',
                entity_type='Call',
                entity_id=updated_call.id,
                description=f"Convocatoria '{updated_call.title}' actualizada."
            )
            db.session.commit()

        return updated_call.to_dict(), None

    @classmethod
    def delete_call(cls, call_id, current_user_id=None):
        call = CallRepository.get_by_id(call_id)
        if not call:
            return False, "Convocatoria no encontrada"
        
        call_title = call.title
        CallRepository.delete(call)

        if current_user_id:
            log_activity(
                user_id=current_user_id,
                action='CALL_DELETED',
                entity_type='Call',
                entity_id=call_id,
                description=f"Convocatoria '{call_title}' eliminada."
            )
            db.session.commit()

        return True, None

    @classmethod
    def join_call(cls, call_id, user_id):
        call = CallRepository.get_by_id(call_id)
        if not call:
            return None, "Convocatoria no encontrada", 404

        existing = CallRepository.get_participant(call_id, user_id)
        if existing:
            return existing.to_dict(), "Ya estás inscrito en esta convocatoria", 400

        participant = CallRepository.register_participant(call_id, user_id)
        db.session.flush()

        log_activity(
            user_id=user_id,
            action='CALL_JOINED',
            entity_type='Call',
            entity_id=call_id,
            description=f"El usuario se inscribió a la convocatoria '{call.title}'."
        )
        db.session.commit()

        return participant.to_dict(), None, 201

    @classmethod
    def add_requirement(cls, call_id, data, current_user_id=None):
        if not data.get("title"):
            return None, "El título del requisito es obligatorio"
        req = CallRepository.add_requirement(
            call_id=call_id,
            title=data["title"],
            description=data.get("description"),
            is_required=data.get("is_required", True)
        )
        db.session.flush()

        if current_user_id:
            log_activity(
                user_id=current_user_id,
                action='REQUIREMENT_ADDED',
                entity_type='Requirement',
                entity_id=req.id,
                description=f"Requisito '{req.title}' añadido a la convocatoria."
            )
            db.session.commit()

        return req.to_dict(), None

    @classmethod
    def update_application_status(cls, participant_id, status, current_user_id=None):
        valid_statuses = ["REGISTERED", "SUBMITTED", "IN_REVIEW", "APPROVED", "REJECTED"]
        if status not in valid_statuses:
            return None, f"Estado inválido. Debe ser uno de: {valid_statuses}"

        updated = CallRepository.update_participant_status(participant_id, status)
        if not updated:
            return None, "Participante no encontrado"
        
        db.session.flush()

        if current_user_id:
            log_activity(
                user_id=current_user_id,
                action='APPLICATION_STATUS_UPDATED',
                entity_type='Participant',
                entity_id=updated.id,
                description=f"Estatus de la postulación actualizado a: {status}."
            )
            db.session.commit()

        return updated.to_dict(), None

    @classmethod
    def get_workspace(cls, call_id, user):
        call = CallRepository.get_by_id(call_id)
        if not call:
            return None, "Convocatoria no encontrada", 404

        user_id = user.id if hasattr(user, 'id') else user
        requirements = [r.to_dict() for r in call.requirements]

        # VISTA PARA ADMINISTRADOR: Ve el listado global de postulantes
        if user.role == 'admin':
            participants_raw = CallRepository.get_all_participants(call_id)
            participants_data = []
            for p in participants_raw:
                p_dict = p.to_dict()
                if p.user:
                    p_dict['user_email'] = p.user.email
                    p_dict['user_name'] = getattr(p.user, 'name', p.user.email)
                participants_data.append(p_dict)

            return {
                "call": call.to_dict(),
                "requirements": requirements,
                "participants": participants_data,
                "is_admin_view": True
            }, None, 200

        # VISTA PARA USUARIO POSTULANTE: Ve su propio avance
        participant = CallRepository.get_participant(call_id, user_id)
        project_obj = ProjectRepository.get_by_call_and_user(call_id, user_id)
        project_dict = project_obj.to_dict() if project_obj else None

        documents = []
        if project_obj:
            docs = DocumentRepository.get_by_project_id(project_obj.id)
            documents = [doc.to_dict() for doc in docs]

        tracking = []
        if project_obj:
            logs = HistoryRepository.get_by_entity("project", project_obj.id)
            tracking = [log.to_dict() for log in logs]

        req_count = len(requirements)
        uploaded_count = len(documents)
        progress = int((uploaded_count / req_count) * 100) if req_count > 0 else 0

        return {
            "call": call.to_dict(),
            "participant_status": participant.status if participant else "NOT_REGISTERED",
            "requirements": requirements,
            "project": project_dict,
            "documents": documents,
            "tracking": tracking,
            "stats": {
                "documents_uploaded": uploaded_count,
                "progress": min(progress, 100),
            },
            "is_admin_view": False
        }, None, 200
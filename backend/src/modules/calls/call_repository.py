# src/modules/calls/call_repository.py
from extensions.db import db
from src.models.call import Call
from src.models.call_requirement import CallRequirement
from src.models.call_participant import CallParticipant
from sqlalchemy.orm import subqueryload, joinedload  # <-- Agregado joinedload


class CallRepository:
    # --- MÉTODOS EXISTENTES DE CALLS ---
    @staticmethod
    def get_all():
        return Call.query.options(
            subqueryload(Call.participants),
            subqueryload(Call.requirements)
        ).order_by(Call.created_at.desc()).all()

    @staticmethod
    def get_by_id(call_id):
        return (
            Call.query.options(joinedload(Call.requirements))
            .filter_by(id=call_id)
            .first()
        )

    @staticmethod
    def create(data):
        call = Call(
            title=data["title"],
            description=data.get("description"),
            start_date=data["start_date"],
            end_date=data["end_date"],
            is_active=data.get("is_active", True),
        )
        db.session.add(call)
        db.session.commit()
        return call

    @staticmethod
    def update(call, data):
        for key, value in data.items():
            if hasattr(call, key):
                setattr(call, key, value)
        db.session.commit()
        return call

    @staticmethod
    def delete(call):
        db.session.delete(call)
        db.session.commit()

    # --- REQUISITOS (CallRequirements) ---
    @staticmethod
    def add_requirement(call_id, title, description=None, is_required=True):
        req = CallRequirement(
            call_id=call_id,
            title=title,
            description=description,
            is_required=is_required,
        )
        db.session.add(req)
        db.session.commit()
        return req

    @staticmethod
    def get_requirements(call_id):
        return CallRequirement.query.filter_by(call_id=call_id).all()

    # --- PARTICIPANTES (CallParticipants) ---
    @staticmethod
    def get_participant(call_id, user_id):
        return CallParticipant.query.filter_by(call_id=call_id, user_id=user_id).first()

    @staticmethod
    def register_participant(call_id, user_id):
        participant = CallParticipant(
            call_id=call_id, user_id=user_id, status="REGISTERED"
        )
        db.session.add(participant)
        db.session.commit()
        return participant

    @staticmethod
    def get_all_participants(call_id):
        return CallParticipant.query.filter_by(call_id=call_id).all()

    @staticmethod
    def update_participant_status(participant_id, new_status):
        part = CallParticipant.query.get(participant_id)
        if part:
            part.status = new_status
            db.session.commit()
        return part
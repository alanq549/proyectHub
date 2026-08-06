# src/modules/calls/call_repository.py

from extensions.db import db
from src.models.call import Call  # Cambiado de 'from .call import Call'

class CallRepository:
    @staticmethod
    def get_all():
        return Call.query.order_by(Call.created_at.desc()).all()

    @staticmethod
    def get_by_id(call_id):
        return Call.query.get(call_id)

    @staticmethod
    def create(data):
        call = Call(
            title=data['title'],
            description=data.get('description'),
            start_date=data['start_date'],
            end_date=data['end_date'],
            is_active=data.get('is_active', True)
        )
        db.session.add(call)
        db.session.commit()
        return call

    @staticmethod
    def update(call, data):
        if 'title' in data:
            call.title = data['title']
        if 'description' in data:
            call.description = data['description']
        if 'start_date' in data:
            call.start_date = data['start_date']
        if 'end_date' in data:
            call.end_date = data['end_date']
        if 'is_active' in data:
            call.is_active = data['is_active']
        
        db.session.commit()
        return call

    @staticmethod
    def delete(call):
        db.session.delete(call)
        db.session.commit()
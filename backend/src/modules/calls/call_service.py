# src/modules/calls/call_service.py
from datetime import datetime, timezone
from .call_repository import CallRepository

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
                parsed_dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            except (ValueError, TypeError):
                raise ValueError(f"Formato de fecha inválido: {date_str}")

        # Si el datetime ya tiene zona horaria, se convierte a UTC.
        # Si es naive (sin offset), se le asigna UTC explícitamente.
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
    def create_call(cls, data):
        if not data.get('title') or not data.get('start_date') or not data.get('end_date'):
            return None, "Los campos title, start_date y end_date son obligatorios"

        try:
            start_date = cls._parse_date(data['start_date'])
            end_date = cls._parse_date(data['end_date'])
        except ValueError as e:
            return None, str(e)

        if end_date < start_date:
            return None, "La fecha de fin (end_date) debe ser posterior o igual a la fecha de inicio (start_date)"

        payload = {
            'title': data['title'],
            'description': data.get('description'),
            'start_date': start_date,
            'end_date': end_date,
            'is_active': data.get('is_active', True)
        }

        call = CallRepository.create(payload)
        return call.to_dict(), None

    @classmethod
    def update_call(cls, call_id, data):
        call = CallRepository.get_by_id(call_id)
        if not call:
            return None, "Convocatoria no encontrada"

        try:
            # Si se actualiza solo una de las fechas, nos aseguramos de parsear/normalizar
            start_date = cls._parse_date(data['start_date']) if 'start_date' in data else cls._parse_date(call.start_date)
            end_date = cls._parse_date(data['end_date']) if 'end_date' in data else cls._parse_date(call.end_date)
        except ValueError as e:
            return None, str(e)

        if end_date < start_date:
            return None, "La fecha de fin debe ser posterior o igual a la fecha de inicio"

        payload = dict(data)
        if 'start_date' in data: 
            payload['start_date'] = start_date
        if 'end_date' in data: 
            payload['end_date'] = end_date

        updated_call = CallRepository.update(call, payload)
        return updated_call.to_dict(), None

    @classmethod
    def delete_call(cls, call_id):
        call = CallRepository.get_by_id(call_id)
        if not call:
            return False, "Convocatoria no encontrada"
        CallRepository.delete(call)
        return True, None
# src/modules/history/history_service.py
from src.modules.history.history_repository import HistoryRepository

class HistoryService:
    def __init__(self):
        self.repository = HistoryRepository()

    def get_history(self, current_user, entity_type=None, entity_id=None, limit=50):
        # Admins ven todo el historial; usuarios normales ven solo sus propias acciones
        if current_user.role == 'admin':
            return self.repository.get_all(
                entity_type=entity_type, 
                entity_id=entity_id, 
                limit=limit
            )
        
        return self.repository.get_all(
            user_id=current_user.id, 
            entity_type=entity_type, 
            entity_id=entity_id, 
            limit=limit
        )
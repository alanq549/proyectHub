# src/modules/history/history_repository.py
from extensions.db import db
from src.models.activity_log import ActivityLog


class HistoryRepository:

    @staticmethod
    def get_all(
        user_id=None,
        entity_type=None,
        entity_id=None,
        limit=50
    ):
        query = ActivityLog.query

        if user_id:
            query = query.filter_by(user_id=user_id)

        if entity_type:
            query = query.filter_by(entity_type=entity_type)

        if entity_id:
            query = query.filter_by(entity_id=entity_id)

        return (
            query
            .order_by(ActivityLog.created_at.desc())
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_by_id(log_id):
        return ActivityLog.query.get(log_id)

    @staticmethod
    def get_by_entity(entity_type, entity_id):
        return HistoryRepository.get_all(
            entity_type=entity_type,
            entity_id=entity_id
        )
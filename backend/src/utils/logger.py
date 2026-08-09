# app/utils/logger.py
from extensions.db import db
from src.models.activity_log import ActivityLog


def log_activity(
    user_id: int,
    action: str,
    entity_type: str,
    entity_id: int,
    description: str
):
    activity = ActivityLog(
        user_id=user_id,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        description=description
    )

    db.session.add(activity)
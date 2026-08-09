#src/models/call_participant.py
from datetime import datetime, timezone
from extensions.db import db


class CallParticipant(db.Model):
    __tablename__ = "call_participants"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    call_id = db.Column(
        db.Integer,
        db.ForeignKey("calls.id"),
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    status = db.Column(
        db.String(50),
        default="REGISTERED"
    )

    joined_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    call = db.relationship(
        "Call",
        back_populates="participants"
    )

    user = db.relationship(
        "User"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "call_id": self.call_id,
            "user_id": self.user_id,
            "status": self.status
        }
# src/models/call_requirement.py
from datetime import datetime, timezone
from extensions.db import db


class CallRequirement(db.Model):
    __tablename__ = "call_requirements"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    call_id = db.Column(
        db.Integer,
        db.ForeignKey("calls.id"),
        nullable=False
    )

    title = db.Column(
        db.String(150),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    is_required = db.Column(
        db.Boolean,
        default=True
    )

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    call = db.relationship(
        "Call",
        back_populates="requirements"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "call_id": self.call_id,
            "title": self.title,
            "description": self.description,
            "is_required": self.is_required
        }
# src/models/call.py
from datetime import datetime, timezone
from extensions.db import db


class Call(db.Model):
    __tablename__ = "calls"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    requirements = db.relationship(
        "CallRequirement", back_populates="call", lazy=True, cascade="all, delete"
    )

    participants = db.relationship(
        "CallParticipant", back_populates="call", lazy=True, cascade="all, delete"
    )

    def to_dict(self, include_requirements=True, include_counts=True):  # <-- Agregado include_counts
        data = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "participants_count": len(self.participants) if include_counts else 0,
            "requirements_count": len(self.requirements) if include_counts else 0,
        }

        if include_requirements:
            data["requirements"] = [req.to_dict() for req in self.requirements]

        return data
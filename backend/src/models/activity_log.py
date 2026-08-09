from datetime import datetime
from extensions.db import db

class ActivityLog(db.Model):
    __tablename__ = 'activity_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    action = db.Column(db.String(100), nullable=False)       # ej. 'PROJECT_CREATED', 'DOCUMENT_UPLOADED'
    entity_type = db.Column(db.String(50), nullable=False)   # ej. 'Project', 'Document', 'Call'
    entity_id = db.Column(db.Integer, nullable=True)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship('User', backref=db.backref('activity_logs', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user_name': f"{self.user.first_name} {self.user.last_name}" if self.user and (self.user.first_name or self.user.last_name) else (self.user.username if self.user else "Sistema"),
            'action': self.action,
            'entity_type': self.entity_type,
            'entity_id': self.entity_id,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
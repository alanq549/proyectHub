from datetime import datetime
from extensions.db import db

class Project(db.Model):
    __tablename__ = 'projects'

    VALID_STATUSES = {'draft', 'submitted', 'in_review', 'approved', 'rejected'}

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), default='draft', nullable=False)
    feedback = db.Column(db.Text, nullable=True)  # <-- Asegúrate de tener este campo
    
    # Llaves foráneas
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    call_id = db.Column(db.Integer, db.ForeignKey('calls.id', ondelete='SET NULL'), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relaciones
    user = db.relationship('User', backref=db.backref('projects', lazy=True, cascade='all, delete-orphan'))
    call = db.relationship('Call', backref=db.backref('projects', lazy=True))
    documents = db.relationship('Document', backref='project', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'feedback': self.feedback,
            'user_id': self.user_id,
            'call_id': self.call_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'call_title': self.call.title if self.call else None
        }
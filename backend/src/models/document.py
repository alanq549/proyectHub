from datetime import datetime
from extensions.db import db

class Document(db.Model):
    __tablename__ = 'documents'

    VALID_STATUSES = {'uploaded', 'verified', 'rejected'}

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)          # Nombre físico/almacenado
    original_filename = db.Column(db.String(255), nullable=False) # Nombre original subido por el usuario
    file_path = db.Column(db.String(500), nullable=False)         # Ruta local o clave S3
    mime_type = db.Column(db.String(100), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)             # En bytes
    status = db.Column(db.String(50), default='uploaded', nullable=False)

    # Llaves foráneas
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id', ondelete='SET NULL'), nullable=True)
    call_id = db.Column(db.Integer, db.ForeignKey('calls.id', ondelete='SET NULL'), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relaciones
    user = db.relationship('User', backref=db.backref('documents', lazy=True, cascade='all, delete-orphan'))
    call = db.relationship('Call', backref=db.backref('documents', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'original_filename': self.original_filename,
            'file_path': self.file_path,
            'mime_type': self.mime_type,
            'file_size': self.file_size,
            'status': self.status,
            'user_id': self.user_id,
            'project_id': self.project_id,
            'call_id': self.call_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
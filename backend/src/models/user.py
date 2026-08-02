from extensions.db import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone

DEFAULT_PROFILE_PICTURE_URL = '/static/defaults/icon_default.png'

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(80), nullable=True)
    last_name = db.Column(db.String(80), nullable=True)
    role = db.Column(db.String(20), default='user', nullable=False)
    profile_picture_url = db.Column(db.String(255), default=DEFAULT_PROFILE_PICTURE_URL, nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'role': self.role,
            'profile_picture_url': self.profile_picture_url or DEFAULT_PROFILE_PICTURE_URL,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
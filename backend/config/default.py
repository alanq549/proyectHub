import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'a_very_secret_key_that_should_be_changed')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://projecthub_user:projecthub_password@localhost:5432/projecthub_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'super-secret-jwt-key')
    CORS_HEADERS = 'Content-Type'

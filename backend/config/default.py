import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'a_very_secret_key_that_should_be_changed')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://projecthub_user:projecthub_password@localhost:5432/projecthub_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'super-secret-jwt-key')
    CORS_HEADERS = 'Content-Type'
    # AWS Configuration
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')
    S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME', 'your-s3-bucket-name')

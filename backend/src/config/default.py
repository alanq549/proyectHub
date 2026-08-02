import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    CORS_HEADERS = 'Content-Type'

    STORAGE_PROVIDER = os.getenv('STORAGE_PROVIDER', 'local')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    BOOTSTRAP_FIRST_USER_AS_ADMIN = os.getenv('BOOTSTRAP_FIRST_USER_AS_ADMIN', 'true').lower() == 'true'

    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
    S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME', 'your-s3-bucket-name')

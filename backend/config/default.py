import os

class Config:
# Si no existe DATABASE_URL en el .env, no asignamos un usuario/password real por defecto
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

#JWT Configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    CORS_HEADERS = 'Content-Type'
# Opcional: Configurar tiempo de expiración
    # JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    # JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

# AWS Configuration
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
    S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME', 'your-s3-bucket-name')

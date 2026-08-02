import os

API_BASE_URL = os.getenv('PROJECTHUB_API_URL', 'http://localhost:5000/api/v1')

DEFAULT_ADMIN = {
    'username': os.getenv('PROJECTHUB_ADMIN_USERNAME', 'admin'),
    'email': os.getenv('PROJECTHUB_ADMIN_EMAIL', 'admin@projecthub.local'),
    'password': os.getenv('PROJECTHUB_ADMIN_PASSWORD', 'Admin1234!'),
    'first_name': os.getenv('PROJECTHUB_ADMIN_FIRSTNAME', 'System'),
    'last_name': os.getenv('PROJECTHUB_ADMIN_LASTNAME', 'Administrator'),
}

DEFAULT_PROFILE_PICTURE_URL = '/static/defaults/icon_default.png'

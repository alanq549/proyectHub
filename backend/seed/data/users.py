import os

SEED_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKEND_DIR = os.path.dirname(SEED_DIR)
PROFILES_DIR = os.path.join(BACKEND_DIR, 'src', 'static', 'uploads', 'profiles')

DEFAULT_USERS = [
    {
        'username': 'ana.lopez',
        'email': 'ana.lopez@projecthub.local',
        'password': 'Ana1234!',
        'first_name': 'Ana',
        'last_name': 'López',
        'role': 'user',
        'profile_picture': os.path.join(PROFILES_DIR, '113d026de5a94282b22d323299ef79dd_holland_march_holding_blahaj.jpg'),
    },
    {
        'username': 'carlos.gomez',
        'email': 'carlos.gomez@projecthub.local',
        'password': 'Carlos1234!',
        'first_name': 'Carlos',
        'last_name': 'Gómez',
        'role': 'user',
        'profile_picture': os.path.join(PROFILES_DIR, '30766a8eb57549869c8f350077ea50b4_img2.jpg'),
    },
    {
        'username': 'maria.ramirez',
        'email': 'maria.ramirez@projecthub.local',
        'password': 'Maria1234!',
        'first_name': 'María',
        'last_name': 'Ramírez',
        'role': 'user',
        'profile_picture': os.path.join(PROFILES_DIR, '71b586721de64b0a8484977b9905d29f_descarga.jpg'),
    },
    {
        'username': 'pedro.martinez',
        'email': 'pedro.martinez@projecthub.local',
        'password': 'Pedro1234!',
        'first_name': 'Pedro',
        'last_name': 'Martínez',
        'role': 'user',
        'profile_picture': os.path.join(PROFILES_DIR, 'a98c5e1c1cbe499885745b88d314091b_imgcdm.jpg'),
    },
    {
        'username': 'laura.torres',
        'email': 'laura.torres@projecthub.local',
        'password': 'Laura1234!',
        'first_name': 'Laura',
        'last_name': 'Torres',
        'role': 'user',
        'profile_picture': os.path.join(PROFILES_DIR, 'c0fc1fd102174b6684fbc6cc51e9fa0f_holland_march_holding_blahaj.jpg'),
    },
]

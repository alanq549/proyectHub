# src/lib/auth.py
from ..lib.http_client import request
from ..config import DEFAULT_ADMIN


def login(credentials):
    res = request('POST', '/login', {
        'body': {
            'email': credentials['email'],
            'password': credentials['password'],
        }
    })
    if res['status'] == 200:
        json_body = res.get('json') or {}
        if json_body.get('access_token'):
            return {
                'token': json_body['access_token'],
                'refresh_token': json_body.get('refresh_token'),
                'user': json_body.get('user'),
            }
    return None


def register_public_user(payload):
    return request('POST', '/register', {'body': payload})


def make_first_admin_via_register():
    res = register_public_user({
        'username': DEFAULT_ADMIN['username'],
        'email': DEFAULT_ADMIN['email'],
        'password': DEFAULT_ADMIN['password'],
        'first_name': DEFAULT_ADMIN['first_name'],
        'last_name': DEFAULT_ADMIN['last_name'],
    })
    if res['status'] not in (201, 400):
        raise RuntimeError(
            f'Registro admin falló status={res["status"]}: {res["json"]}'
        )
    fresh = login(DEFAULT_ADMIN)
    if not fresh or not fresh.get('token'):
        raise RuntimeError('No se pudo iniciar sesión con el admin recién creado')
    return fresh


def find_user_by_email(token, email):
    res = request('GET', '/users', {'token': token})
    if res['status'] != 200:
        return None
    body = res.get('json')
    if not isinstance(body, list):
        return None
    for u in body:
        if isinstance(u, dict) and str(u.get('email', '')).lower() == email.lower():
            return u
    return None


def ensure_admin():
    admin_login = login(DEFAULT_ADMIN)

    if admin_login and admin_login.get('token'):
        me = request('GET', '/me', {'token': admin_login['token']})
        user = me.get('json') or {}
        if user.get('role') == 'admin':
            return {
                'token': admin_login['token'],
                'user': user,
                'created': False,
            }

    fresh_admin = make_first_admin_via_register()
    me = request('GET', '/me', {'token': fresh_admin['token']})
    user = me.get('json') or {}
    if user.get('role') != 'admin':
        raise RuntimeError(
            'El primer usuario registrado debió recibir role=admin gracias al '
            'BOOTSTRAP_FIRST_USER_AS_ADMIN. Actualmente role='
            f'{user.get("role")}. Revisa la variable o crea el admin inicial '
            'directamente en la BD antes de ejecutar el seed.'
        )
    return {
        'token': fresh_admin['token'],
        'user': user,
        'created': True,
    }

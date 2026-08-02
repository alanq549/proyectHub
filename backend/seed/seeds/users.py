from ..lib.http_client import request, expect
from ..data.users import DEFAULT_USERS

DEFAULT_PROFILE_PICTURE_URL = '/static/defaults/icon_default.png'


def is_default_profile(url):
    if not url:
        return True
    return url == DEFAULT_PROFILE_PICTURE_URL


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


def create_user_by_admin(admin_token, payload):
    return request('POST', '/users', {
        'token': admin_token,
        'body': {
            'username': payload['username'],
            'email': payload['email'],
            'password': payload['password'],
            'first_name': payload.get('first_name'),
            'last_name': payload.get('last_name'),
            'role': payload.get('role', 'user'),
        }
    })


def update_user_by_admin(admin_token, user_id, body):
    return request('PUT', f'/users/{user_id}', {
        'token': admin_token,
        'body': body,
    })


def seed_users(admin_token):
    created = []
    skipped = []

    for u in DEFAULT_USERS:
        existing = find_user_by_email(admin_token, u['email'])
        if existing:
            user_id = existing.get('id')
            final_user = existing

            needs_update = (
                existing.get('role') != (u.get('role') or 'user')
                or existing.get('first_name') != u.get('first_name')
                or existing.get('last_name') != u.get('last_name')
            )
            updated_ok = False
            if needs_update and user_id:
                updated = update_user_by_admin(admin_token, user_id, {
                    'first_name': u.get('first_name'),
                    'last_name': u.get('last_name'),
                    'role': u.get('role', 'user'),
                })
                if updated['status'] == 200:
                    final_user = updated.get('json', {}).get('user') or final_user
                    updated_ok = True
            skipped.append({
                'email': u['email'],
                'id': final_user.get('id'),
                'updated': updated_ok,
            })
            continue

        res = create_user_by_admin(admin_token, u)
        if res['status'] != 201:
            raise RuntimeError(
                f'No se pudo crear usuario {u["email"]} status={res["status"]}: {res["json"]}'
            )
        user = (res.get('json') or {}).get('user') or {}
        if not is_default_profile(user.get('profile_picture_url')):
            raise RuntimeError(
                f'{u["email"]} debió nacer con avatar default, obtuvo: '
                f'{user.get("profile_picture_url")}'
            )
        created.append({
            'id': user.get('id'),
            'email': user.get('email'),
            'username': user.get('username'),
            'role': user.get('role'),
            'profile_picture_url': user.get('profile_picture_url'),
        })

    list_res = expect(
        200,
        request('GET', '/users', {'token': admin_token}),
        'Listar usuarios al final del seed',
    )
    users = list_res.get('json') or []

    return {
        'created': created,
        'skipped': skipped,
        'total': len(users) if isinstance(users, list) else None,
    }

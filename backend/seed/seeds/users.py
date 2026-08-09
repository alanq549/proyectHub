import os
import mimetypes

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


def create_user_by_admin(admin_token, payload, file_payload=None):
    opts = {
        'token': admin_token,
        'form': {
            'username': payload['username'],
            'email': payload['email'],
            'password': payload['password'],
            'first_name': payload.get('first_name'),
            'last_name': payload.get('last_name'),
            'role': payload.get('role', 'user'),
        }
    }
    if file_payload:
        opts['file'] = file_payload
    return request('POST', '/users', opts)


def update_user_with_file(admin_token, user_id, body, file_payload=None):
    opts = {
        'token': admin_token,
        'form': body,
    }
    if file_payload:
        opts['file'] = file_payload
    return request('PUT', f'/users/{user_id}', opts)


def _load_file(file_path):
    if not file_path or not os.path.isfile(file_path):
        return None
    try:
        with open(file_path, 'rb') as fh:
            data = fh.read()
        fname = os.path.basename(file_path)
        mtype, _ = mimetypes.guess_type(file_path)
        return {
            'name': fname,
            'bytes': data,
            'content_type': mtype or 'application/octet-stream',
        }
    except OSError:
        return None


def seed_users(admin_token):
    created = []
    skipped = []
    users = []

    for u in DEFAULT_USERS:
        existing = find_user_by_email(admin_token, u['email'])
        file_payload = _load_file(u.get('profile_picture'))

        if existing:
            user_id = existing.get('id')
            final_user = existing

            needs_update = (
                existing.get('role') != (u.get('role') or 'user')
                or existing.get('first_name') != u.get('first_name')
                or existing.get('last_name') != u.get('last_name')
                or (file_payload and is_default_profile(existing.get('profile_picture_url')))
            )
            updated_ok = False
            if needs_update and user_id:
                update_body = {
                    'first_name': u.get('first_name'),
                    'last_name': u.get('last_name'),
                    'role': u.get('role', 'user'),
                }
                updated = update_user_with_file(
                    admin_token, user_id, update_body, file_payload=file_payload
                )
                if updated['status'] == 200:
                    final_user = updated.get('json', {}).get('user') or final_user
                    updated_ok = True
            skipped.append({
                'email': u['email'],
                'id': final_user.get('id'),
                'updated': updated_ok,
            })
            if final_user:
                users.append(final_user)
            continue

        res = create_user_by_admin(admin_token, u, file_payload=file_payload)
        if res['status'] != 201:
            raise RuntimeError(
                f'No se pudo crear usuario {u["email"]} status={res["status"]}: {res["json"]}'
            )
        user = (res.get('json') or {}).get('user') or {}
        created.append({
            'id': user.get('id'),
            'email': user.get('email'),
            'username': user.get('username'),
            'role': user.get('role'),
            'profile_picture_url': user.get('profile_picture_url'),
        })
        users.append(user)

    list_res = expect(
        200,
        request('GET', '/users', {'token': admin_token}),
        'Listar usuarios al final del seed',
    )
    all_users = list_res.get('json') or []

    return {
        'created': created,
        'skipped': skipped,
        'total': len(all_users) if isinstance(all_users, list) else None,
        'users': users if users else (all_users if isinstance(all_users, list) else []),
    }

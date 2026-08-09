from ..lib.http_client import request, expect
from ..data.calls import DEFAULT_CALLS
from ..lib.auth import login
from ..config import DEFAULT_ADMIN


def _find_call_by_title(admin_token, title):
    res = request('GET', '/calls', {'token': admin_token})
    if res['status'] != 200:
        return None
    body = res.get('json') or {}
    calls = body.get('data') if isinstance(body, dict) else body
    if not isinstance(calls, list):
        return None
    for c in calls:
        if isinstance(c, dict) and c.get('title') == title:
            return c
    return None


def _find_participant(admin_token, call_id, user_id):
    res = request('GET', f'/calls/{call_id}', {'token': admin_token})
    if res['status'] != 200:
        return None
    data = (res.get('json') or {}).get('data') or {}
    participants_count = data.get('participants_count', 0)
    if participants_count == 0:
        return None
    return True


def _login_as_user(user_email, password):
    res = request('POST', '/login', {
        'body': {
            'email': user_email,
            'password': password,
        }
    })
    if res['status'] == 200:
        body = res.get('json') or {}
        return body.get('access_token')
    return None


def seed_calls(admin_token, users):
    created_calls = []
    skipped_calls = []
    created_requirements = []
    created_participants = []

    for idx, call_data in enumerate(DEFAULT_CALLS):
        requirements = call_data.pop('requirements', [])
        existing = _find_call_by_title(admin_token, call_data['title'])

        if existing:
            call_id = existing.get('id')
            skipped_calls.append({
                'id': call_id,
                'title': call_data['title'],
            })
        else:
            create_res = expect(
                201,
                request('POST', '/calls', {
                    'token': admin_token,
                    'body': call_data,
                }),
                f'Crear convocatoria {call_data["title"]}'
            )
            call_obj = (create_res.get('json') or {}).get('data') or {}
            call_id = call_obj.get('id')
            created_calls.append({
                'id': call_id,
                'title': call_obj.get('title'),
            })

        req_index = 0
        for req in requirements:
            req_index += 1
            req_res = request('POST', f'/calls/{call_id}/requirements', {
                'token': admin_token,
                'body': req,
            })
            if req_res['status'] == 201:
                req_obj = (req_res.get('json') or {}).get('data') or {}
                created_requirements.append({
                    'id': req_obj.get('id'),
                    'call_id': call_id,
                    'title': req.get('title'),
                })
            elif req_res['status'] in (400, 409):
                created_requirements.append({
                    'id': None,
                    'call_id': call_id,
                    'title': req.get('title'),
                    'skipped': True,
                })
            else:
                raise RuntimeError(
                    f'No se pudo crear requisito {req.get("title")} para call_id={call_id} '
                    f'status={req_res["status"]}: {req_res.get("json")}'
                )
            if req_index >= 5:
                break

        if idx < len(users):
            user = users[idx] if isinstance(users[idx], dict) else {'email': None, 'password': None}
            user_email = user.get('email')
            user_password = None
            for default_u in [DEFAULT_ADMIN]:
                if default_u.get('email') == user_email:
                    user_password = default_u.get('password')
                    break

            from ..data.users import DEFAULT_USERS
            for du in DEFAULT_USERS:
                if du.get('email') == user_email:
                    user_password = du.get('password')
                    break

            if user_email and user_password:
                user_token = _login_as_user(user_email, user_password)
                if user_token:
                    participant_exists = _find_participant(admin_token, call_id, user.get('id'))
                    if not participant_exists:
                        join_res = request('POST', f'/calls/{call_id}/join', {
                            'token': user_token,
                        })
                        if join_res['status'] in (201, 400):
                            participant_obj = (join_res.get('json') or {}).get('data') or {}
                            created_participants.append({
                                'id': participant_obj.get('id') if participant_obj else None,
                                'call_id': call_id,
                                'user_id': user.get('id'),
                                'user_email': user_email,
                                'status': 'REGISTERED' if join_res['status'] == 201 else 'EXISTE',
                            })
                        else:
                            raise RuntimeError(
                                f'No se pudo inscribir usuario {user_email} en call_id={call_id} '
                                f'status={join_res["status"]}: {join_res.get("json")}'
                            )
                    else:
                        created_participants.append({
                            'call_id': call_id,
                            'user_id': user.get('id'),
                            'user_email': user_email,
                            'status': 'EXISTE',
                        })

    list_res = expect(
        200,
        request('GET', '/calls', {'token': admin_token}),
        'Listar convocatorias al final del seed',
    )
    calls_data = (list_res.get('json') or {}).get('data') or []

    return {
        'created_calls': created_calls,
        'skipped_calls': skipped_calls,
        'total_calls': len(calls_data) if isinstance(calls_data, list) else None,
        'calls': calls_data if isinstance(calls_data, list) else [],
        'created_requirements': created_requirements,
        'total_requirements': len(created_requirements),
        'created_participants': created_participants,
        'total_participants': len(created_participants),
    }

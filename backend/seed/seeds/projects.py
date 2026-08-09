import os
import mimetypes

from ..lib.http_client import request, expect
from ..data.projects import DEFAULT_PROJECTS


def _list_projects(user_token):
    res = request('GET', '/projects', {'token': user_token})
    if res['status'] != 200:
        return []
    body = res.get('json') or {}
    data = body.get('data') if isinstance(body, dict) else body
    return data if isinstance(data, list) else []


def _find_project_by_title(user_token, title):
    for p in _list_projects(user_token):
        if isinstance(p, dict) and p.get('title') == title:
            return p
    return None


def _list_documents(user_token, project_id):
    res = request('GET', '/documents', {
        'token': user_token,
        'query': {'project_id': project_id},
    })
    if res['status'] != 200:
        return []
    body = res.get('json') or {}
    docs = body.get('data') if isinstance(body, dict) else body
    return docs if isinstance(docs, list) else []


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


def _load_file(file_path, override_name=None):
    if not file_path or not os.path.isfile(file_path):
        return None
    try:
        with open(file_path, 'rb') as fh:
            data = fh.read()
        fname = override_name or os.path.basename(file_path)
        mtype, _ = mimetypes.guess_type(file_path)
        if override_name:
            guessed, _ = mimetypes.guess_type(override_name)
            if guessed:
                mtype = guessed
        return {
            'name': fname,
            'bytes': data,
            'content_type': mtype or 'application/octet-stream',
        }
    except OSError:
        return None


def _get_user_password(user_email):
    from ..data.users import DEFAULT_USERS
    for du in DEFAULT_USERS:
        if du.get('email') == user_email:
            return du.get('password')
    from ..config import DEFAULT_ADMIN
    if DEFAULT_ADMIN.get('email') == user_email:
        return DEFAULT_ADMIN.get('password')
    return None


def seed_projects(admin_token, users, calls):
    created_projects = []
    skipped_projects = []
    created_documents = []

    calls_by_index = list(calls) if isinstance(calls, list) else []

    for idx, proj_data in enumerate(DEFAULT_PROJECTS):
        documents_data = proj_data.pop('documents', [])
        user_index = proj_data.pop('user_index', 0)
        call_index = proj_data.pop('call_index', None)

        user_obj = users[user_index] if 0 <= user_index < len(users) else None
        if not user_obj:
            continue
        user_email = user_obj.get('email')
        user_id = user_obj.get('id')
        user_password = _get_user_password(user_email)
        if not user_password:
            continue
        user_token = _login_as_user(user_email, user_password)
        if not user_token:
            continue

        call_id = None
        if call_index is not None and 0 <= call_index < len(calls_by_index):
            call_obj = calls_by_index[call_index]
            call_id = call_obj.get('id') if isinstance(call_obj, dict) else None

        existing = _find_project_by_title(user_token, proj_data['title'])

        project_payload = {
            'title': proj_data['title'],
            'description': proj_data.get('description'),
            'status': proj_data.get('status', 'draft'),
        }
        if call_id:
            project_payload['call_id'] = call_id

        if existing:
            project_id = existing.get('id')
            skipped_projects.append({
                'id': project_id,
                'title': proj_data['title'],
                'user_id': user_id,
            })
        else:
            create_res = expect(
                201,
                request('POST', '/projects', {
                    'token': user_token,
                    'body': project_payload,
                }),
                f'Crear proyecto {proj_data["title"]} por {user_email}'
            )
            project_obj = (create_res.get('json') or {}).get('data') or {}
            project_id = project_obj.get('id')
            created_projects.append({
                'id': project_id,
                'title': project_obj.get('title'),
                'user_id': user_id,
                'status': project_obj.get('status'),
            })

        doc_count = 0
        for doc_def in documents_data:
            if doc_count >= 5:
                break
            existing_docs = _list_documents(user_token, project_id)
            doc_original = doc_def.get('original_filename', 'documento.txt')
            already_exists = any(
                d.get('original_filename') == doc_original
                for d in existing_docs if isinstance(d, dict)
            )
            if already_exists:
                created_documents.append({
                    'project_id': project_id,
                    'original_filename': doc_original,
                    'status': 'EXISTE',
                })
                doc_count += 1
                continue

            src_file = doc_def.get('source_file')
            file_payload = _load_file(src_file, override_name=doc_original)
            if not file_payload:
                continue

            upload_opts = {
                'token': user_token,
                'form': {
                    'project_id': project_id,
                },
                'file': file_payload,
            }
            upload_res = request('POST', '/documents/upload', upload_opts)
            if upload_res['status'] == 201:
                doc_obj = (upload_res.get('json') or {}).get('data') or {}
                created_documents.append({
                    'id': doc_obj.get('id'),
                    'project_id': project_id,
                    'original_filename': doc_obj.get('original_filename') or doc_original,
                    'status': 'CREADO',
                })
            elif upload_res['status'] in (400, 409):
                created_documents.append({
                    'project_id': project_id,
                    'original_filename': doc_original,
                    'status': 'SKIP',
                })
            else:
                raise RuntimeError(
                    f'No se pudo subir documento {doc_original} al proyecto {project_id} '
                    f'status={upload_res["status"]}: {upload_res.get("json")}'
                )
            doc_count += 1

    all_projects = []
    for u in users:
        u_email = u.get('email') if isinstance(u, dict) else None
        u_pwd = _get_user_password(u_email) if u_email else None
        if u_email and u_pwd:
            u_token = _login_as_user(u_email, u_pwd)
            if u_token:
                all_projects.extend(_list_projects(u_token))

    seen_ids = set()
    unique_projects = []
    for p in all_projects:
        pid = p.get('id') if isinstance(p, dict) else None
        if pid and pid not in seen_ids:
            seen_ids.add(pid)
            unique_projects.append(p)

    return {
        'created_projects': created_projects,
        'skipped_projects': skipped_projects,
        'total_projects': len(unique_projects),
        'projects': unique_projects,
        'created_documents': created_documents,
        'total_documents': len(created_documents),
    }

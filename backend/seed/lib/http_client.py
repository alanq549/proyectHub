import json
from urllib.parse import urlencode, urlparse, parse_qsl, urlunparse
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

from ..config import API_BASE_URL


def build_url(path, query=None):
    if path.startswith('http://') or path.startswith('https://'):
        url = path
    else:
        url = f'{API_BASE_URL}{path}'

    if query:
        clean_query = {k: v for k, v in query.items() if v is not None}
        if clean_query:
            parsed = urlparse(url)
            existing = dict(parse_qsl(parsed.query))
            existing.update({str(k): str(v) for k, v in clean_query.items()})
            new_query = urlencode(existing)
            url = urlunparse(parsed._replace(query=new_query))
    return url


def build_headers(token=None, is_multipart=False):
    headers = {}
    if not is_multipart:
        headers['Content-Type'] = 'application/json'
    if token:
        headers['Authorization'] = f'Bearer {token}'
    return headers


def _encode_body(body, form, file, is_multipart):
    if not is_multipart:
        if body is None:
            return None, {}
        return json.dumps(body).encode('utf-8'), {}

    boundary = '----ProjectHubSeedBoundary' + 'x' * 24
    parts = []

    def add_field(name, value):
        parts.append(f'--{boundary}'.encode('utf-8'))
        parts.append(
            f'Content-Disposition: form-data; name="{name}"'.encode('utf-8')
        )
        parts.append(b'')
        if isinstance(value, (dict, list)):
            parts.append(json.dumps(value).encode('utf-8'))
        else:
            parts.append(str(value).encode('utf-8'))

    if form:
        for k, v in form.items():
            if v is None:
                continue
            add_field(k, v)
    if body and isinstance(body, dict):
        for k, v in body.items():
            if v is None:
                continue
            add_field(k, v)
    if file:
        file_bytes = file.get('bytes')
        file_name = file.get('name', 'file')
        content_type = file.get('content_type', 'application/octet-stream')
        parts.append(f'--{boundary}'.encode('utf-8'))
        parts.append(
            (
                f'Content-Disposition: form-data; name="file"; filename="{file_name}"'
            ).encode('utf-8')
        )
        parts.append(f'Content-Type: {content_type}'.encode('utf-8'))
        parts.append(b'')
        parts.append(file_bytes if isinstance(file_bytes, (bytes, bytearray)) else b'')

    parts.append(f'--{boundary}--'.encode('utf-8'))
    parts.append(b'')

    payload = b'\r\n'.join(parts)
    headers = {'Content-Type': f'multipart/form-data; boundary={boundary}'}
    return payload, headers


def request(method, path, options=None):
    options = options or {}
    token = options.get('token')
    body = options.get('body')
    query = options.get('query')
    file = options.get('file')
    form = options.get('form')

    is_multipart = bool(file) or bool(form)
    url = build_url(path, query)

    extra_headers = {}
    if is_multipart:
        payload, extra_headers = _encode_body(body, form, file, True)
    else:
        payload, _ = _encode_body(body, None, None, False)

    headers = build_headers(token=token, is_multipart=is_multipart)
    headers.update(extra_headers)

    req = Request(url, data=payload, headers=headers, method=method.upper())

    try:
        with urlopen(req, timeout=60) as resp:
            raw = resp.read()
            status = resp.status
    except HTTPError as e:
        raw = e.read()
        status = e.code
    except URLError as e:
        return {
            'status': 0,
            'json': {'error': str(e.reason)},
            'ok': False,
        }

    json_data = None
    text = raw.decode('utf-8', errors='replace') if raw else ''
    if text:
        try:
            json_data = json.loads(text)
        except (ValueError, json.JSONDecodeError):
            json_data = {'raw': text}

    return {
        'status': status,
        'json': json_data if json_data is not None else {},
        'ok': 200 <= status < 300,
    }


def expect(status, res, context=None):
    actual = res.get('status')
    if actual != status:
        msg_parts = [f'[FAIL] {context or ""}',
                     f'  Esperado: {status}',
                     f'  Actual  : {actual}',
                     f'  Body    : {json.dumps(res.get("json"), ensure_ascii=False)}']
        raise AssertionError('\n'.join(msg_parts))
    return res

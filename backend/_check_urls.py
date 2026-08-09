import sys
import os

sys.path.insert(0, os.getcwd())
sys.path.insert(0, os.path.join(os.getcwd(), 'seed'))

from seed.lib.http_client import build_url

cases = [
    ('/login',               False, 'auth root: NO slash'),
    ('/register',            False, 'auth root: NO slash'),
    ('/me',                  False, 'auth root: NO slash'),
    ('/refresh',             False, 'auth root: NO slash'),
    ('/logout',              False, 'auth root: NO slash'),
    ('/me/password',         True,  'auth 2-segment: YES slash'),
    ('/users',               True,  'users collection: YES slash'),
    ('/users/2',             True,  'users id: YES slash'),
    ('/calls',               True,  'calls collection: YES slash'),
    ('/calls/10',            True,  'call id: YES slash'),
    ('/calls/10/join',       True,  'call join: YES slash'),
    ('/calls/10/requirements', True, 'call requirements: YES slash'),
    ('/calls/participants/7/status', True, 'participant status: YES slash'),
    ('/projects',            True,  'projects collection: YES slash'),
    ('/projects/1',          True,  'project id: YES slash'),
    ('/documents',           True,  'documents collection: YES slash'),
    ('/documents/upload',    True,  'doc upload: YES slash'),
    ('/documents/1/download', True, 'doc download: YES slash'),
    ('/history',             True,  'history: YES slash'),
    ('/static/defaults/icon_default.png', False, 'PNG asset: NO slash'),
    ('/static/uploads/profiles/x.jpg',    False, 'JPG asset: NO slash'),
]

all_ok = True
for path, expect_slash, desc in cases:
    url = build_url(path)
    parsed = urlparse(url)
    has_trailing = parsed.path.endswith('/')
    ok = has_trailing == expect_slash
    if not ok:
        all_ok = False
    status = 'OK' if ok else 'FAIL'
    prefix = '[{}]'.format(status)
    print(prefix, desc)
    print('   Input :', path)
    print('   Output:', parsed.path)
    print()

print('======')
if all_ok:
    print('ALL CASES PASSED')
    sys.exit(0)
else:
    print('SOME CASES FAILED')
    sys.exit(1)

import os
import sys

SEED_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(SEED_DIR)
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)
if SEED_DIR not in sys.path:
    sys.path.insert(0, SEED_DIR)

from seed.lib.auth import ensure_admin
from seed.seeds.users import seed_users


SECTIONS = []
RESULTS = []


def record(section, name, description, result):
    if not any(s['key'] == section for s in SECTIONS):
        SECTIONS.append({'key': section, 'name': section})
    RESULTS.append({
        'section': section,
        'name': name,
        'description': description,
        'result': result,
    })


def header(title):
    bar = '═' * 62
    print()
    print('╔' + bar + '╗')
    padded = f'  {title}'
    if len(padded) < 62:
        padded = padded + ' ' * (62 - len(padded))
    print('║' + padded + '║')
    print('╚' + bar + '╝')
    print()


def print_summary():
    print('\n── RESUMEN DE SEED ──────────────────────────────────────────')
    for s in SECTIONS:
        rows = [r for r in RESULTS if r['section'] == s['key']]
        print(f'\n[{s["name"]}] {len(rows)} paso(s):')
        for r in rows:
            status = r['result']
            if isinstance(status, bool):
                status_str = 'OK' if status else 'FAIL'
            else:
                status_str = str(status)
            name_line = f'  • {r["name"]}'
            fill = '.' * max(1, 48 - len(name_line))
            print(f'{name_line} {fill} → {status_str}')
            if r.get('description'):
                print(f'      {r["description"]}')

    any_fail = any(
        r['result'] == 'FAIL' or r['result'] is False for r in RESULTS
    )
    print('\n─────────────────────────────────────────────────────────────')
    if any_fail:
        print('❌ Algunos pasos del seed fallaron.')
        sys.exit(1)
    print('✅ Seed completado satisfactoriamente.')


def main():
    header('PROJECTHUB · SEED PROGRESIVO POR ENDPOINTS (PYTHON)')

    print('> Asegurando usuario administrador (por endpoints)...')
    try:
        admin = ensure_admin()
    except Exception as e:
        print('💥 ERROR en ensure_admin:', e)
        sys.exit(1)

    admin_user = admin.get('user') or {}
    record(
        'AUTH',
        'ensureAdmin',
        f'email={admin_user.get("email")} role={admin_user.get("role")}',
        'CREADO' if admin.get('created') else 'EXISTE',
    )
    if admin_user.get('role') != 'admin':
        print('⚠️  ADVERTENCIA: El usuario admin no tiene role=admin.')
        print(
            '   El registro público crea usuarios con role=user por defecto; '
            'el primero se promueve automáticamente solo si '
            'BOOTSTRAP_FIRST_USER_AS_ADMIN=true y la tabla estaba vacía.'
        )
        print(f'   UPDATE users SET role=\'admin\' WHERE email=\'{admin_user.get("email")}\';\n')

    print('> Seed del módulo Users (admin crea/actualiza 5 usuarios demo)...')
    try:
        users_report = seed_users(admin['token'])
    except Exception as e:
        print('💥 ERROR en seed_users:', e)
        raise

    created = users_report.get('created') or []
    skipped = users_report.get('skipped') or []
    record(
        'USERS',
        'seedUsers',
        (
            f'creados={len(created)} '
            f'actualizados={sum(1 for s in skipped if s.get("updated"))} '
            f'skipped={len(skipped)} '
            f'total={users_report.get("total")}'
        ),
        'OK' if len(created) >= 0 else 'FAIL',
    )
    if created:
        print('  Creados:')
        for u in created:
            print(
                f'    - #{u.get("id")} {u.get("email")} ({u.get("role")}) '
                f'· avatar={u.get("profile_picture_url")}'
            )
    if skipped:
        print(
            '  Ya existían (skip/update): ' +
            ', '.join(s.get('email', '') for s in skipped)
        )

    print_summary()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\n⏹  Seed cancelado por el usuario.')
        sys.exit(130)
    except Exception as err:
        print('\n💥 Seed interrumpido por error:', err)
        sys.exit(1)

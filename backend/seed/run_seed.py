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
from seed.seeds.calls import seed_calls
from seed.seeds.projects import seed_projects


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

    admin_token = admin['token']
    created_users_all = []

    print('> Seed del módulo Users (admin crea/actualiza 5 usuarios demo con fotos)...')
    try:
        users_report = seed_users(admin_token)
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
    created_users_all = list(users_report.get('users') or [])
    if admin_user:
        created_users_all.insert(0, admin_user)

    print('\n> Seed del módulo Calls (5 convocatorias + 5 requisitos c/u + 5 participantes)...')
    try:
        calls_report = seed_calls(admin_token, created_users_all)
    except Exception as e:
        print('💥 ERROR en seed_calls:', e)
        raise

    created_calls = calls_report.get('created_calls') or []
    skipped_calls = calls_report.get('skipped_calls') or []
    record(
        'CALLS',
        'seedCalls',
        (
            f'creadas={len(created_calls)} '
            f'existentes={len(skipped_calls)} '
            f'total={calls_report.get("total_calls")}'
        ),
        'OK' if calls_report.get('total_calls', 0) >= 0 else 'FAIL',
    )
    if created_calls:
        print('  Convocatorias creadas:')
        for c in created_calls:
            print(f'    - #{c.get("id")} {c.get("title")}')
    if skipped_calls:
        print(
            '  Ya existían: ' +
            ', '.join(s.get('title', '') for s in skipped_calls)
        )

    created_reqs = calls_report.get('created_requirements') or []
    record(
        'CALL REQUIREMENTS',
        'seedCallRequirements',
        (
            f'creados={sum(1 for r in created_reqs if not r.get("skipped"))} '
            f'skipped={sum(1 for r in created_reqs if r.get("skipped"))} '
            f'total={calls_report.get("total_requirements")}'
        ),
        'OK' if len(created_reqs) > 0 else 'FAIL',
    )
    print(f'  Requisitos de convocatorias procesados: {len(created_reqs)}')

    created_participants = calls_report.get('created_participants') or []
    record(
        'CALL PARTICIPANTS',
        'seedCallParticipants',
        (
            f'inscritos={sum(1 for p in created_participants if p.get("status") == "REGISTERED")} '
            f'preexistentes={sum(1 for p in created_participants if p.get("status") == "EXISTE")} '
            f'total={calls_report.get("total_participants")}'
        ),
        'OK' if len(created_participants) > 0 else 'FAIL',
    )
    if created_participants:
        print('  Participantes inscritos:')
        for p in created_participants:
            print(
                f'    - call#{p.get("call_id")} user#{p.get("user_id")} '
                f'({p.get("user_email")}) [{p.get("status")}]'
            )

    calls_all = list(calls_report.get('calls') or [])

    print('\n> Seed del módulo Projects (5 proyectos + 5 documentos c/u)...')
    try:
        projects_report = seed_projects(admin_token, created_users_all, calls_all)
    except Exception as e:
        print('💥 ERROR en seed_projects:', e)
        raise

    created_projects = projects_report.get('created_projects') or []
    skipped_projects = projects_report.get('skipped_projects') or []
    record(
        'PROJECTS',
        'seedProjects',
        (
            f'creados={len(created_projects)} '
            f'existentes={len(skipped_projects)} '
            f'total={projects_report.get("total_projects")}'
        ),
        'OK' if projects_report.get('total_projects', 0) >= 0 else 'FAIL',
    )
    if created_projects:
        print('  Proyectos creados:')
        for p in created_projects:
            print(
                f'    - #{p.get("id")} {p.get("title")} '
                f'[user#{p.get("user_id")} / {p.get("status")}]'
            )
    if skipped_projects:
        print(
            '  Ya existían: ' +
            ', '.join(s.get('title', '') for s in skipped_projects)
        )

    created_docs = projects_report.get('created_documents') or []
    record(
        'DOCUMENTS',
        'seedDocuments',
        (
            f'subidos={sum(1 for d in created_docs if d.get("status") == "CREADO")} '
            f'existentes={sum(1 for d in created_docs if d.get("status") in ("EXISTE", "SKIP"))} '
            f'total={projects_report.get("total_documents")}'
        ),
        'OK' if len(created_docs) > 0 else 'FAIL',
    )
    print(f'  Documentos procesados: {len(created_docs)}')

    record(
        'ACTIVITY LOGS',
        'autoGenerated',
        'Los activity logs se generan automáticamente por cada acción CRUD realizada (usuarios, convocatorias, proyectos, documentos).',
        'OK',
    )
    print('  Los Activity Logs han sido generados automáticamente por cada acción.')

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

# Reset de la base de datos (Neon + Flask + Alembic)

## Cuándo usarlo

Utilizar este procedimiento cuando:

* Una migración falla y la base queda en un estado inconsistente.
* Se quiere empezar desde cero durante el desarrollo.
* No existen datos importantes que conservar.

## 1. Eliminar el esquema actual

Ejecutar en PostgreSQL:

```sql
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
```

Esto elimina todas las tablas, índices, secuencias y la tabla `alembic_version`.

## 2. Aplicar las migraciones nuevamente

```bash
python run.py db upgrade
```

Si se hicieron cambios en los modelos antes de crear la migración:

```bash
python run.py db migrate -m "descripcion_de_la_migracion"
python run.py db upgrade
```

## comandos útiles de Alembic
- python run.py db current     # Ver la migración actual
- python run.py db history     # Ver el historial
- python run.py db migrate -m "mensaje"
- python run.py db upgrade
- python run.py db downgrade   # Revertir una migración

## Notas

* ⚠️ Este procedimiento elimina todos los datos de la base de datos.
* Solo debe utilizarse en entornos de desarrollo.
* No usar en producción.

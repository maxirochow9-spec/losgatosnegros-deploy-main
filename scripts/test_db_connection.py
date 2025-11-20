#!/usr/bin/env python3
"""
Pequeño script para probar la conexión a PostgreSQL usando .env o variables de entorno.

Soporta:
- `DATABASE_URL` (ej: postgres://user:pass@host:5432/dbname?sslmode=require)
- o variables individuales: DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME

Uso: `python scripts/test_db_connection.py`
"""
import os
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()

def mask_dsn(dsn):
    try:
        p = urlparse(dsn)
        user = p.username or ''
        host = p.hostname or ''
        port = p.port or ''
        db = p.path.lstrip('/') or ''
        return f"postgresql://{user}:*****@{host}:{port}/{db}"
    except Exception:
        return dsn


def build_dsn_from_env():
    # Buscar nombres comunes
    user = os.getenv('DATABASE_USER') or os.getenv('DB_USER') or os.getenv('losgatosdb_POSTGRES_USER') or os.getenv('USER') or os.getenv('user')
    password = os.getenv('DATABASE_PASSWORD') or os.getenv('DB_PASSWORD') or os.getenv('losgatosdb_POSTGRES_PASSWORD') or os.getenv('PASSWORD') or os.getenv('password')
    host = os.getenv('DATABASE_HOST') or os.getenv('DB_HOST') or os.getenv('losgatosdb_POSTGRES_HOST') or os.getenv('HOST') or os.getenv('host')
    port = os.getenv('DATABASE_PORT') or os.getenv('DB_PORT') or os.getenv('losgatosdb_POSTGRES_PORT') or os.getenv('PORT') or os.getenv('port') or '5432'
    dbname = os.getenv('DATABASE_NAME') or os.getenv('DB_NAME') or os.getenv('losgatosdb_POSTGRES_DATABASE') or os.getenv('DBNAME') or os.getenv('PGDATABASE') or 'postgres'

    if not (host and user and password):
        print('Aviso: faltan algunas variables necesarias para construir el DSN (host/user/password).')
        print(f'Valores actuales -> host={host!r}, user={user!r}, port={port!r}, dbname={dbname!r}')

    return f"postgresql://{user}:{password}@{host}:{port}/{dbname}"


def main():
    # Prefer DATABASE_URL
    database_url = os.getenv('DATABASE_URL') or os.getenv('DATABASE_URL_INTERNAL')

    if database_url and database_url.startswith('postgres'):
        dsn = database_url
    else:
        dsn = build_dsn_from_env()

    print('Intentando conectar usando DSN:', mask_dsn(dsn))

    # Intentar con psycopg (psycopg3) o psycopg2 si no está disponible
    last_exc = None
    try:
        # psycopg (v3) si está instalado
        import psycopg as db
        conn = db.connect(dsn)
        cur = conn.cursor()
        cur.execute('SELECT NOW();')
        res = cur.fetchone()
        print('Conexión exitosa (psycopg):', res)
        cur.close()
        conn.close()
        return
    except Exception as e:
        last_exc = e
        print('psycopg (v3) falló:', e)

    try:
        import psycopg2
        conn = psycopg2.connect(dsn)
        cur = conn.cursor()
        cur.execute('SELECT NOW();')
        res = cur.fetchone()
        print('Conexión exitosa (psycopg2):', res)
        cur.close()
        conn.close()
        return
    except Exception as e2:
        last_exc = e2
        print('psycopg2 falló:', e2)

    print('\nNo se pudo establecer la conexión. Última excepción:')
    print(last_exc)


if __name__ == '__main__':
    main()

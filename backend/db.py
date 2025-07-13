"""
Módulo de utilidades para la base de datos PostgreSQL.
Conexión directa con psycopg2 usando las credenciales del .env
"""

from typing import List, Tuple
import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor

# ---------- Configuración ---------- #
load_dotenv()  # lee .env solo una vez al importar el módulo

PGHOST = os.getenv("PGHOST", "localhost")
PGPORT = os.getenv("PGPORT", "5432")
PGDATABASE = os.getenv("PGDATABASE", "feedback")
PGUSER = os.getenv("PGUSER", "postgres")
PGPASSWORD = os.getenv("PGPASSWORD", "")

_CONN_INFO = {
    "host": PGHOST,
    "port": PGPORT,
    "dbname": PGDATABASE,
    "user": PGUSER,
    "password": PGPASSWORD,
}

# ---------- Helpers ---------- #
def _get_conn():
    """Devuelve una conexión nueva; recuerda cerrarla tras usarla."""
    return psycopg2.connect(**_CONN_INFO)


def init_db() -> None:
    """Crea la tabla feedback si aún no existe."""
    # lenguaje de definición de datos (DDL) SQL. para crear la estructura de la tabla.
    ddl = """
    CREATE TABLE IF NOT EXISTS feedback (
        id SERIAL PRIMARY KEY,
        texto      TEXT NOT NULL,
        respuesta  TEXT NOT NULL,
        fecha      TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    """
    with _get_conn() as conn, conn.cursor() as cur:
        cur.execute(ddl)
        conn.commit()


# ---------- API pública ---------- #
def guardar_postgres(texto: str, respuesta: str) -> None:
    """Inserta un nuevo registro en la tabla feedback."""
    sql = "INSERT INTO feedback (texto, respuesta) VALUES (%s, %s);"
    with _get_conn() as conn, conn.cursor() as cur:
        cur.execute(sql, (texto, respuesta))
        conn.commit()


def leer_historial(limit: int = 20) -> List[Tuple]:
    """Devuelve los últimos <limit> registros como lista de dicts."""
    sql = "SELECT * FROM feedback ORDER BY fecha DESC LIMIT %s;"
    with _get_conn() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(sql, (limit,))
        return cur.fetchall()

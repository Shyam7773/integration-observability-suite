import os
import sys
from pathlib import Path

# Ensure repo root is importable
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv
load_dotenv()

import psycopg2

def _dsn():
    dsn = os.getenv("DATABASE_URL")
    if not dsn:
        raise RuntimeError("DATABASE_URL not set for tests")
    return dsn

def _exec(sql: str):
    with psycopg2.connect(_dsn()) as conn, conn.cursor() as cur:
        cur.execute(sql)

def pytest_sessionstart(session):
    # Ensure schema exists
    init_sql = (ROOT / "infra" / "init.sql").read_text(encoding="utf-8")
    _exec(init_sql)

import pytest

@pytest.fixture(autouse=True)
def clean_db():
    _exec("""
    truncate table
      raw.alerts,
      raw.connector_attempts,
      raw.connector_runs,
      raw.connector_schema
    restart identity;
    """)
    yield

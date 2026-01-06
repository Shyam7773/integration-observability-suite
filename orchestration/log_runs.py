from __future__ import annotations
from typing import Optional
from orchestration.db import get_conn

def insert_run(
    *,
    connector_name: str,
    idempotency_key: str,
    status: str,
    started_at,
    ended_at,
    latency_ms: int,
    attempts: int,
    request_count: int,
    rate_limited: bool,
    error_type: Optional[str],
    error_message: Optional[str],
) -> None:
    sql = """
    insert into raw.connector_runs
    (connector_name, idempotency_key, status, started_at, ended_at, latency_ms,
     attempts, request_count, rate_limited, error_type, error_message)
    values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    on conflict (connector_name, idempotency_key) do nothing
    """
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            sql,
            (
                connector_name,
                idempotency_key,
                status,
                started_at,
                ended_at,
                latency_ms,
                attempts,
                request_count,
                rate_limited,
                error_type,
                error_message,
            ),
        )

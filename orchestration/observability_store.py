from __future__ import annotations
from typing import Optional, List
from orchestration.db import get_conn

def write_alert(*, severity: str, connector_name: Optional[str], alert_type: str,
                message: str, recommended_action: str, dedupe_minutes: int = 30) -> None:
    # Prevent alert spam: don't insert same alert type for same connector too often
    sql = """
    insert into raw.alerts(severity, connector_name, alert_type, message, recommended_action)
    select %s,%s,%s,%s,%s
    where not exists (
      select 1
      from raw.alerts a
      where a.severity = %s
        and a.alert_type = %s
        and (a.connector_name is not distinct from %s)
        and a.created_at > now() - (%s || ' minutes')::interval
    )
    """
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            sql,
            (
                severity, connector_name, alert_type, message, recommended_action,
                severity, alert_type, connector_name, dedupe_minutes,
            ),
        )

def get_schema_keys(connector_name: str) -> Optional[List[str]]:
    sql = "select schema_keys from raw.connector_schema where connector_name=%s"
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(sql, (connector_name,))
        row = cur.fetchone()
    return list(row[0]) if row else None

def upsert_schema_keys(connector_name: str, keys: List[str]) -> None:
    sql = """
    insert into raw.connector_schema(connector_name, schema_keys)
    values (%s,%s)
    on conflict (connector_name) do update
      set schema_keys = excluded.schema_keys,
          updated_at = now()
    """
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(sql, (connector_name, keys))

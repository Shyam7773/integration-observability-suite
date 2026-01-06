import psycopg2
import os
from orchestration.observability_store import write_alert

def dsn():
    return os.environ["DATABASE_URL"]

def test_alert_dedupe_prevents_spam():
    write_alert(
        severity="warning",
        connector_name="x",
        alert_type="freshness",
        message="No successful run",
        recommended_action="Check scheduler",
        dedupe_minutes=60,
    )
    write_alert(
        severity="warning",
        connector_name="x",
        alert_type="freshness",
        message="No successful run",
        recommended_action="Check scheduler",
        dedupe_minutes=60,
    )

    with psycopg2.connect(dsn()) as conn, conn.cursor() as cur:
        cur.execute("select count(*) from raw.alerts where connector_name='x' and alert_type='freshness'")
        assert cur.fetchone()[0] == 1

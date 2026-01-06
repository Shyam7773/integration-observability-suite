import psycopg2
import os
from checks.schema_drift import check_schema_drift

def dsn():
    return os.environ["DATABASE_URL"]

def test_schema_drift_creates_alert_and_updates_schema():
    # baseline - no alert
    check_schema_drift("schema_changer", {"user_id": 1, "value": 10, "version": 1})

    # drift - should alert
    check_schema_drift("schema_changer", {"user_id": 1, "amount": 10, "currency": "EUR", "version": 2})

    with psycopg2.connect(dsn()) as conn, conn.cursor() as cur:
        cur.execute("select count(*) from raw.alerts where alert_type='schema_drift' and connector_name='schema_changer'")
        assert cur.fetchone()[0] == 1

        cur.execute("select schema_keys from raw.connector_schema where connector_name='schema_changer'")
        keys = cur.fetchone()[0]
        assert "amount" in keys and "currency" in keys

from datetime import datetime, timezone, timedelta
import os
import psycopg2

from orchestration.log_runs import insert_run
from models.run_models import run_models

def dsn():
    return os.environ["DATABASE_URL"]

def test_marts_success_rate_math():
    now = datetime.now(timezone.utc)
    # 2 success, 1 fail => success_rate ~ 0.6667
    for i, status in enumerate(["success", "success", "failed"]):
        insert_run(
            connector_name="kpi_test",
            idempotency_key=f"kpi:{i}",
            status=status,
            started_at=now - timedelta(seconds=10+i),
            ended_at=now - timedelta(seconds=i),
            latency_ms=100 + i,
            attempts=1,
            request_count=1,
            rate_limited=False,
            error_type=("X" if status == "failed" else None),
            error_message=("boom" if status == "failed" else None),
        )

    run_models()

    with psycopg2.connect(dsn()) as conn, conn.cursor() as cur:
        cur.execute("""
          select success_rate
          from mart.connector_health_daily
          where connector_name='kpi_test'
          order by day desc
          limit 1
        """)
        rate = cur.fetchone()[0]
        assert abs(rate - (2/3)) < 0.01

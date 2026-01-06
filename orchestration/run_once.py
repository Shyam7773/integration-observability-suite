from __future__ import annotations
import os
import time
from datetime import datetime, timezone

from adapters.simulated_connectors import GoodConnector, RateLimitedConnector, SchemaChangerConnector
from adapters.open_meteo_connector import OpenMeteoConnector
from orchestration.log_runs import insert_run
from checks.schema_drift import check_schema_drift

def utcnow():
    return datetime.now(timezone.utc)

def run_connector(connector):
    idem = connector.build_idempotency_key()
    started = utcnow()
    t0 = time.time()

    result = connector.run()

    ended = utcnow()
    latency_ms = result.latency_ms or int((time.time() - t0) * 1000)

    insert_run(
        connector_name=connector.name,
        idempotency_key=idem,
        status=result.status,
        started_at=started,
        ended_at=ended,
        latency_ms=latency_ms,
        attempts=result.attempts,
        request_count=result.request_count,
        rate_limited=result.rate_limited,
        error_type=result.error_type,
        error_message=result.error_message,
    )

    if result.payload:
        check_schema_drift(connector.name, result.payload)

    print(f"[{connector.name}] {result.status} latency_ms={latency_ms} attempts={result.attempts} rate_limited={result.rate_limited}")

def main():
    connectors = [GoodConnector(), RateLimitedConnector(), SchemaChangerConnector()]
    if os.getenv('ENABLE_REAL_CONNECTOR') == '1':
        connectors.append(OpenMeteoConnector())
    for c in connectors:
        run_connector(c)

if __name__ == "__main__":
    main()
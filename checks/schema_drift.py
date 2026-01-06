from __future__ import annotations
from typing import Dict, Any
from orchestration.observability_store import get_schema_keys, upsert_schema_keys, write_alert

def check_schema_drift(connector_name: str, payload: Dict[str, Any]) -> None:
    new_keys = sorted(list(payload.keys()))
    prev = get_schema_keys(connector_name)

    # First run: record baseline
    if prev is None:
        upsert_schema_keys(connector_name, new_keys)
        return

    prev_sorted = sorted(prev)
    if prev_sorted != new_keys:
        write_alert(
            severity="warning",
            connector_name=connector_name,
            alert_type="schema_drift",
            message=f"Schema drift detected. Prev={prev_sorted} New={new_keys}",
            recommended_action="Update mapping/contract; optionally quarantine payloads and replay after fix."
        )
        upsert_schema_keys(connector_name, new_keys)

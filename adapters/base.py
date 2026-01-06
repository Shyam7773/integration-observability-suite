from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, Optional
import uuid

@dataclass
class ConnectorResult:
    status: str  # "success" | "failed"
    payload: Optional[Dict[str, Any]]
    request_count: int
    rate_limited: bool
    error_type: Optional[str] = None
    error_message: Optional[str] = None
    http_status: Optional[int] = None
    latency_ms: int = 0
    attempts: int = 0

def default_idempotency_key(prefix: str) -> str:
    # For demo: unique per run; later replace with event_id/payload_id
    return f"{prefix}:{uuid.uuid4()}"

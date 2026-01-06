from __future__ import annotations
import random
import time
from adapters.base import ConnectorResult, default_idempotency_key

class GoodConnector:
    name = "good_api"

    def build_idempotency_key(self) -> str:
        return default_idempotency_key(self.name)

    def run(self) -> ConnectorResult:
        t0 = time.time()
        payload = {"user_id": 123, "value": 42, "version": 1}
        latency_ms = int((time.time() - t0) * 1000)
        return ConnectorResult(
            status="success",
            payload=payload,
            request_count=1,
            rate_limited=False,
            latency_ms=latency_ms,
            attempts=1,
        )

class RateLimitedConnector:
    name = "rate_limited_api"

    def build_idempotency_key(self) -> str:
        return default_idempotency_key(self.name)

    def run(self) -> ConnectorResult:
        t0 = time.time()
        attempts = 0
        rate_limited = False

        for _ in range(3):
            attempts += 1

            # 50% chance to simulate a 429
            if random.random() < 0.5:
                rate_limited = True
                time.sleep(0.2)  # backoff
                continue

            payload = {"ok": True, "attempt": attempts}
            latency_ms = int((time.time() - t0) * 1000)
            return ConnectorResult(
                status="success",
                payload=payload,
                request_count=attempts,
                rate_limited=rate_limited,
                latency_ms=latency_ms,
                attempts=attempts,
            )

        latency_ms = int((time.time() - t0) * 1000)
        return ConnectorResult(
            status="failed",
            payload=None,
            request_count=attempts,
            rate_limited=True,
            error_type="RateLimitError",
            error_message="429 Too Many Requests",
            http_status=429,
            latency_ms=latency_ms,
            attempts=attempts,
        )

class SchemaChangerConnector:
    name = "schema_changer"

    def build_idempotency_key(self) -> str:
        return default_idempotency_key(self.name)

    def run(self) -> ConnectorResult:
        t0 = time.time()

        # Flip schema sometimes (drift)
        if random.random() < 0.5:
            payload = {"user_id": 1, "value": 10, "version": 1}
        else:
            payload = {"user_id": 1, "amount": 10, "currency": "EUR", "version": 2}

        latency_ms = int((time.time() - t0) * 1000)
        return ConnectorResult(
            status="success",
            payload=payload,
            request_count=1,
            rate_limited=False,
            latency_ms=latency_ms,
            attempts=1,
        )

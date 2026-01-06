from __future__ import annotations
import time
import requests
from adapters.base import ConnectorResult, default_idempotency_key

class OpenMeteoConnector:
    name = "open_meteo"

    def __init__(self, latitude: float = 53.3498, longitude: float = -6.2603):
        self.latitude = latitude
        self.longitude = longitude

    def build_idempotency_key(self) -> str:
        return default_idempotency_key(self.name)

    def run(self) -> ConnectorResult:
        t0 = time.time()
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "current_weather": "true",
        }

        try:
            r = requests.get(url, params=params, timeout=6)
        except requests.Timeout:
            latency_ms = int((time.time() - t0) * 1000)
            return ConnectorResult(
                status="failed",
                payload=None,
                request_count=1,
                rate_limited=False,
                error_type="TimeoutError",
                error_message="Request timed out",
                latency_ms=latency_ms,
                attempts=1,
            )
        except requests.RequestException as e:
            latency_ms = int((time.time() - t0) * 1000)
            return ConnectorResult(
                status="failed",
                payload=None,
                request_count=1,
                rate_limited=False,
                error_type="RequestError",
                error_message=str(e),
                latency_ms=latency_ms,
                attempts=1,
            )

        latency_ms = int((time.time() - t0) * 1000)

        if r.status_code == 429:
            return ConnectorResult(
                status="failed",
                payload=None,
                request_count=1,
                rate_limited=True,
                error_type="RateLimitError",
                error_message="429 Too Many Requests",
                http_status=429,
                latency_ms=latency_ms,
                attempts=1,
            )

        if r.status_code != 200:
            return ConnectorResult(
                status="failed",
                payload=None,
                request_count=1,
                rate_limited=False,
                error_type="HttpError",
                error_message=f"HTTP {r.status_code}",
                http_status=r.status_code,
                latency_ms=latency_ms,
                attempts=1,
            )

        data = r.json()
        cw = data.get("current_weather") or {}

        payload = {
            "latitude": data.get("latitude"),
            "longitude": data.get("longitude"),
            "temperature": cw.get("temperature"),
            "windspeed": cw.get("windspeed"),
            "winddirection": cw.get("winddirection"),
            "time": cw.get("time"),
            "source": "open-meteo",
        }

        return ConnectorResult(
            status="success",
            payload=payload,
            request_count=1,
            rate_limited=False,
            latency_ms=latency_ms,
            attempts=1,
        )

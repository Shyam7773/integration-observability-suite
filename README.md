![CI](https://github.com/Shyam7773/integration-observability-suite/actions/workflows/ci.yml/badge.svg)

# Integration Observability Suite — Connector Health

I started this project for one simple reason: **integrations don’t fail loudly**.

Most pipelines don’t “crash” — they *quietly rot*. A vendor rate-limits you. A field gets renamed. A payload shape drifts. Your job still “runs”… but your downstream data slowly turns into a fairytale.

So I built the thing I always wished existed when working with messy real-world integrations:

**A small, production-style observability layer for connectors** — log every run, detect schema drift, raise actionable alerts, and surface KPIs in one dashboard.

---

## What this project does

- **Runs connectors** (simulated connectors + an optional real public API connector)
- **Logs every run** into Postgres (`success/failed`, latency, attempts, rate-limited, error type)
- **Detects schema drift** (payload keys change → alert)
- **Dedupes alerts** (prevents spam)
- **Builds KPI marts** in Postgres for daily health metrics
- **Streamlit dashboard** to monitor runs, alerts, and KPIs
- **Automated CI smoke test** with GitHub Actions
- **Pytest suite** to keep behaviour stable

---

## Architecture (the mental model)

```mermaid
flowchart LR
  A[Connector Runner] --> B[Adapters / Connectors]
  B --> C[(Postgres: raw schema)]
  B --> D[Schema Drift Check]
  D --> E[(Postgres: raw.alerts)]
  C --> F[Models: marts.sql]
  F --> G[(Postgres: mart views)]
  C --> H[Streamlit Dashboard]
  E --> H
  G --> H

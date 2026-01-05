# Integration Reliability & Observability Suite

A small platform to run connectors (API/webhook/CSV), track reliability KPIs, detect schema drift, and raise alerts.

## Quickstart (local)
1. Copy env: `cp .env.example .env`
2. Bring up infra: `make up`
3. Init DB: `make initdb`
4. Run pipeline: `make run`
5. Dashboard: `make dash`

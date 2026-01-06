create schema if not exists raw;

create table if not exists raw.connector_runs (
  run_id bigserial primary key,
  connector_name text not null,
  idempotency_key text not null,
  status text not null,               -- success | failed
  started_at timestamptz not null,
  ended_at timestamptz not null,
  latency_ms integer not null,
  attempts integer not null,
  request_count integer not null default 0,
  rate_limited boolean not null default false,
  error_type text,
  error_message text
);

create unique index if not exists ux_runs_connector_idem
  on raw.connector_runs(connector_name, idempotency_key);

create table if not exists raw.connector_attempts (
  attempt_id bigserial primary key,
  connector_name text not null,
  idempotency_key text not null,
  attempt_no integer not null,
  started_at timestamptz not null,
  ended_at timestamptz not null,
  status text not null,               -- success | failed
  http_status integer,
  error_type text,
  error_message text
);

create table if not exists raw.alerts (
  alert_id bigserial primary key,
  created_at timestamptz not null default now(),
  severity text not null,             -- info | warning | critical
  connector_name text,
  alert_type text not null,           -- freshness | success_rate | schema_drift | retries
  message text not null,
  recommended_action text
);

create table if not exists raw.connector_schema (
  connector_name text primary key,
  schema_keys text[] not null,
  updated_at timestamptz not null default now()
);

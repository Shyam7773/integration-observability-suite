create schema if not exists mart;

create or replace view mart.connector_health_daily as
select
  connector_name,
  date_trunc('day', ended_at) as day,
  count(*) as total_runs,
  avg(case when status='success' then 1 else 0 end)::float as success_rate,
  avg(latency_ms)::float as avg_latency_ms,
  avg(attempts)::float as avg_attempts,
  avg(case when rate_limited then 1 else 0 end)::float as rate_limited_rate
from raw.connector_runs
group by 1,2;

create or replace view mart.top_failure_reasons as
select
  connector_name,
  coalesce(error_type, 'unknown') as error_type,
  count(*) as failures
from raw.connector_runs
where status='failed'
group by 1,2
order by failures desc;

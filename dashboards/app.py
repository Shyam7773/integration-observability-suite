import os
import pandas as pd
import streamlit as st
import psycopg2

st.set_page_config(page_title="Connector Health", layout="wide")
dsn = os.getenv("DATABASE_URL")
if not dsn:
    st.error("DATABASE_URL not set")
    st.stop()

conn = psycopg2.connect(dsn)

st.title("Integration Reliability & Observability — Connector Health")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Latest runs")
    df = pd.read_sql("""
      select ended_at, connector_name, status, latency_ms, attempts, rate_limited, error_type
      from raw.connector_runs
      order by ended_at desc
      limit 50
    """, conn)
    st.dataframe(df, use_container_width=True)

with col2:
    st.subheader("Alerts")
    df = pd.read_sql("""
      select created_at, severity, connector_name, alert_type, message, recommended_action
      from raw.alerts
      order by created_at desc
      limit 50
    """, conn)
    st.dataframe(df, use_container_width=True)

st.subheader("Daily KPIs")
df = pd.read_sql("""
  select * from mart.connector_health_daily
  order by day desc, connector_name asc
  limit 200
""", conn)
st.dataframe(df, use_container_width=True)

st.subheader("Top failure reasons")
df = pd.read_sql("select * from mart.top_failure_reasons limit 50", conn)
st.dataframe(df, use_container_width=True)

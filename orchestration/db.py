import os
import psycopg2
from dotenv import load_dotenv

# Loads .env automatically for local dev
load_dotenv()

def get_conn():
    dsn = os.getenv("DATABASE_URL")
    if not dsn:
        raise RuntimeError("DATABASE_URL not set. Create .env from .env.example")
    return psycopg2.connect(dsn)

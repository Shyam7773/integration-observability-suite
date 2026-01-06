from orchestration.db import get_conn

def run_models():
    with open("models/marts.sql", "r", encoding="utf-8") as f:
        sql = f.read()
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(sql)

if __name__ == "__main__":
    run_models()

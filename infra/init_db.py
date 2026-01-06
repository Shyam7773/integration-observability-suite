import os
import psycopg2

def main():
    dsn = os.getenv("DATABASE_URL")
    if not dsn:
        raise RuntimeError("DATABASE_URL not set")

    with open("infra/init.sql", "r", encoding="utf-8") as f:
        sql = f.read()

    with psycopg2.connect(dsn) as conn, conn.cursor() as cur:
        cur.execute(sql)

    print("DB init OK")

if __name__ == "__main__":
    main()

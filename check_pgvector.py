import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

db_url = os.getenv("DATABASE_URL")

try:
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    cur.execute("SELECT extname FROM pg_extension WHERE extname = 'vector';")
    extension = cur.fetchone()
    if extension:
        print("pgvector extension is installed.")
    else:
        print("pgvector extension is NOT installed.")
    cur.close()
    conn.close()
except Exception as e:
    print(f"Error: {e}")

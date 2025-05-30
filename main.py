import asyncio
import aiohttp
import psycopg
from urllib.parse import quote

# --- 🔐 Configuration ---
TAVILY_API_KEY = "Enter Key"
PG_USER = "postgres"
PG_PASSWORD = "admin1234"
PG_HOST = "localhost"
PG_PORT = "5432"
PG_DB = "postgres"

# Encode password safely
pg_password_escaped = quote(PG_PASSWORD)
POSTGRES_URL = f"postgresql://{PG_USER}:{pg_password_escaped}@{PG_HOST}:{PG_PORT}/{PG_DB}"

# --- 🛠 Create table and insert query ---
CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS tavily_results (
    id SERIAL PRIMARY KEY,
    query TEXT NOT NULL,
    url TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

INSERT_SQL = """
INSERT INTO tavily_results (query, url, content) VALUES (%s, %s, %s);
"""

# --- 🔍 Tavily search ---
async def search_tavily(query: str, max_results: int = 5):
    url = "https://api.tavily.com/search"
    headers = {"Content-Type": "application/json"}
    payload = {
        "api_key": TAVILY_API_KEY,
        "query": query,
        "search_depth": "basic",
        "max_results": max_results
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as resp:
            if resp.status != 200:
                raise Exception(f"Tavily error: {resp.status}")
            return (await resp.json())["results"]

# --- 💾 Store to Postgres ---
def store_results(query, results):
    with psycopg.connect(POSTGRES_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(CREATE_TABLE_SQL)
            for r in results:
                cur.execute(INSERT_SQL, (query, r["url"], r["content"]))
        conn.commit()
    print(f"✅ Stored {len(results)} result(s) to PostgreSQL")

# --- 🚀 Runner ---
async def run():
    query = input("🔍 Enter your Tavily search query: ").strip()
    results = await search_tavily(query)
    print(f"🧠 Top {len(results)} results from Tavily:")
    for r in results:
        print("-", r["url"])
    store_results(query, results)

if __name__ == "__main__":
    asyncio.run(run())

from mcp.server.fastmcp import FastMCP
import aiohttp
import psycopg
from urllib.parse import quote
import json

# FastMCP Setup 
mcp = FastMCP("MCPTools")

# Web Search Tool 
@mcp.tool()
async def search_web(query: str, max_results: int = 5) -> list:
    """Search the web using Tavily and return top results."""
    url = "https://api.tavily.com/search"
    headers = {"Content-Type": "application/json"}
    payload = {
        "api_key": "Enter Your API Key", #Enter API KEY 
        "query": query,
        "search_depth": "basic",
        "max_results": max_results
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as resp:
            data = await resp.json()
            return data["results"]

# 📂 PostgreSQL Storage Tool 
@mcp.tool()
def store_to_db(query: str, results: list) -> str:
    """Store Tavily results in PostgreSQL."""
    PG_USER = "postgres"
    PG_PASSWORD = "admin1234" # Enter Your Credentials
    PG_HOST = "localhost"
    PG_PORT = "5432"
    PG_DB = "postgres"

    pg_password_escaped = quote(PG_PASSWORD)
    POSTGRES_URL = f"postgresql://{PG_USER}:{pg_password_escaped}@{PG_HOST}:{PG_PORT}/{PG_DB}"

    with psycopg.connect(POSTGRES_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS tavily_results (
                    id SERIAL PRIMARY KEY,
                    query TEXT NOT NULL,
                    url TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            for r in results:
                cur.execute(
                    "INSERT INTO tavily_results (query, url, content) VALUES (%s, %s, %s);",
                    (query, r["url"], r["content"])
                )
        conn.commit()
    return f"Stored {len(results)} results."

# 📢 Slack Notification Tool 
@mcp.tool()
async def notify_slack(message: str) -> str:
    """Send a Slack message via webhook."""
    webhook_url = "Your Webhook url" # Generate Your own webhook url
    headers = {"Content-Type": "application/json"}
    payload = {"text": message}

    async with aiohttp.ClientSession() as session:
        async with session.post(webhook_url, headers=headers, data=json.dumps(payload)) as resp:
            if resp.status == 200:
                return "Message sent to Slack."
            else:
                return f"Failed to send Slack message. Status: {resp.status}"

#  Run the MCP Server ---
if __name__ == "__main__":
    mcp.run(transport="stdio")

# 🤖 MCP Agent: Web Search, DB Store, and Slack Notify

This project demonstrates a multi-tool AI agent using **LangGraph**, **FastMCP**, and **Streamlit**.

The agent can:
- 🔍 Search the web using Tavily API
- 💾 Store search results in a PostgreSQL database
- 📢 Notify a Slack channel with the results
  
## 📁 Project Structure

├── server.py # FastMCP server defining tools
├── client.py # Streamlit UI and agent runner
├── README.md # Setup guide

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/mcp-agent-app.git
cd mcp-agent-app
```

### 2. Create and Activate Virtual Environment

python3 -m venv venv
source venv/bin/activate       # Mac/Linux
# OR
venv\Scripts\activate          # Windows

### 3. Install Required Packages
Make sure your requirements.txt contains:

aiohttp
psycopg[binary]
streamlit
langchain
langgraph
langchain_openai
langchain_mcp_adapters
Then install:

bash
pip install -r requirements.txt


### 🔑 Configuration

### Tavily API Key
In server.py, update this line:

"api_key": "Enter Your API Key"
Get your key from Tavily.

### PostgreSQL Connection
Update credentials inside the store_to_db() tool in server.py:


PG_USER = "postgres"
PG_PASSWORD = "admin1234"
PG_HOST = "localhost"
PG_PORT = "5432"
PG_DB = "postgres"
Make sure PostgreSQL is installed and running locally.

### Slack Webhook URL
Update this line in notify_slack() in server.py:

webhook_url = "Your Webhook url"
You can create one from Slack Incoming Webhooks.: https://api.slack.com/messaging/webhooks

## Run the App

**Step 1: Start the Streamlit-Langgraph Client**
bash
streamlit run client.py

**Step 2: Run the Agent**
Enter your prompt in the input box (e.g. Search Latest Update on H1B VISA, store important info in SQL table and update on Slack)

Click 🔍 Run Agent Task

The app will:

1. Start the FastMCP server with tools

2. Use LangGraph agent to call tools as needed

3. Show log and final summary on screen

📌 Notes

The agent calls tools in sequence using LangGraph's ReAct pattern.

Streamlit shows intermediate logs and final summaries.

Output includes web results, DB insert confirmation, and Slack notification status.

### Feedback & Contributions
Feel free to open issues or submit PRs. Happy building!

Let me know if you’d like to auto-generate the `requirements.txt` file too.










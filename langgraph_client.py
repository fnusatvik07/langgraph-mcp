import streamlit as st
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from datetime import datetime
import json

# --- UI ---
st.set_page_config(page_title="MCP Agent Dashboard", layout="wide")
st.title("🤖 MCP Agent: Web Search, DB Store, and Slack Notify")

prompt = st.text_input("Enter your task for the agent:",
    value="Search Latest Update on H1B VISA, store important info in SQL table and update on Slack")

log_container = st.container()
summary_container = st.container()
log_text = []
summary_markdown = ""

# Logging function
def log(message: str):
    timestamp = datetime.now().strftime("%H:%M:%S")
    log_text.append(f"[{timestamp}] {message}")
    log_container.markdown("\n".join(f"- {line}" for line in log_text[-15:]), unsafe_allow_html=True)

# Render a readable summary
def render_summary(results):
    global summary_markdown
    summary_markdown = ""  # Reset for fresh run
    summary_markdown += "### 📝 Agent Summary\n"

    if isinstance(results, dict):
        steps = results.get("intermediate_steps", [])
        for step in steps:
            name = step.get("tool", "Unknown Tool")
            output = step.get("output", "").strip()
            if not output:
                continue
            summary_markdown += f"**🔧 Tool Used:** `{name}`\n\n"
            try:
                if name == "search_web":
                    parsed_output = json.loads(output)
                    summary_markdown += "**🔗 Top Web Results:**\n"
                    for item in parsed_output:
                        title = item.get("title", "No Title")
                        url = item.get("url", "")
                        content = item.get("content", "")
                        summary_markdown += f"- **[{title}]({url})**<br>{content[:300]}...\n"
                elif name == "store_to_db":
                    summary_markdown += f"**💾 Database Update:**\n{output}\n"
                elif name == "notify_slack":
                    summary_markdown += f"**📢 Slack Notification:**\n{output}\n"
                else:
                    summary_markdown += f"**📄 Output Preview:**\n{output}\n"
            except Exception as e:
                summary_markdown += f"**📄 Output (raw):**\n{output}\n"

        final_text = results.get("output", "").strip()
        if final_text:
            summary_markdown += "---\n**🧠 Final Summary by Agent:**\n"
            summary_markdown += f"{final_text}\n"

        summary_container.markdown(summary_markdown, unsafe_allow_html=True)

if st.button("🔍 Run Agent Task"):
    result_placeholder = st.empty()

    async def run_agent():
        log("Connecting to MCP Server and loading tools...")

        client = MultiServerMCPClient({
            "mcp_tools": {
                "command": "python",
                "args": ["/Users/datasense/Desktop/mcp-langgraph/server.py"],
                "transport": "stdio"
            }
        })

        tools = await client.get_tools()
        log("✅ Tools Loaded: " + ", ".join(tool.name for tool in tools))

        agent = create_react_agent(ChatOpenAI(model="gpt-4", temperature=0), tools)

        log("💬 Sending prompt to agent...")
        result = await agent.ainvoke({"messages": [{"role": "user", "content": prompt}]})

        log("📤 Final response from agent received.")

        # Show readable summary only
        render_summary(result)

    asyncio.run(run_agent())

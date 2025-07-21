import asyncio
import os
from dotenv import load_dotenv

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent

RETRY_INTERVAL = 5  # seconds
load_dotenv()

async def wait_for_server(client: MultiServerMCPClient):
    print("🔁 Waiting for MCP server to become available...")
    while True:
        try:
            tools = await client.get_tools()
            print("✅ MCP Tools loaded from server:")
            for t in tools:
                args = t.args_schema.get("properties", {})
                print(f" - {t.name} ({', '.join(args.keys()) if args else 'no args'})")
            return tools
        except Exception as e:
            print(f"⚠️ MCP server not ready yet ({e.__class__.__name__})... retrying in {RETRY_INTERVAL}s")
            await asyncio.sleep(RETRY_INTERVAL)


async def main():
    client = MultiServerMCPClient(
        {
            "aws": {
                "url": "http://localhost:8000/mcp",
                "transport": "streamable_http",
            }
        }
    )

    print("\n🤖 Agent is getting ready... just a second:")

    tools = await wait_for_server(client)
    print("\n✅ MCP Tools loaded from server:")


    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("Missing GROQ_API_KEY in .env")

    model = ChatGroq(model="meta-llama/llama-4-maverick-17b-128e-instruct")

    agent = create_react_agent(model, tools)

    print("\n🤖 Hi, Agent is now ready. Ask a question (or 'exit'):")

    while True:
        q = input("🦁 Ashish: ").strip()
        if q.lower() == "exit" or "bye":
            break
        if q:
            response = await agent.ainvoke({"messages": [{"role": "user", "content": q}]})
            print("🤖 Agent:", response["messages"][-1].content)
        else:
            print("⚠️ Uhho... You hit a wall... Please enter a valid query.")

if __name__ == "__main__":
    asyncio.run(main())

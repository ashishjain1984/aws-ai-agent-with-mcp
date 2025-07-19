# src/client/client_test_like.py

import asyncio
import os
from dotenv import load_dotenv

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent

load_dotenv()

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

    tools = await client.get_tools()
    print("\n✅ MCP Tools loaded from server:")

    for t in tools:
        args = t.args_schema.get("properties", {})
        print(f" - {t.name} ({', '.join(args.keys()) if args else 'no args'})")


    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("Missing GROQ_API_KEY in .env")

    model = ChatGroq(model="meta-llama/llama-4-maverick-17b-128e-instruct")

    agent = create_react_agent(model, tools)

    print("\n🤖 Hi, Agent is now ready. Ask a question (or 'exit'):")

    while True:
        q = input("🦁 Ashish: ").strip()
        if q.lower() == "exit":
            break
        if q:
            response = await agent.ainvoke({"messages": [{"role": "user", "content": q}]})
            print("🤖 Agent:", response["messages"][-1].content)
        else:
            print("⚠️ Uhho... You hit a wall... Please enter a valid query.")

if __name__ == "__main__":
    asyncio.run(main())

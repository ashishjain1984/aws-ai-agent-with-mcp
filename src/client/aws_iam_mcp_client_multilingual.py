# src/client/awc_iam_mcp_client_multilingual.py

import asyncio
import os
from dotenv import load_dotenv
from deep_translator import GoogleTranslator

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent

load_dotenv()

async def main():
    translator = GoogleTranslator(source='auto', target='en')

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

    print("\n🌐 You can now speak to AWS in Hindi, English, or any language! Type 'exit' to quit.\n")

    while True:
        user_input = input("🦁 आप: ").strip()
        if user_input.lower() == "exit":
            break

        if user_input:
            translated_input = translator.translate(user_input)

            # Run through agent
            response = await agent.ainvoke({
                "messages": [{"role": "user", "content": translated_input}]
            })

            agent_reply = response["messages"][-1].content

            # Translate back to original language
            back_translator = GoogleTranslator(source='en', target='hi')
            translated_output = back_translator.translate(agent_reply)

            print(f"🤖 Agent (translated): {translated_output}")
        else:
            print("⚠️ कृपया एक मान्य प्रश्न दर्ज करें। / Please enter a valid query.")

if __name__ == "__main__":
    asyncio.run(main())

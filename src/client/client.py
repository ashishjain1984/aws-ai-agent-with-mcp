from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
from langgraph.prebuilt import create_react_agent
import asyncio

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
    
    tools = await client.get_tools()
    
    for tool in tools:
        print(f"{tool.name}")
        for arg, props in tool.args_schema['properties'].items():
            print(f"  - {arg} (default: {props.get('default')})")


    api_key = os.environ.get("GROQ_API_KEY")
    if (api_key):
        os.environ["GROQ_API_KEY"] = api_key
    else:
        raise ValueError("GROQ_API_KEY is not set")

    model = ChatGroq(model="meta-llama/llama-4-maverick-17b-128e-instruct")

    agent = create_react_agent(
        model,
        tools,
    )

    while True:
        command = input("What are you looking for today in aws (or 'exit' to quit): ").strip()
        if command.lower() == 'exit':
            break
        if command:
            # Call the function to get data
            aws_response = await agent.ainvoke(
                {
                "messages": [
                        {
                            "role": "user", 
                            "content": command
                        }
                    ]
                }
            )

            print("Response:", aws_response['messages'][-1].content)
        else:
            print("Please enter a valid command.")



asyncio.run(main())

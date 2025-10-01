import asyncio
import json
from mcp import ClientSession
from mcp.client.sse import sse_client

async def main():
    # Connect to MCP Gateway which proxies NASDAQ MCP at this URL
    nasdaq_url = "http://localhost:8080/sse"
    
    # Use async context managers properly for sse transport and client session
    async with sse_client(nasdaq_url) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools_response = await session.list_tools()  # Lists all tools available from all backend servers via gateway
            print("Available tools through gateway:")
            for tool in tools_response.tools:
                print(f"- {tool.name}: {tool.description}")

            # Call a tool by name, gateway routes accordingly
            tool_name = "search_worldbank_indicators"
            args = {"keyword": "GDP"}

            print(f"\nCalling tool '{tool_name}' with arguments {args}...")
            result = await session.call_tool(tool_name, args)

            print(result.content[0].text)




if __name__ == "__main__":
    asyncio.run(main())

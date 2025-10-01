import asyncio
import json
from mcp import ClientSession
from mcp.client.sse import sse_client

async def main():
    # Connect to MCP Gateway which proxies NASDAQ MCP at this URL
    nasdaq_url = "http://localhost:8080/nasdaq/sse"
    
    # Use async context managers properly for sse transport and client session
    async with sse_client(nasdaq_url) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize MCP session handshake
            await session.initialize()
            
            # List all available tools from NASDAQ MCP server
            tools_response = await session.list_tools()
            print("Available NASDAQ MCP tools:")
            for tool in tools_response.tools:
                print(f"- {tool.name}: {tool.description}")
            
            # Example tool call - replace tool_name and args as per actual tools
            tool_name = "list_stock_stat_fields"
            args = {}
            
            print(f"\nCalling tool '{tool_name}' with arguments {args}...")
            result = await session.call_tool(tool_name, args)
            
            print("Tool call result:")
            print(result.content, indent=2)
            # if hasattr(result, 'content') and result.content:
            #     print(json.dumps(result.content, indent=2))
            # else:
            #     print(result)

if __name__ == "__main__":
    asyncio.run(main())

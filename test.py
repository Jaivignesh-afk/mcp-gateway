import asyncio
import hashlib
import requests
from mcp import ClientSession
from mcp.client.sse import sse_client
import os
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env file

ZERODHA_API_KEY = os.getenv("KITE_API_KEY")
ZERODHA_API_SECRET = os.getenv("API_SECRET")
ZERODHA_REDIRECT_URI = os.getenv("ZERODHA_REDIRECT_URI")
 # Must match your app settings

def generate_checksum(api_key: str, request_token: str, api_secret: str) -> str:
    msg = api_key + request_token + api_secret
    return hashlib.sha256(msg.encode()).hexdigest()

def get_access_token(request_token: str) -> str:
    url = "https://api.kite.trade/session/token"
    checksum = generate_checksum(ZERODHA_API_KEY, request_token, ZERODHA_API_SECRET)
    payload = {
        "api_key": ZERODHA_API_KEY,
        "request_token": request_token,
        "checksum": checksum
    }
    headers = {"X-Kite-Version": "3"}
    resp = requests.post(url, data=payload, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    return data["data"]["access_token"]

async def main():
    # print("Open this URL in your browser to login and authorize:")
    # login_url = f"https://kite.zerodha.com/connect/login?v=3&api_key={ZERODHA_API_KEY}"
    # print(login_url)

    # request_token = input("After login, enter the request_token from redirect URL: ").strip()

    # try:
    #     access_token = get_access_token(request_token)
    # except Exception as e:
    #     print(f"Error obtaining access token: {e}")
    #     return

    # print(f"Access Token: {access_token}")
    # You can now pass access_token to MCP backend or environment as needed

    gateway_url = "http://localhost:8080/sse"
    async with sse_client(gateway_url) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools_response = await session.list_tools()
            print("Available tools through gateway:")
            for tool in tools_response.tools:
                print(f"- {tool.name}: {tool.description}")

            # tool_name = "get_stock_stats"
            # args = {"symbol": "MSFT"}

            # print(f"\nCalling tool '{tool_name}' with arguments {args}...")
            # result = await session.call_tool(tool_name, args)

            # for content in result.content:
            #     if getattr(content, "type", None) == "text":
            #         print(content.text)
                    # break

if __name__ == "__main__":
    asyncio.run(main())

import asyncio
from fastmcp import Client
from server import mcp

async def main():
    async with Client(mcp) as client:
        tools = await client.list_tools()
        print("Tools:", [t.name for t in tools])
        result = await client.call_tool("get_target_schema", {})
        print(result.data)

asyncio.run(main())
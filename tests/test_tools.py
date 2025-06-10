import pytest
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from mcp_server_gravitino.server import tools as tls


def make_server_params(**kwargs) -> StdioServerParameters:
    return StdioServerParameters(
        command="uv",
        args=[
            "--directory",
            "/Users/panchenxi/Work/Project/work/own/component/mcp-gravitino",
            "run",
            "--with",
            "fastmcp",
            "--with",
            "httpx",
            "--with",
            "mcp-server-gravitino",
            "python",
            "-m",
            "mcp_server_gravitino.server",
        ],
        env={
            "GRAVITINO_METALAKE": kwargs.get("GRAVITINO_METALAKE", "demo_metalake"),
            "GRAVITINO_URI": kwargs.get("GRAVITINO_URI", "http://localhost:8090"),
            "GRAVITINO_USERNAME": kwargs.get("GRAVITINO_USERNAME", "admin"),
            "GRAVITINO_PASSWORD": kwargs.get("GRAVITINO_PASSWORD", "admin"),
            "GRAVITINO_ACTIVE_TOOLS": kwargs.get("GRAVITINO_ACTIVE_TOOLS", "*"),
        },
    )


@pytest.mark.asyncio
async def test_activate_default_method():
    params = {
        "GRAVITINO_ACTIVE_TOOLS": "get_list_of_tables",
    }
    async with stdio_client(make_server_params(**params)) as (stdio, write):
        async with ClientSession(stdio, write) as session:
            await session.initialize()
            result = await session.list_tools()
            tools = result.tools
            assert len(tools) == 1
            assert tools[0].name == "get_list_of_tables"


@pytest.mark.asyncio
async def test_activate_two_method():
    params = {
        "GRAVITINO_ACTIVE_TOOLS": "get_list_of_tables, get_list_of_tags",
    }
    async with stdio_client(make_server_params(**params)) as (stdio, write):
        async with ClientSession(stdio, write) as session:
            await session.initialize()
            result = await session.list_tools()
            tools = result.tools
            assert len(tools) == 2
            assert tools[0].name == "get_list_of_tables" or tools[1].name == "get_list_of_tables"
            assert tools[0].name == "get_list_of_tags" or tools[1].name == "get_list_of_tags"


@pytest.mark.asyncio
async def test_activate_all_method():
    params = {
        "GRAVITINO_ACTIVE_TOOLS": "*",
    }
    async with stdio_client(make_server_params(**params)) as (stdio, write):
        async with ClientSession(stdio, write) as session:
            await session.initialize()
            result = await session.list_tools()
            tools = result.tools
            assert len(tools) == len(tls.__all__)

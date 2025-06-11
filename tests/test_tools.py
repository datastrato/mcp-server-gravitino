from unittest.mock import patch

import pytest
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.types import TextContent

from mcp_server_gravitino.server import tools as tls
from mcp_server_gravitino.server.test_helper import (
    LIST_CATALOG_TEST_RESPONSE,
    LIST_MODEL_TEST_RESPONSE,
    LIST_SCHEMA_TEST_RESPONSE,
)

DEFAULT_METALAKE = "demo_metalake"
DEFAULT_URI = "http://localhost:8090"
DEFAULT_USER = "admin"
DEFAULT_PASS = "admin"
DEFAULT_ACTIVE_TOOLS = "*"
DEFAULT_TEST = "False"


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
            "GRAVITINO_METALAKE": kwargs.get("GRAVITINO_METALAKE", DEFAULT_METALAKE),
            "GRAVITINO_URI": kwargs.get("GRAVITINO_URI", DEFAULT_URI),
            "GRAVITINO_USERNAME": kwargs.get("GRAVITINO_USERNAME", DEFAULT_USER),
            "GRAVITINO_PASSWORD": kwargs.get("GRAVITINO_PASSWORD", DEFAULT_PASS),
            "GRAVITINO_ACTIVE_TOOLS": kwargs.get("GRAVITINO_ACTIVE_TOOLS", DEFAULT_ACTIVE_TOOLS),
            "GRAVITINO_TEST": kwargs.get("GRAVITINO_TEST", DEFAULT_TEST),
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


@pytest.mark.asyncio
async def test_get_list_of_catalogs():
    params = {
        "GRAVITINO_TEST": "True",
    }
    async with stdio_client(make_server_params(**params)) as (stdio, write):
        async with ClientSession(stdio, write) as session:
            await session.initialize()
            result = await session.call_tool("get_list_of_catalogs", arguments={})

            validate_result(result)


@pytest.mark.asyncio
async def test_get_list_of_schemas():
    params = {
        "GRAVITINO_TEST": "True",
    }
    async with stdio_client(make_server_params(**params)) as (stdio, write):
        async with ClientSession(stdio, write) as session:
            await session.initialize()
            result = await session.call_tool(
                "get_list_of_schemas",
                arguments={
                    "catalog_name": "catalog",
                },
            )
            validate_result(result)


@pytest.mark.asyncio
async def test_get_list_of_tables():
    params = {
        "GRAVITINO_TEST": "True",
    }
    async with stdio_client(make_server_params(**params)) as (stdio, write):
        async with ClientSession(stdio, write) as session:
            await session.initialize()
            result = await session.call_tool(
                "get_list_of_tables",
                arguments={
                    "catalog_name": "catalog",
                    "schema_name": "schema",
                },
            )

            validate_result(result)


@pytest.mark.asyncio
async def test_get_list_of_models():
    params = {
        "GRAVITINO_TEST": "True",
    }
    async with stdio_client(make_server_params(**params)) as (stdio, write):
        async with ClientSession(stdio, write) as session:
            await session.initialize()
            result = await session.call_tool(
                "get_list_of_models",
                arguments={
                    "catalog_name": "catalog",
                    "schema_name": "schema",
                },
            )

            validate_result(result)


def validate_result(result) -> None:
    assert not result.isError

    content = result.content
    assert len(content) == 1
    item = content[0]
    assert item.type == "text"
    assert isinstance(item, TextContent)

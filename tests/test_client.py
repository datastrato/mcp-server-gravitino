import os

import pytest
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from mcp_server_gravitino.server import tools as tls


def make_server_params(**kwargs) -> StdioServerParameters:
    return StdioServerParameters(
        command="uv",
        args=[
            "--directory",
            f"{os.getcwd()}",
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
async def test_list_resources():
    async with stdio_client(make_server_params()) as (stdio, write):
        async with ClientSession(stdio, write) as session:
            await session.initialize()
            result = await session.list_resources()
            assert isinstance(result.resources, list)
            assert not result.resources


@pytest.mark.asyncio
async def test_list_resource_templates():
    async with stdio_client(make_server_params()) as (stdio, write):
        async with ClientSession(stdio, write) as session:
            await session.initialize()
            result = await session.list_resource_templates()
            assert isinstance(result.resourceTemplates, list)
            assert not result.resourceTemplates


@pytest.mark.asyncio
async def test_list_prompts():
    async with stdio_client(make_server_params()) as (stdio, write):
        async with ClientSession(stdio, write) as session:
            await session.initialize()
            result = await session.list_prompts()
            assert isinstance(result.prompts, list)
            assert not result.prompts


@pytest.mark.asyncio
async def test_list_tools():
    async with stdio_client(make_server_params()) as (stdio, write):
        async with ClientSession(stdio, write) as session:
            await session.initialize()
            result = await session.list_tools()
            assert isinstance(result.tools, list)
            assert len(result.tools) == len(tls.__all__)

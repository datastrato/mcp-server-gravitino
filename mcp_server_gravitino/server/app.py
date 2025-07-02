# Copyright 2024 Datastrato Pvt Ltd.
# This software is licensed under the Apache License version 2.
import os

import httpx
from fastmcp import FastMCP
from httpx import Response

from mcp_server_gravitino.server import tools
from mcp_server_gravitino.server.settings import Settings
from mcp_server_gravitino.server.test_helper import (
    LIST_CATALOG_TEST_RESPONSE,
    LIST_MODEL_TEST_RESPONSE,
    LIST_SCHEMA_TEST_RESPONSE,
    LIST_TABLE_TEST_RESPONSE,
    mock_httpx_client,
)


class GravitinoMCPServer:
    """mcp server for gravitino"""

    def __init__(self):
        self.test_enabled = os.getenv("GRAVITINO_TEST") == "True"
        self.metalake = metalake_name = os.getenv("GRAVITINO_METALAKE", "metalake_demo")

        self.mcp = FastMCP("Gravitino", dependencies=["httpx"])
        self.settings = Settings()
        self.session = self._create_session()

        self.mount_tools()

    def mount_tools(self) -> None:
        """
        Mount tools to mcp server

        Raises
        ------
        ValueError
            if tool not found
        """
        if not self.settings.active_tools:
            raise ValueError("No tools to mount")
        if self.settings.active_tools == "*":
            for tool in tools.__all__:
                register_tool = getattr(tools, tool)
                register_tool(self.mcp, self.session)
        else:
            for tool in self.settings.active_tools.split(","):
                if hasattr(tools, tool.strip()):
                    register_tool = getattr(tools, tool.strip())
                    register_tool(self.mcp, self.session)
                else:
                    raise ValueError(f"Tool {tool} not found", tool.strip())

    def run(self) -> None:
        """
        Run mcp server
        """
        self.mcp.run()

    def _create_session(self):
        if not self.test_enabled:
            return httpx.Client(
                base_url=self.settings.uri,
                headers=self.settings.authorization,
            )

        return mock_httpx_client(self.metalake, self.settings)

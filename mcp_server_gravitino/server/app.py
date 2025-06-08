# Copyright 2024 Datastrato Pvt Ltd.
# This software is licensed under the Apache License version 2.
import httpx
from fastmcp import FastMCP

from mcp_server_gravitino.server import tools
from mcp_server_gravitino.server.settings import Settings
from mcp_server_gravitino.server.tools.registry import TOOLS


class GravitinoMCPServer:
    """mcp server for gravitino"""

    def __init__(self):
        self.mcp = FastMCP("Gravitino", dependencies=["httpx"])
        self.settings = Settings()

        self.session = self._create_session()
        self.mount_tools()

    def _create_session(self):
        return httpx.Client(
            base_url=self.settings.uri,
            headers=self.settings.authorization,
        )

    def mount_tools(self):
        """
        Mount specific tools to the mcp server.
        If the active_tools is "*", all tools will be mounted.
        Otherwise, the active_tools will be mounted.
        Returns
        -------
        None
        """
        if not self.settings.active_tools:
            raise ValueError("No tools to mount")

        active = (
            TOOLS.keys()
            if self.settings.active_tools == "*"
            else [c.strip() for c in self.settings.active_tools.split(",")]
        )

        if unknown := [c for c in active if c.strip() not in TOOLS]:
            raise ValueError(f"Unknown tool category(s): {', '.join(unknown)}")

        for category in active:
            for tool_fn in TOOLS[category]:
                tool_fn(self.mcp, self.session)

    def run(self):
        """
        Run the mcp server.
        Returns
        -------
        None
        """
        self.mcp.run()

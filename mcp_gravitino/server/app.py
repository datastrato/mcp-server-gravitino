# Copyright 2024 Datastrato Pvt Ltd.
# This software is licensed under the Apache License version 2.
import httpx
from fastmcp import FastMCP

from mcp_gravitino.server import tools
from mcp_gravitino.server.settings import Settings


class GravitinoMCPServer:
    def __init__(self):
        self.mcp = FastMCP("Gravitino", dependencies=["httpx"])
        self.settings = Settings()

        self.session = self._create_session()
        self.mount_tools()

    def _create_session(self):
        session = httpx.Client(base_url=self.settings.uri, headers=self.settings.authorization)
        return session

    def mount_tools(self):
        if self.settings.active_tools:
            if self.settings.active_tools == "*":
                for tool in tools.__all__:
                    register_tool = getattr(tools, tool)
                    register_tool(self.mcp, self.session)
            else:
                for tool in self.settings.active_tools.split(","):
                    if hasattr(tools, tool):
                        register_tool = getattr(tools, tool)
                    register_tool(self.mcp, self.session)
                else:
                    raise ValueError(f"Tool {tool} not found")
        else:
            raise ValueError("No tools to mount")

    def run(self):
        self.mcp.run()

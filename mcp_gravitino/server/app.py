# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
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

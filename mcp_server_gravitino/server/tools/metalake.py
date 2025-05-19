# Copyright 2024 Datastrato Pvt Ltd.
# This software is licensed under the Apache License version 2.

from typing import Any

import httpx
from fastmcp import FastMCP


def get_list_of_metalakes(mcp: FastMCP, session: httpx.Client) -> None:
    """Get a list of metalake"""

    @mcp.tool(
        name="get_list_of_metalakes",
        description="Get a list of metalake",
        annotations={
            "readOnlyHint": True,
            "openWorldHint": True,
        },
    )
    def _get_list_of_metalakes() -> list[dict[str, Any]]:
        """
        Get a list of metalake.
        Returns
        -------
        list[dict[str, Any]]
            A list of dictionaries containing metalake details.
            - name: Name of the metalake.
            - comment: Comment about the metalake.
            - in-use: Whether the metalake is in use.
            - creator: Creator of the metalake.
            - createTime: Creation time of the metalake.
        """
        response = session.get("/api/metalakes")
        response.raise_for_status()

        response_json = response.json()
        metalakes = response_json.get("metalakes", [])
        return [
            {
                "name": metalake.get("name"),
                "comment": metalake.get("comment", ""),
                "in-use": metalake.get("in-use"),
                "creator": metalake.get("audit").get("creator"),
                "createTime": metalake.get("audit").get("createTime"),
            }
            for metalake in metalakes
        ]

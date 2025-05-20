# Copyright 2024 Datastrato Pvt Ltd.
# This software is licensed under the Apache License version 2.

# Table organizes data in rows and columns and is defined in a Database Schema.
from typing import Any

import httpx
from fastmcp import FastMCP

from mcp_server_gravitino.server.tools import metalake_name
from mcp_server_gravitino.server.tools.common_tools import CATALOG_TAG, DETAILS_TAG, LIST_OPERATION_TAG


def get_list_of_catalogs(mcp: FastMCP, session: httpx.Client):
    """Get a list of catalogs in the Metalake."""

    # https://gravitino.apache.org/docs/0.8.0-incubating/api/rest/list-catalogs
    @mcp.tool(
        name="get_list_of_catalogs",
        description="Get a list of catalogs in the Metalake.",
        tags={
            CATALOG_TAG,
            LIST_OPERATION_TAG,
            DETAILS_TAG,
        },
        annotations={
            "readOnlyHint": True,
            "openWorldHint": True,
        },
    )
    def _get_list_of_catalogs() -> list[dict[str, Any]]:
        """
        Get a list of catalogs in the Metalake. it returns a list of dictionaries containing catalog details.


        Returns
        -------
        list[dict[str, Any]]
            A list of dictionaries containing catalog details.
            - name: Name of the catalog.
            - type: Type of the catalog.
            - provider: Provider of the catalog.
            - comment: Comment about the catalog.
        """
        response = session.get(f"/api/metalakes/{metalake_name}/catalogs?details=true")
        response.raise_for_status()
        response_json = response.json()

        catalogs = response_json.get("catalogs", [])
        return [
            {
                "name": catalog.get("name"),
                "type": catalog.get("type"),
                "provider": catalog.get("provider"),
                "comment": catalog.get("comment"),
            }
            for catalog in catalogs
        ]

# Copyright 2024 Datastrato Pvt Ltd.
# This software is licensed under the Apache License version 2.

# Table organizes data in rows and columns and is defined in a Database Schema.
from typing import Any

import httpx
from fastmcp import FastMCP

from mcp_server_gravitino.server.tools import metalake_name
from mcp_server_gravitino.server.tools.common_tools import LIST_OPERATION_TAG, SCHEMA_TAG


def get_list_of_schemas(mcp: FastMCP, session: httpx.Client) -> None:
    """Get a list of schemas, filtered by catalog it belongs to."""

    # https://gravitino.apache.org/docs/0.8.0-incubating/api/rest/list-schemas
    @mcp.tool(
        name="get_list_of_schemas",
        description="Get a list of schemas, filtered by catalog it belongs to.",
        tags={
            SCHEMA_TAG,
            LIST_OPERATION_TAG,
        },
        annotations={
            "readOnlyHint": True,
            "openWorldHint": True,
        },
    )
    def _get_list_of_schemas(catalog_name: str) -> list[dict[str, Any]]:
        """
        Get a list of schemas, filtered by catalog it belongs to.

        Parameters
        ----------
        catalog_name : str
            Name of the catalog to filter by.

        Returns
        -------
        list[dict[str, Any]]
            List of schemas in the catalog. It contains the following keys:
            - name: Name of the schema.
            - namespace: Namespace of the schema.
        """
        response = session.get(f"/api/metalakes/{metalake_name}/catalogs/{catalog_name}/schemas")
        response.raise_for_status()
        response_json = response.json()

        identifiers = response_json.get("identifiers", [])
        return [
            {
                "name": ident.get("name"),
                "namespace": ".".join(ident.get("namespace")),
            }
            for ident in identifiers
        ]

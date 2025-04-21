# Copyright 2024 Datastrato Pvt Ltd.
# This software is licensed under the Apache License version 2.

# Table organizes data in rows and columns and is defined in a Database Schema.
import httpx
from fastmcp import FastMCP
from mcp_server_gravitino.server.tools import metalake_name

def get_list_of_catalogs(mcp: FastMCP, session: httpx.Client):
    # https://gravitino.apache.org/docs/0.8.0-incubating/api/rest/list-catalogs
    @mcp.tool(
        name="get_list_of_catalogs",
        description="Get a list of catalogs.",
    )
    def _get_list_of_catalogs():
        """
        Get a list of catalogs.
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


def get_list_of_schemas(mcp: FastMCP, session: httpx.Client):
    # https://gravitino.apache.org/docs/0.8.0-incubating/api/rest/list-schemas
    @mcp.tool(
        name="get_list_of_schemas",
        description="Get a list of schemas, filtered by catalog it belongs to.",
    )
    def _get_list_of_schemas(
            catalog_name: str
    ):
        """
        Get a list of schemas, filtered by catalog it belongs to.

        Args:
            catalog_name (str):  name of the catalog
        """
        response = session.get(f"/api/metalakes/{metalake_name}/catalogs/{catalog_name}/schemas")
        response.raise_for_status()
        response_json = response.json()

        identifiers = response_json.get("identifiers", [])
        return [
            {
                "name": ident.get("name"),
                "namespace":  ".".join(ident.get("namespace")),
            }
            for ident in identifiers
        ]

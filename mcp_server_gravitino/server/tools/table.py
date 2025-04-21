# Copyright 2024 Datastrato Pvt Ltd.
# This software is licensed under the Apache License version 2.

# Table organizes data in rows and columns and is defined in a Database Schema.
import httpx
from fastmcp import FastMCP
from mcp_server_gravitino.server.tools import metalake_name

def get_list_of_tables(mcp: FastMCP, session: httpx.Client):
    # https://gravitino.apache.org/docs/0.8.0-incubating/api/rest/list-tables
    @mcp.tool(
        name="get_list_of_tables",
        description="Get a list of tables, filtered by catalog and schema it belongs to.",
    )
    def _get_list_of_tables(
        catalog_name: str,
        schema_name: str,
    ):
        """
        Get a list of tables, optionally filtered by database it belongs to.
        """
        response = session.get(f"/api/metalakes/{metalake_name}/catalogs/{catalog_name}/schemas/{schema_name}/tables")
        response.raise_for_status()
        response_json = response.json()

        tables = response_json.get("identifiers", [])
        return [
            {
                "name": table.get("name"),
                "namespace":  ".".join(table.get("namespace")),
                "fullyQualifiedName": ".".join(table.get("namespace"))+"."+table.get("name"),
            }
            for table in tables
        ]


def _get_table_by_fqn_response(session: httpx.Client, fully_qualified_name: str):
    table_names = fully_qualified_name.split('.')
    #metalake=table_names[0]
    catalog_name = table_names[1]
    schema_name = table_names[2]
    table_name = table_names[3]
    response = session.get(f"/api/metalakes/{metalake_name}/catalogs/{catalog_name}/schemas/{schema_name}/tables/{table_name}")
    response.raise_for_status()
    return response.json()


def get_table_by_fqn(mcp: FastMCP, session: httpx.Client):
    # https://gravitino.apache.org/docs/0.8.0-incubating/api/rest/load-table
    @mcp.tool(
        name="get_table_by_fqn",
        description="Get a table by fully qualified table name.",
    )
    def _get_table_by_fqn(fully_qualified_name: str):
        """
        Get a table by fully qualified table name.

        Args:
            fully_qualified_name (str): Fully qualified name of the table
        """
        response = _get_table_by_fqn_response(session, fully_qualified_name)

        return {
            "name": response.get("table").get("name"),
            "fullyQualifiedName": fully_qualified_name,
            "comment": response.get("table").get("comment"),
        }


def get_table_columns_by_fqn(mcp: FastMCP, session: httpx.Client):
    @mcp.tool(
        name="get_table_columns_by_fqn",
        description="Get a table columns by fully qualified table name.",
    )
    def _get_table_columns_by_fqn(fully_qualified_name: str):
        """
        Get a table by fully qualified table name.

        Args:
            fully_qualified_name (str): Fully qualified name of the table
        """

        response = _get_table_by_fqn_response(session, fully_qualified_name)

        return {
            "name": response.get("table").get("name"),
            "fullyQualifiedName": fully_qualified_name,
            "comment": response.get("table").get("comment"),
            "columns": response.get("table").get("columns"),
        }

# Copyright 2024 Datastrato Pvt Ltd.
# This software is licensed under the Apache License version 2.

# Table organizes data in rows and columns and is defined in a Database Schema.
from typing import Any

import httpx
from fastmcp import FastMCP

from mcp_server_gravitino.server.tools import metalake_name
from mcp_server_gravitino.server.tools.common_tools import GET_OPERATION_TAG, LIST_OPERATION_TAG, TABLE_TAG


def get_list_of_tables(mcp: FastMCP, session: httpx.Client) -> None:
    """Get a list of tables, optionally filtered by database it belongs to."""

    # https://gravitino.apache.org/docs/0.8.0-incubating/api/rest/list-tables
    @mcp.tool(
        name="get_list_of_tables",
        description="Get a list of tables, filtered by catalog and schema it belongs to.",
        tags={
            TABLE_TAG,
            LIST_OPERATION_TAG,
        },
        annotations={
            "readOnlyHint": True,
            "openWorldHint": True,
        },
    )
    def _get_list_of_tables(
        catalog_name: str,
        schema_name: str,
    ) -> list[dict[str, Any]]:
        """
        Get a list of tables, filtered by catalog and schema it belongs to.

        Parameters
        ----------
        catalog_name : str
            Name of the catalog
        schema_name : str
            Name of the schema

        Returns
        -------
        list[dict[str, Any]]
            Returns a list of tables, it contains the following keys:
            - name: Name of the table
            - namespace: Namespace of the table
            - fullyQualifiedName: Fully qualified name of the table
        """
        response = session.get(f"/api/metalakes/{metalake_name}/catalogs/{catalog_name}/schemas/{schema_name}/tables")
        response.raise_for_status()
        response_json = response.json()

        tables = response_json.get("identifiers", [])
        return [
            {
                "name": table.get("name"),
                "namespace": ".".join(table.get("namespace")),
                "fullyQualifiedName": ".".join(table.get("namespace")) + "." + table.get("name"),
            }
            for table in tables
        ]


def get_table_by_fqn(mcp: FastMCP, session: httpx.Client) -> None:
    """Get a table by fully qualified table name."""

    # https://gravitino.apache.org/docs/0.8.0-incubating/api/rest/load-table
    @mcp.tool(
        name="get_table_by_fqn",
        description="Get a table by fully qualified table name.",
        tags={
            TABLE_TAG,
            GET_OPERATION_TAG,
        },
        annotations={
            "readOnlyHint": True,
            "openWorldHint": True,
        },
    )
    def _get_table_by_fqn(fully_qualified_name: str) -> dict[str, Any]:
        """
        Get a table by fully qualified table name.

        Parameters
        ----------
        fully_qualified_name : str
            Fully qualified name of the table

        Returns
        -------
        dict[str, Any]
            Returns a dictionary containing the following keys:
            - name: Name of the table
            - fullyQualifiedName: Fully qualified name of the table
            - comment: Comment of the table
        """
        response = _get_table_by_fqn_response(session, fully_qualified_name)

        return {
            "name": response.get("table").get("name"),
            "fullyQualifiedName": fully_qualified_name,
            "comment": response.get("table").get("comment"),
        }


def get_table_columns_by_fqn(mcp: FastMCP, session: httpx.Client) -> None:
    """Get a table columns by fully qualified table name."""

    @mcp.tool(
        name="get_table_columns_by_fqn",
        description="Get a table columns by fully qualified table name.",
        tags={
            TABLE_TAG,
            GET_OPERATION_TAG,
        },
        annotations={
            "readOnlyHint": True,
            "openWorldHint": True,
        },
    )
    def _get_table_columns_by_fqn(fully_qualified_name: str) -> dict[str, Any]:
        """
        Get a table columns by fully qualified table name.

        Parameters
        ----------
        fully_qualified_name : str
            Fully qualified name of the table

        Returns
        -------
        dict[str, Any]
            Returns a dictionary containing the following keys:
            - name: Name of the table
            - fullyQualifiedName: Fully qualified name of the table
            - comment: Comment of the table
            - columns: List of columns in the table, it contains the following keys:
                - name: Name of the column
                - type: Type of the column
                - nullable: If the column is nullable or not
                - autoIncrement: If the column is auto-incremented or not
        """

        response = _get_table_by_fqn_response(session, fully_qualified_name)

        return {
            "name": response.get("table").get("name"),
            "fullyQualifiedName": fully_qualified_name,
            "comment": response.get("table").get("comment"),
            "columns": response.get("table").get("columns"),
        }


def _get_table_by_fqn_response(session: httpx.Client, fully_qualified_name: str) -> Any:
    """
    Get a table by fully qualified table name.

    Parameters
    ----------
    session : httpx.Client
        HTTP client
    fully_qualified_name : str
        Fully qualified name of the table

    Returns
    -------
    Any
        Returns a dictionary containing the table details
    """
    table_names = fully_qualified_name.split(".")
    # metalake=table_names[0]
    catalog_name = table_names[1]
    schema_name = table_names[2]
    table_name = table_names[3]
    response = session.get(
        f"/api/metalakes/{metalake_name}/catalogs/{catalog_name}/schemas/{schema_name}/tables/{table_name}"
    )
    response.raise_for_status()
    return response.json()

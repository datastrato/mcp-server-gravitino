# Copyright 2024 Datastrato Pvt Ltd.
# This software is licensed under the Apache License version 2.
from typing import Optional

import httpx
from fastmcp import FastMCP

from mcp_server_gravitino.server.tools import metalake_name
from mcp_server_gravitino.server.tools.common_tools import LIST_OPERATION_TAG, TAG_OBJECT_TAG


def get_list_of_tags(mcp: FastMCP, session: httpx.Client):
    """Get a list of tags."""

    # https://gravitino.apache.org/docs/0.8.0-incubating/api/rest/list-tags
    @mcp.tool(
        name="get_list_of_tags",
        description="Get a list of tags, which can be used to classify the data assets.",
        tags={
            TAG_OBJECT_TAG,
            LIST_OPERATION_TAG,
        },
        annotations={
            "readOnlyHint": True,
            "openWorldHint": True,
        },
    )
    def _get_list_of_tags() -> list[dict[str, str]]:
        """
        Get the list of tags.

        Returns
        -------
        list[dict[str, str]]
            A list of tags, where each tag is represented as a dictionary with the following keys:
            - name: The name of the tag.
        """
        response = session.get(f"/api/metalakes/{metalake_name}/tags")
        response.raise_for_status()
        response_json = response.json()

        tags = response_json.get("names", [])
        return [
            {
                "name": f"{tag}",
            }
            for tag in tags
        ]


def associate_tag_to_table(mcp: FastMCP, session: httpx.Client) -> None:
    @mcp.tool(
        name="associate_tag_to_table",
        description="associate tag to table object",
        tags={
            TAG_OBJECT_TAG,
        },
        annotations={
            "readOnlyHint": False,
            "openWorldHint": True,
            "destructiveHint": True,
            "idempotentHint": True,
        },
    )
    def _associate_tag_to_table(tag_name: str, fully_qualified_name: str) -> dict[str, str]:
        """
        Associate a tag with a table by tag name and table's fully qualified name.

        Parameters
        ----------
        tag_name : str
            The name of the tag to be associated with the table
        fully_qualified_name : str
            Fully qualified name of the table


        Returns
        -------
        dict[str, str]
            If an error occurs, returns {"result": "error", "message": "error message"}.
            if successful, returns {"result": "success"}
        """
        if not fully_qualified_name:
            return {"result": "error", "message": "fully_qualified_name cannot be empty"}
        table_names = fully_qualified_name.split(".")
        if len(table_names) != 4:
            return {
                "result": "error",
                "message": "table fully_qualified_name should be in the format 'metalake.catalog.schema.table'",
            }

        # metalake = table_names[0]
        catalog_name = table_names[1]
        schema_name = table_names[2]
        table_name = table_names[3]

        qualified_name = f"{catalog_name}.{schema_name}.{table_name}"

        return _associate_tag_to_object(
            session=session, tag_name=tag_name, object_type="table", obj_qualified_name=qualified_name
        )


def associate_tag_to_column(mcp: FastMCP, session: httpx.Client) -> None:
    @mcp.tool(
        name="associate_tag_to_column",
        description="associate tag to a column object",
        tags={
            TAG_OBJECT_TAG,
        },
        annotations={
            "readOnlyHint": False,
            "openWorldHint": True,
            "destructiveHint": True,
            "idempotentHint": True,
        },
    )
    def _associate_tag_to_column(tag_name: str, table_fully_qualified_name: str, column_name: str) -> dict[str, str]:
        """
        Associate a tag with a column by tag name, table's fully qualified name and column name.

        Parameters
        ----------
        tag_name : str
            The name of the tag to be associated with the column
        table_fully_qualified_name : str
            Fully qualified name of the table
        column_name : str
            Name of the column

        Returns
        -------
        dict[str, str]
            If an error occurs, returns {"result": "error", "message": "error message"}.
            if successful, returns {"result": "success"}
        """
        if not table_fully_qualified_name:
            return {"result": "error", "message": "table_fully_qualified_name cannot be empty"}
        table_names = table_fully_qualified_name.split(".")
        if len(table_names) != 4:
            return {
                "result": "error",
                "message": "table_fully_qualified_name should be in the format 'metalake.catalog.schema.table'",
            }

        # metalake = table_names[0]
        catalog_name = table_names[1]
        schema_name = table_names[2]
        table_name = table_names[3]

        qualified_name = f"{catalog_name}.{schema_name}.{table_name}.{column_name}"

        return _associate_tag_to_object(
            session=session, tag_name=tag_name, object_type="column", obj_qualified_name=qualified_name
        )


def list_objects_by_tag(mcp: FastMCP, session: httpx.Client) -> None:
    """List the metadata objects with a given tag."""

    @mcp.tool(
        name="list_objects_by_tag",
        description="list the metadata objects which have a tag",
        tags={
            TAG_OBJECT_TAG,
            LIST_OPERATION_TAG,
        },
        annotations={
            "readOnlyHint": True,
            "openWorldHint": True,
        },
    )
    def _list_objects_by_tag(tag_name: str) -> dict[str, str] | list[dict[str, str]]:
        """
        List the metadata objects with a given tag.

        Parameters
        ----------
        tag_name : str
            The name of the tag

        Returns
        -------
        dict[str, str] | list[dict[str, str]]
            If an error occurs, returns {"result": "error", "message": "error message"}.
            if successful, returns a list of dictionaries, where each dictionary represents a metadata object,
            with the following keys:
            - fullName: The fully qualified name of the object
            - type: The type of the object
        """

        if not tag_name:
            return {"result": "error", "message": "tag_name cannot be empty"}

        response = session.get(f"/api/metalakes/{metalake_name}/tags/{tag_name}/objects")
        response.raise_for_status()
        response_json = response.json()

        meta_objects = response_json.get("metadataObjects", [])
        return [
            {
                "fullName": f"{obj.get('fullName')}",
                "type": f"{obj.get('type')}",
            }
            for obj in meta_objects
        ]


def _associate_tag_to_object(
    session: httpx.Client,
    tag_name: str,
    object_type: str,
    obj_qualified_name: str,
) -> dict[str, str]:
    # https://gravitino.apache.org/docs/0.8.0-incubating/api/rest/associate-tags
    """
    Associate a tag with an object by tag name, object type and object's qualified name.

    Parameters
    ----------
    session : httpx.Client
        HTTPX client to make the API call
    tag_name : str
        The name of the tag to be associated with the object
    object_type : str
        The type of the object to be associated with the tag
    obj_qualified_name : str
        The qualified name of the object to be associated with the tag

    Returns
    -------
    dict[str, str]
        Return a dictionary with the following keys:
        - result: "success" if the operation is successful, "error" otherwise
        - message: A message describing the result of the operation, only present if the result is "error"
    """

    if not tag_name:
        return {"result": "error", "message": "tag_name cannot be empty"}
    if not object_type:
        return {"result": "error", "message": "object_type cannot be empty"}
    if not obj_qualified_name:
        return {"result": "error", "message": "obj_qualified_name cannot be empty"}

    json_data = {"tagsToAdd": [tag_name]}
    try:
        response = session.post(
            f"/api/metalakes/{metalake_name}/objects/{object_type}/{obj_qualified_name}/tags", json=json_data
        )
        response.raise_for_status()
    except httpx.HTTPStatusError as http_err:
        return {"result": "error", "message": str(http_err)}
    except Exception as err:
        return {"result": "error", "message": str(err)}

    return {
        "result": "success",
    }

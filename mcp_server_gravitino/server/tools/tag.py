# Copyright 2024 Datastrato Pvt Ltd.
# This software is licensed under the Apache License version 2.
from typing import Dict, Optional

import httpx
from fastmcp import FastMCP

from mcp_server_gravitino.server.tools import metalake_name
from mcp_server_gravitino.server.tools.common_tools import (
    LIST_OPERATION_TAG,
    TAG_OBJECT_TAG,
    get_name_identifier_without_metalake,
)

_level_map: Dict[int, str] = {
    2: "catalog",
    3: "schema",
    4: "table",
    5: "column",
}


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


def associate_tag_to_entity(mcp: FastMCP, session: httpx.Client) -> None:
    """Associate a tag with a catalog, schema, table or column."""

    @mcp.tool(
        name="associate_tag_to_entity",
        description="Associate a tag with a catalog, schema, table or column.",
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
    def _associate_tag_to_entity(
        tag_name: str,
        fully_qualified_name: str,
    ) -> dict[str, str]:
        if not fully_qualified_name:
            return {"result": "error", "message": "fully_qualified_name cannot be empty"}

        names = fully_qualified_name.split(".")
        level = len(names)
        if level not in _level_map.keys():
            return {
                "result": "error",
                "message": "Invalid 'fully_qualified_name': it must refer to a catalog, schema, table or column.",
            }

        object_type = _get_object_type(level)
        qualified_name = get_name_identifier_without_metalake(fully_qualified_name)

        return _associate_tag_to_object(
            session=session,
            tag_name=tag_name,
            object_type=object_type,
            obj_qualified_name=qualified_name,
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


def _get_object_type(level: int) -> str:
    object_type = _level_map.get(level)
    if object_type is None:
        raise ValueError(f"Invalid level: {level}")

    return object_type

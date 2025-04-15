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
from mcp_gravitino.server.tools import metalake_name

def get_list_of_tags(mcp: FastMCP, session: httpx.Client):
    # https://gravitino.apache.org/docs/0.8.0-incubating/api/rest/list-tags
    @mcp.tool(
        name="get_list_of_tags",
        description="Get a list of tags, which can be used to classify the data assets.",
    )
    def _get_list_of_tags():
        """
        Get a list of tags.
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


def _associate_tag_to_object(session: httpx.Client,
                             tag_name: str,
                             object_type: str,
                             obj_qualified_name: str):
    # https://gravitino.apache.org/docs/0.8.0-incubating/api/rest/associate-tags

    """
        Associate a tag with a table by tag name and table's fully qualified name.

        Args:
            tag_name (str): The name of the tag to be associated with the table
            object_type (str): The type of the object (e.g., table, column)
            obj_qualified_name (str): object's fully qualified name of the table
        """
    if not tag_name:
        return {"result": "error", "message": "tag_name cannot be empty"}
    if not object_type:
        return {"result": "error", "message": "object_type cannot be empty"}
    if not obj_qualified_name:
        return {"result": "error", "message": "obj_qualified_name cannot be empty"}

    json_data = {
        "tagsToAdd": [tag_name]
    }
    try:
        response = session.post(f"/api/metalakes/{metalake_name}/objects/{object_type}/{obj_qualified_name}/tags",
                                json=json_data)
        response.raise_for_status()
    except httpx.HTTPStatusError as http_err:
        return {"result": "error", "message": str(http_err)}
    except Exception as err:
        return {"result": "error", "message": str(err)}

    return {
        "result": "success",
    }


def associate_tag_to_table(mcp: FastMCP, session: httpx.Client):
    @mcp.tool(
        name="associate_tag_to_table",
        description="associate tag to table object",
    )
    def _associate_tag_to_table(
            tag_name: str,
            fully_qualified_name: str):
        """
        Associate a tag with a table by tag name and table's fully qualified name.

        Args:
            tag_name (str): The name of the tag to be associated with the table
            fully_qualified_name (str): Fully qualified name of the table
        """
        if not fully_qualified_name:
            return {"result": "error", "message": "fully_qualified_name cannot be empty"}
        table_names = fully_qualified_name.split('.')
        if len(table_names) != 4:
            return {"result": "error", "message": "table fully_qualified_name should be in the format "
                                                  "'metalake.catalog.schema.table'"}

        #metalake = table_names[0]
        catalog_name = table_names[1]
        schema_name = table_names[2]
        table_name = table_names[3]

        qualified_name = f"{catalog_name}.{schema_name}.{table_name}"

        _associate_tag_to_object(session=session, tag_name=tag_name,object_type="table", obj_qualified_name=qualified_name)


def associate_tag_to_column(mcp: FastMCP, session: httpx.Client):
    @mcp.tool(
        name="associate_tag_to_column",
        description="associate tag to a column object",
    )
    def _associate_tag_to_column(
            tag_name: str,
            table_fully_qualified_name: str,
            column_name: str):
        """
        Associate a tag with a column by tag name, table's fully qualified name and the column's name.

        Args:
            tag_name (str): The name of the tag to be associated with the table
            table_fully_qualified_name (str): Fully qualified name of the table
            column_name (str): The name of the column to be associated with the table
        """
        if not table_fully_qualified_name:
            return {"result": "error", "message": "table_fully_qualified_name cannot be empty"}
        table_names = table_fully_qualified_name.split('.')
        if len(table_names) != 4:
            return {"result": "error", "message": "table_fully_qualified_name should be in the format "
                                                  "'metalake.catalog.schema.table'"}

        #metalake = table_names[0]
        catalog_name = table_names[1]
        schema_name = table_names[2]
        table_name = table_names[3]

        qualified_name = f"{catalog_name}.{schema_name}.{table_name}.{column_name}"

        _associate_tag_to_object(session=session, tag_name=tag_name, object_type="column", obj_qualified_name=qualified_name)


def list_objects_by_tag(mcp: FastMCP, session: httpx.Client):
        @mcp.tool(
            name="list_objects_by_tag",
            description="list the metadata objects which have a tag",
        )
        def _list_objects_by_tag(tag_name: str):
            """
            List the metadata object by tag name.

            Args:
                tag_name (str): The name of the tag to query
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
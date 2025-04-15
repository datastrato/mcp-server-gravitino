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

# Table organizes data in rows and columns and is defined in a Database Schema.
import httpx
from fastmcp import FastMCP
from mcp_gravitino.server.tools import metalake_name

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

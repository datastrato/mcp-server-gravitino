# Copyright 2024 Datastrato Pvt Ltd.
# This software is licensed under the Apache License version 2.

from typing import Any, List, Optional, Tuple

import httpx
from fastmcp import FastMCP

from mcp_server_gravitino.server.tools import metalake_name as global_metalake_name
from mcp_server_gravitino.server.tools.common_tools import parse_four_level_fqn


def get_list_of_models(mcp: FastMCP, session: httpx.Client) -> None:
    """List all models in the given catalog and schema."""

    @mcp.tool(
        name="get_list_of_models",
        description="List all models in the given catalog and schema.",
        tags={
            "model",
            "list operation",
        },
    )
    def _get_list_of_models(
        catalog_name: str,
        schema_name: str,
    ) -> list[dict[str, Any]]:
        """
        List all models in the given catalog and schema.

        Parameters
        ----------
        catalog_name : str
            Name of the catalog.
        schema_name : str
            Name of the schema.

        Returns
        -------
        list[dict[str, Any]]
            A list of models, each represented as:
            - name: Name of the model
            - namespace:  Dot-separated namespace string, e.g. "catalog.schema".
            - fullyQualifiedName: Fully qualified name of the model
        """
        response = session.get(
            f"/api/metalakes/{global_metalake_name}/catalogs/{catalog_name}/schemas/{schema_name}/models"
        )
        response.raise_for_status()
        response_json = response.json()

        models = response_json.get("identifiers", [])
        return [
            {
                "name": model.get("name"),
                "namespace": ".".join(model.get("namespace")),
                "fullyQualifiedName": ".".join(model.get("namespace")) + "." + model.get("name"),
            }
            for model in models
        ]


def get_list_of_model_versions_by_fqn(mcp: FastMCP, session: httpx.Client) -> None:
    """List all model versions by fully qualified model name."""

    @mcp.tool(
        name="get_list_model_versions_by_fqn",
        description="List all versions of a model identified by its fully qualified name.",
        tags={
            "model version",
            "list operation",
        },
    )
    def _list_model_versions_by_fqn(fqn: str) -> list[dict[str, Any]]:
        """
        List all versions of a model by its fully qualified name.

        Parameters
        ----------
        fqn : str
            Fully qualified model name, of the form 'catalog.schema.model'
            or 'metalake.catalog.schema.model'.

        Returns
        -------
        list[dict[str, Any]]
            A list of versions, each represented as:
            - version: Version information
            - comment: Comment associated with the version
            - aliases: Aliases associated with the version
            - uri: URI of the version
            - creator: Creator of the version
        """
        metalake_name, catalog_name, schema_name, model_name = parse_four_level_fqn(fqn.split("."))
        if not metalake_name:
            metalake_name = global_metalake_name

        response = session.get(
            f"/api/metalakes/{metalake_name}/catalogs/{catalog_name}/schemas/{schema_name}/models/{model_name}/versions"
        )
        response.raise_for_status()
        response_json = response.json()
        versions = response_json.get("versions", [])

        version_objects = [
            _get_model_version_by_fqn_and_version_response(session, fqn, version).get("modelVersion")
            for version in versions
        ]

        return [
            {
                "version": obj.get("version"),
                "comment": obj.get("comment"),
                "aliases": ",".join(obj.get("aliases")),
                "uri": obj.get("uri"),
                "creator": obj.get("audit").get("creator"),
            }
            for obj in version_objects
        ]


def _get_model_version_by_fqn_and_version_response(session: httpx.Client, fully_qualified_name: str, version: str):
    """
    Get a model version by fully qualified model name and version.
    Parameters
    ----------
    session : httpx.Client
        HTTP client to make requests to Metalake API.
    fully_qualified_name : str
        Fully qualified name of the model.
    version : str
        Version of the model version.
    Returns
    -------
    dict
        Response from Metalake API.
    """
    model_names = fully_qualified_name.split(".")
    metalake_name, catalog_name, schema_name, model_name = parse_four_level_fqn(model_names)
    if not metalake_name:
        metalake_name = global_metalake_name

    response = session.get(
        f"/api/metalakes/{metalake_name}/catalogs/{catalog_name}/schemas/{schema_name}/models/{model_name}/versions/{version}"
    )
    response.raise_for_status()
    return response.json()

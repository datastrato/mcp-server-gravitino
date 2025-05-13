# Copyright 2024 Datastrato Pvt Ltd.
# This software is licensed under the Apache License version 2.

from typing import Any, List, Optional, Tuple

import httpx
from fastmcp import FastMCP

from mcp_server_gravitino.server.tools import metalake_name as global_metalake_name


def get_list_of_models(mcp: FastMCP, session: httpx.Client) -> None:
    """List all models in the given namespace"""

    @mcp.tool(
        name="get_list_of_models",
        description="List all models in the given namespace.",
        tags={
            "model",
            "list operation",
        },
    )
    def _get_list_of_models(namespace: str) -> list[dict[str, Any]]:
        """
        List all models in the given namespace.

        Parameters
        ----------
        namespace : str
            The namespace to list models from.

        Returns

        -------
        list[dict[str, Any]]
            List of models.
        """
        metalake_name, catalog_name, schema_name = _parse_namespace(namespace)
        if metalake_name is None:
            metalake_name = global_metalake_name

        response = session.get(f"/api/metalakes/{metalake_name}/catalogs/{catalog_name}/schemas/{schema_name}/models")
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


def get_model_by_fqn(mcp: FastMCP, session: httpx.Client) -> None:
    """Get a model by fully qualified table name."""

    @mcp.tool(
        name="get_model_by_fqn",
        description="Get a model by fully qualified table name.",
        tags={
            "model",
            "get operation",
        },
    )
    def _get_model_by_fqn(fully_qualified_name: str) -> dict[str, Any]:
        """
        Get a model by fully qualified table name.

        Parameters
        ----------
        fully_qualified_name : str
            The fully qualified name of the model.

        Returns
        -------
        dict[str, Any]
            The model details.
        """
        response_json = _get_model_by_fqn_response(session, fully_qualified_name)
        model = response_json.get("model")

        return {
            "name": model.get("name"),
            "comment": model.get("comment"),
            "latest version": model.get("latestVersion"),
            "creator": model.get("audit").get("creator"),
            "create time": model.get("audit").get("createTime"),
        }


def get_list_model_versions_by_fqn(mcp: FastMCP, session: httpx.Client) -> None:
    """List all model versions by fully qualified model name."""

    @mcp.tool(
        name="get_list_model_versions_by_fqn",
        description="List all model versions by using fully qualified model name.",
        tags={
            "model version",
            "list operation",
        },
    )
    def _list_model_versions_by_fqn(fqn: str) -> list[dict[str, Any]]:
        """
        List all model versions.

        Parameters
        ----------
        catalog_name : str
            The name of the catalog.
        schema_name : str
            The name of the schema.
        model_name : str
            The name of the model.

        Returns
        -------
        list[dict[str, Any]]
            List of model versions.
        """
        metalake_name, catalog_name, schema_name, model_name = _parse_four_level_fqn(fqn.split("."))
        if not metalake_name:
            metalake_name = global_metalake_name

        response = session.get(
            f"/api/metalakes/{metalake_name}/catalogs/{catalog_name}/schemas/{schema_name}/models/{model_name}/versions"
        )
        response.raise_for_status()
        response_json = response.json()
        versions = response_json.get("versions", [])

        return [
            {
                "version": version,
            }
            for version in versions
        ]


def get_model_version_by_fqn_and_alias(mcp: FastMCP, session: httpx.Client) -> None:
    """Get a model version by fully qualified model name and alias."""

    @mcp.tool(
        name="get_model_version_by_fqn_and_alias",
        description="Get a model version by fully qualified model name and alias.",
        tags={
            "model version",
            "get operation",
        },
    )
    def _get_model_version_by_fqn_and_alias(
        fully_qualified_name: str,
        alias: str,
    ) -> dict[str, Any]:
        """
        Get a model version by fully qualified model name and alias.

        Parameters
        ----------
        fully_qualified_name : str
            Fully qualified name of the model.
        alias : str
            Alias of the model version.

        Returns
        -------
        dict[str, Any]
            Model version details.
        """
        response_json = _get_model_version_by_fqn_and_alias_response(session, fully_qualified_name, alias)
        version = response_json.get("modelVersion")

        return {
            "version": version.get("version"),
            "comment": version.get("comment"),
            "aliases": ",".join(version.get("aliases")),
            "uri": version.get("uri"),
            "creator": version.get("audit").get("creator"),
        }


def get_model_version_by_fqn_and_version(mcp: FastMCP, session: httpx.Client) -> None:
    """Get a model version by fully qualified table name and version."""

    @mcp.tool(
        name="get_model_version_by_fqn_and_version",
        description="Get a model version by fully qualified table name and version.",
        tags={
            "model version",
            "get operation",
        },
    )
    def _get_model_version_by_fqn_and_version(
        fully_qualified_name: str,
        version: str,
    ) -> dict[str, Any]:
        """
        Get a model version by fully qualified table name and version.

        Parameters
        ----------
        fully_qualified_name : str
            Fully qualified name of the model.
        version : str
            Version of the model version.

        Returns
        -------
        dict[str, Any]
            Model version details.
        """
        response_json = _get_model_version_by_fqn_and_version_response(session, fully_qualified_name, version)
        version_dict = response_json.get("modelVersion")

        return {
            "version": version_dict.get("version"),
            "comment": version_dict.get("comment"),
            "aliases": ",".join(version_dict.get("aliases")),
            "uri": version_dict.get("uri"),
            "creator": version_dict.get("audit").get("creator"),
        }


def _get_model_by_fqn_response(session: httpx.Client, fully_qualified_name: str):
    """
    Get a model by fully qualified table name.

    Parameters
    ----------
    session : httpx.Client
        HTTP client to make requests to Metalake API.
    fully_qualified_name : str
        Fully qualified name of the model.

    Returns
    -------
    dict
        Response from Metalake API.
    """
    model_names = fully_qualified_name.split(".")
    model_names = fully_qualified_name.split(".")
    metalake_name, catalog_name, schema_name, model_name = _parse_four_level_fqn(model_names)
    if not metalake_name:
        metalake_name = global_metalake_name

    response = session.get(
        f"/api/metalakes/{metalake_name}/catalogs/{catalog_name}/schemas/{schema_name}/models/{model_name}"
    )
    response.raise_for_status()
    return response.json()


def _get_model_version_by_fqn_and_alias_response(session: httpx.Client, fully_qualified_name: str, alias: str):
    """
    Get a model version by fully qualified model name and alias.

    Parameters
    ----------
    session : httpx.Client
        HTTP client to make requests to Metalake API.
    fully_qualified_name : str
        Fully qualified name of the model.
    alias : str
        Alias of the model version.

    Returns
    -------
    dict
        Response from Metalake API.
    """
    model_names = fully_qualified_name.split(".")
    metalake_name, catalog_name, schema_name, model_name = _parse_four_level_fqn(model_names)
    if not metalake_name:
        metalake_name = global_metalake_name

    response = session.get(
        f"/api/metalakes/{metalake_name}/catalogs/{catalog_name}/schemas/{schema_name}/models/{model_name}/aliases/{alias}"
    )
    response.raise_for_status()
    return response.json()


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
    metalake_name, catalog_name, schema_name, model_name = _parse_four_level_fqn(model_names)
    if not metalake_name:
        metalake_name = global_metalake_name

    response = session.get(
        f"/api/metalakes/{metalake_name}/catalogs/{catalog_name}/schemas/{schema_name}/models/{model_name}/versions/{version}"
    )
    response.raise_for_status()
    return response.json()


def _parse_four_level_fqn(fqn: List[str]) -> Tuple[Optional[str], str, str, str]:
    """
    Parse the four-level fully qualified name.

    Args:
        fqn (List[str]): The splitted name list.

    Returns:
        Tuple[Optional[str], str, str, str]: The metalake name, catalog name, schema name, and xxx name.

    Raises:
        ValueError: If the input is not a four/three-level name.
    """
    if len(fqn) >= 4:
        return fqn[0], fqn[1], fqn[2], fqn[3]
    elif len(fqn) == 3:
        return None, fqn[0], fqn[1], fqn[2]
    else:
        raise ValueError("Invalid fully qualified name. Expected [catalog.schema.XXX] or [metalake.catalog.schema.XXX]")


def _parse_namespace(namespace: str) -> Tuple[Optional[str], str, str]:
    """
    Parse the namespace.

    Parameters
    ----------
    namespace : str
        The namespace to parse.

    Returns
    -------
    Tuple[Optional[str], str, str]
        The metalake name, catalog name, and schema name.

    Raises
    ------
    ValueError
        If the namespace is not a two/three-level name.
    """
    levels = namespace.split(".")
    if len(levels) >= 3:
        return levels[0], levels[1], levels[2]
    elif len(levels) == 2:
        return None, levels[0], levels[1]
    else:
        raise ValueError("Invalid namespace. Expected [catalog.schema] or [metalake.catalog.schema]")

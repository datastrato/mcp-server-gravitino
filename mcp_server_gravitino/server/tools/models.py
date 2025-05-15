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
            Namespace of the form 'catalog.schema' or 'metalake.catalog.schema'.

        Returns
        -------
        list[dict[str, Any]]
            A list of models, where each model contains:
            - name: Name of the model
            - namespace: Namespace of the model (catalog.schema)
            - fullyQualifiedName: Fully qualified name (metalake.catalog.schema.model or catalog.schema.model)
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
            - version: Version identifier
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


def _parse_four_level_fqn(fqn: List[str]) -> Tuple[Optional[str], str, str, str]:
    """
    Parse a fully qualified model name into its components.

    Parameters
    ----------
    fqn : List[str]
        The list obtained by splitting the model FQN by '.'

    Returns
    -------
    Tuple[Optional[str], str, str, str]
        A tuple of (metalake, catalog, schema, model).

    Raises
    ------
    ValueError
        If the name does not match the expected 3 or 4 level structure.
    """
    if len(fqn) >= 4:
        return fqn[0], fqn[1], fqn[2], fqn[3]
    elif len(fqn) == 3:
        return None, fqn[0], fqn[1], fqn[2]
    else:
        raise ValueError("Invalid fully qualified name. Expected [catalog.schema.XXX] or [metalake.catalog.schema.XXX]")


def _parse_namespace(namespace: str) -> Tuple[Optional[str], str, str]:
    """
    Parse a namespace string into its components.

    Parameters
    ----------
    namespace : str
        Namespace string, in the format 'catalog.schema' or 'metalake.catalog.schema'.

    Returns
    -------
    Tuple[Optional[str], str, str]
        Parsed result as (metalake, catalog, schema).

    Raises
    ------
    ValueError
        If the namespace is not valid.
    """
    levels = namespace.split(".")
    if len(levels) >= 3:
        return levels[0], levels[1], levels[2]
    elif len(levels) == 2:
        return None, levels[0], levels[1]
    else:
        raise ValueError("Invalid namespace. Expected [catalog.schema] or [metalake.catalog.schema]")

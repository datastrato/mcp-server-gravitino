# Copyright 2024 Datastrato Pvt Ltd.
# This software is licensed under the Apache License version 2.
import httpx
from fastmcp import FastMCP

from mcp_server_gravitino.server.tools import metalake_name
from mcp_server_gravitino.server.tools.common_tools import (
    GRANT_OPERATION_TAG,
    LIST_OPERATION_TAG,
    PRIVILEGES_TAG,
    REVOKE_OPERATION_TAG,
    ROLE_TAG,
    USER_TAG,
)


def get_list_of_roles(mcp: FastMCP, session: httpx.Client) -> None:
    """Get a list of role names, which can be used to manage access control."""

    # https://gravitino.apache.org/docs/0.8.0-incubating/api/rest/list-roles
    @mcp.tool(
        name="get_list_of_roles",
        description="Get a list of role names, which can be used to manage access control.",
        tags={
            LIST_OPERATION_TAG,
            ROLE_TAG,
        },
        annotations={
            "readOnlyHint": True,
            "openWorldHint": True,
        },
    )
    def _get_list_of_roles() -> list[dict[str, str]]:
        """
        Get a list of role names, which can be used to manage access control.

        Returns
        -------
        list[dict[str, str]]
            A list of role names, which can be used to manage access control, it contains the following fields:
            - name: The name of the role.
        """
        response = session.get(f"/api/metalakes/{metalake_name}/roles")
        response.raise_for_status()
        response_json = response.json()

        roles = response_json.get("names", [])
        return [
            {
                "name": f"{role}",
            }
            for role in roles
        ]


def get_list_of_users(mcp: FastMCP, session: httpx.Client) -> None:
    """Get a list of users, and the roles granted to the user."""

    # https://gravitino.apache.org/docs/0.8.0-incubating/api/rest/list-users
    @mcp.tool(
        name="get_list_of_users",
        description="Get a list of users, and the roles granted to the user.",
        tags={
            LIST_OPERATION_TAG,
            USER_TAG,
        },
        annotations={
            "readOnlyHint": True,
            "openWorldHint": True,
        },
    )
    def _get_list_of_users() -> list[dict[str, str]]:
        """
        Get a list of users, and the roles granted to the user.

        Returns
        -------
        list[dict[str, str]]
            A list of users, and the roles granted to the user, it contains the following fields:
            - name: The name of the user.
            - roles: The roles granted to the user.
        """
        response = session.get(f"/api/metalakes/{metalake_name}/users?details=true")
        response.raise_for_status()
        response_json = response.json()

        users = response_json.get("users", [])
        return [
            {
                "name": f"{user.get('name')}",
                "roles": f"{user.get('roles')}",
            }
            for user in users
        ]


def grant_role_to_user(mcp: FastMCP, session: httpx.Client) -> None:
    """Grant a role to an user."""

    @mcp.tool(
        name="grant_role_to_user",
        description="grant a role to an user",
        tags={
            USER_TAG,
            ROLE_TAG,
            PRIVILEGES_TAG,
            GRANT_OPERATION_TAG,
        },
        annotations={
            "readOnlyHint": False,
            "openWorldHint": True,
            "destructiveHint": True,
            "idempotentHint": False,
        },
    )
    def _grant_role_to_user(user_name: str, role_name: str) -> dict[str, str]:
        """
        Grant a role to an user.

        Parameters
        ----------
        user_name : str
            The name of the user.
        role_name : str
            The name of the role.

        Returns
        -------
        dict[str, str]
            A dictionary containing the result of the operation.
            - result: The result of the operation, either "success" or "error".
            - message: A message describing the result of the operation, only present if the result is "error".
        """
        if not user_name:
            return {"result": "error", "message": "user_name cannot be empty"}
        if not role_name:
            return {"result": "error", "message": "role_name cannot be empty"}

        json_data = {"roleNames": [role_name]}
        try:
            response = session.put(
                f"/api/metalakes/{metalake_name}/permissions/users/{user_name}/grant", json=json_data
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as http_err:
            return {"result": "error", "message": str(http_err)}
        except Exception as err:
            return {"result": "error", "message": str(err)}

        return {
            "result": "success",
        }


def revoke_role_from_user(mcp: FastMCP, session: httpx.Client):
    """Revoke a role from an user."""

    @mcp.tool(
        name="revoke_role_from_user",
        description="revoke a role from an user",
        tags={
            USER_TAG,
            ROLE_TAG,
            PRIVILEGES_TAG,
            REVOKE_OPERATION_TAG,
        },
        annotations={
            "readOnlyHint": False,
            "openWorldHint": True,
            "destructiveHint": True,
            "idempotentHint": False,
        },
    )
    def _revoke_role_from_user(user_name: str, role_name: str) -> dict[str, str]:
        """
        Revoke a role from an user.

        Parameters
        ----------
        user_name : str
            The name of the user.
        role_name : str
            The name of the role.

        Returns
        -------
        dict[str, str]
            A dictionary containing the result of the operation.
            - result: The result of the operation, either "success" or "error".
            - message: A message describing the result of the operation, only present if the result is "error".
        """

        if not user_name:
            return {"result": "error", "message": "user_name cannot be empty"}
        if not role_name:
            return {"result": "error", "message": "role_name cannot be empty"}

        json_data = {"roleNames": [role_name]}
        try:
            response = session.put(
                f"/api/metalakes/{metalake_name}/permissions/users/{user_name}/revoke", json=json_data
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as http_err:
            return {"result": "error", "message": str(http_err)}
        except Exception as err:
            return {"result": "error", "message": str(err)}

        return {
            "result": "success",
        }

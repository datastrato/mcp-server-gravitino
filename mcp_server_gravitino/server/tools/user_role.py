# Copyright 2024 Datastrato Pvt Ltd.
# This software is licensed under the Apache License version 2.
import httpx
from fastmcp import FastMCP
from mcp_server_gravitino.server.tools import metalake_name

def get_list_of_roles(mcp: FastMCP, session: httpx.Client):
    # https://gravitino.apache.org/docs/0.8.0-incubating/api/rest/list-roles
    @mcp.tool(
        name="get_list_of_roles",
        description="Get a list of role names, which can be used to manage access control.",
    )
    def _get_list_of_roles():
        """
        Get a list of roles.
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


def get_list_of_users(mcp: FastMCP, session: httpx.Client):
    # https://gravitino.apache.org/docs/0.8.0-incubating/api/rest/list-users
    @mcp.tool(
        name="get_list_of_users",
        description="Get a list of users, and the roles granted to the user.",
    )
    def _get_list_of_users():
        """
        Get a list of users.
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


def grant_role_to_user(mcp: FastMCP, session: httpx.Client):
    @mcp.tool(
        name="grant_role_to_user",
        description="grant a role to an user",
    )
    def _grant_role_to_user(
            user_name: str,
            role_name: str):
        """
        Grant a role to an user.

        Args:
            user_name (str): The name of the user
            role_name (str): The name of the role to be granted
        """
        if not user_name:
            return {"result": "error", "message": "user_name cannot be empty"}
        if not role_name:
            return {"result": "error", "message": "role_name cannot be empty"}

        json_data = {
            "roleNames": [role_name]
        }
        try:
            response = session.put(f"/api/metalakes/{metalake_name}/permissions/users/{user_name}/grant",
                                    json=json_data)
            response.raise_for_status()
        except httpx.HTTPStatusError as http_err:
            return {"result": "error", "message": str(http_err)}
        except Exception as err:
            return {"result": "error", "message": str(err)}

        return {
            "result": "success",
        }


def revoke_role_from_user(mcp: FastMCP, session: httpx.Client):
    @mcp.tool(
        name="revoke_role_from_user",
        description="revoke a role from an user",
    )
    def _revoke_role_from_user(
            user_name: str,
            role_name: str):
        """
        Revoke a role from an user.

        Args:
            user_name (str): The name of the user
            role_name (str): The name of the role to be revoked
        """
        if not user_name:
            return {"result": "error", "message": "user_name cannot be empty"}
        if not role_name:
            return {"result": "error", "message": "role_name cannot be empty"}

        json_data = {
            "roleNames": [role_name]
        }
        try:
            response = session.put(f"/api/metalakes/{metalake_name}/permissions/users/{user_name}/revoke",
                                   json=json_data)
            response.raise_for_status()
        except httpx.HTTPStatusError as http_err:
            return {"result": "error", "message": str(http_err)}
        except Exception as err:
            return {"result": "error", "message": str(err)}

        return {
            "result": "success",
        }

# Copyright 2024 Datastrato Pvt Ltd.
# This software is licensed under the Apache License version 2.
import os

metalake_name = os.getenv('GRAVITINO_METALAKE', 'metalake_demo')

from mcp_gravitino.server.tools.catalog import (
    get_list_of_catalogs,
    get_list_of_schemas,
)

from mcp_gravitino.server.tools.table import (
    get_list_of_tables,
    get_table_by_fqn,
    get_table_columns_by_fqn,
)

from mcp_gravitino.server.tools.tag import (
    get_list_of_tags,
    associate_tag_to_table,
    associate_tag_to_column,
    list_objects_by_tag,
)

from mcp_gravitino.server.tools.user_role import (
    get_list_of_roles,
    get_list_of_users,
    grant_role_to_user,
    revoke_role_from_user,
)


__all__ = [
    "get_table_by_fqn",
    "get_table_columns_by_fqn",
    "get_list_of_tables",
    "get_list_of_tags",
    "associate_tag_to_table",
    "associate_tag_to_column",
    "list_objects_by_tag",
    "get_list_of_catalogs",
    "get_list_of_schemas",
    "get_list_of_roles",
    "get_list_of_users",
    "grant_role_to_user",
    "revoke_role_from_user",
]

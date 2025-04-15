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

# MCP server for Apache Gravitino(incubating)

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

MCP server providing Gravitino APIs - A FastMCP integration for Apache Gravitino(incubating) services.

## Features

- Gravitino API integration with FastMCP
- Easy-to-use interface for metadata management
- Support for catalog/schema/table metadata, tag, and user-role information

## Installation

### from configuration
```json
{
    "mcpServers": {
        "Gravitino": {
            "command": "uv",
            "args": [
              "--directory",
              "/Users/user/workspace/mcp-server-gravitino",
                "run",
                "--with",
                "fastmcp",
                "--with",
                "httpx",
                "--with",
                "mcp-server-gravitino",
                "python",
                "-m",
                "mcp_server_gravitino.server"
            ],
            "env": {
                "GRAVITINO_URI": "http://localhost:8090",
                "GRAVITINO_USERNAME": "admin",
                "GRAVITINO_PASSWORD": "admin",
                "GRAVITINO_METALAKE": "metalake_demo"
            }
        }
    }
}
```

## Environment Variables

### Authorization
mcp-server-gravitino provides token auth and basic auth:

**Token Auth**
```
GRAVITINO_URI=http://localhost:8090
GRAVITINO_JWT_TOKEN=<YOUR GRAVITINO JWT TOKEN>
```

**Basic Auth**
```
GRAVITINO_URI=http://localhost:8090
GRAVITINO_USERNAME=<YOUR GRAVITINO USERNAME>
GRAVITINO_PASSWORD=<YOUR GRAVITINO PASSWORD>
```


## Tool list
mcp-server-gravitino does not provide all APIs available in Gravitino.

### Table Tools
- `get_list_of_catalogs`: Get a list of catalogs with basic information
- `get_list_of_schemas`: Get a list of schemas with basic information
- `get_list_of_tables`: Get a paginated list of tables with basic information
- `get_table_by_fqn`: Get detailed table information by fully qualified name
- `get_table_columns_by_fqn`: Get table columns information by fully qualified name

### Tag Tools
- `get_list_of_tags`: Get a list of tags with basic information
- `associate_tag_to_table`: Associate a tag to a table
- `associate_tag_to_column`: Associate a tag to a column
- `list_objects_by_tag`: Get a list of objects associated with a tag

### User Role Tools
- `get_list_of_roles`: Get a list of roles with basic information
- `get_list_of_users`: Get a list of users with basic information
- `grant_role_to_user`: Grant a role to a user
- `revoke_role_from_user`: Revoke a role from a user

Each tool returns optimized responses with relevant fields to ensure compatibility with model context limits while providing essential metadata information.


## License

This project is open source software [licensed as Apache License Version 2.0](LICENSE).

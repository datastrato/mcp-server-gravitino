[![MseeP.ai Security Assessment Badge](https://mseep.net/pr/datastrato-mcp-server-gravitino-badge.png)](https://mseep.ai/app/datastrato-mcp-server-gravitino)

# MCP Server for Apache Gravitino

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

MCP server providing Gravitino APIs - A FastMCP integration for Apache Gravitino services.

## Features

* Seamless integration with [FastMCP](https://github.com/jlowin/fastmcp) for Gravitino APIs
* Simplified interface for metadata interaction
* Supports metadata operations for catalogs, schemas, tables, models, users, tags, and user-role management

## Installation

This project uses [uv](https://github.com/astral-sh/uv) as the dependency and virtual environment management tool. Please ensure `uv` is installed on your system.

1. Clone the repository:

   ```bash
   git clone git@github.com:datastrato/mcp-server-gravitino.git
   ```

2. Navigate into the project directory:

   ```bash
   cd mcp-server-gravitino
   ```

3. Create a virtual environment:

   ```bash
   uv venv
   ```

4. Activate the virtual environment:

   ```bash
   source .venv/bin/activate
   ```

5. Install dependencies:

   ```bash
   uv install
   ```

## Configuration

### Common Configuration

Regardless of the Authorization, the following environment variables need to be set:

```bash
GRAVITINO_METALAKE=<YOUR_METALAKE> # default: "metalake_demo"
GRAVITINO_URI=<YOUR_GRAVITINO_URI>
```

* `GRAVITINO_URI`: The base URL of your Gravitino server.
* `GRAVITINO_METALAKE`: The name of the metakube to use.

### Authorization

`mcp-server-gravitino` supports both token-based and basic authentication methods. These mechanisms allow secure access to MCP tools and prompts and are suitable for integration with external systems.

#### Token Authentication

Set the following environment variables:

```bash
GRAVITINO_JWT_TOKEN=<YOUR_GRAVITINO_JWT_TOKEN>
```

`GRAVITINO_JWT_TOKEN`: The JWT token for authentication.

#### Basic Authentication

Alternatively, you can use basic authentication:

```bash
GRAVITINO_USERNAME=<YOUR_GRAVITINO_USERNAME>
GRAVITINO_PASSWORD=<YOUR_GRAVITINO_PASSWORD>
```

* `GRAVITINO_USERNAME`: The username for Gravitino authentication.
* `GRAVITINO_PASSWORD`: The corresponding password.

### Tool Activation

Tool activation is currently based on method names (e.g., `get_list_of_table`). You can specify which tools to activate by setting the optional environment variable `GRAVITINO_ACTIVE_TOOLS`. The default value is `*`, which activates all tools. If just want to activate `get_list_of_roles` tool, you can set the environment variable as follows:

```bash
GRAVITINO_ACTIVE_TOOLS=get_list_of_roles
```

## Usage

To launch the Gravitino MCP Server, run the following command:

```bash
uv \
--directory /path/to/mcp-gravitino \
run \
--with fastmcp \
--with httpx \
--with mcp-server-gravitino \
python -m mcp_server_gravitino.server
```

The meaning of each argument is as follows:

| Argument                                | Description                                                             |
| --------------------------------------- | ----------------------------------------------------------------------- |
| `uv`                                    | Launches the [UV](https://github.com/astral-sh/uv) CLI tool             |
| `--directory /path/to/mcp-gravitino`    | Specifies the working project directory with `pyproject.toml`           |
| `run`                                   | Indicates that a command will be executed in the managed environment    |
| `--with fastmcp`                        | Adds `fastmcp` to the runtime environment without altering project deps |
| `--with httpx`                          | Adds `httpx` dependency for async HTTP functionality                    |
| `--with mcp-server-gravitino`           | Adds the local module as a runtime dependency                           |
| `python -m mcp_server_gravitino.server` | Starts the MCP server using the package's entry module                  |

### Goose Client Example

Example configuration to run the server using Goose:

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

## Tool List

`mcp-server-gravitino` does not expose all Gravitino APIs, but provides a selected set of optimized tools:

### Table Tools

* `get_list_of_catalogs`: Retrieve a list of catalogs
* `get_list_of_schemas`: Retrieve a list of schemas
* `get_list_of_tables`: Retrieve a paginated list of tables
* `get_table_by_fqn`: Fetch detailed information for a specific table
* `get_table_columns_by_fqn`: Retrieve column information for a table

### Tag Tools

* `get_list_of_tags`: Retrieve all tags
* `associate_tag_to_entity`: Attach a tag to a table or column
* `list_objects_by_tag`: List objects associated with a specific tag

### User Role Tools

* `get_list_of_roles`: Retrieve all roles
* `get_list_of_users`: Retrieve all users
* `grant_role_to_user`: Assign a role to a user
* `revoke_role_from_user`: Revoke a user's role

### Model Tools

* `get_list_of_models`: Retrieve a list of models
* `get_list_of_model_versions_by_fqn`: Get versions of a model by fully qualified name

Each tool is designed to return concise and relevant metadata to stay within LLM token limits while maintaining semantic integrity.

## License

This project is licensed under the [Apache License Version 2.0](LICENSE).

# Copyright 2024 Datastrato Pvt Ltd.
# This software is licensed under the Apache License version 2.
import json
from pathlib import Path
from typing import Dict, Optional


def update_mcp_config(
    config_dir: Path,
    server_name: str,
    *,
    with_editable: Optional[Path] = None,
    with_packages: Optional[list[str]] = None,
    env_vars: Optional[Dict[str, str]] = None,
) -> bool:
    config_file = config_dir / "mcp.json"
    if not config_file.exists():
        config_file.write_text("{}")

    config = json.loads(config_file.read_text())
    if "mcpServers" not in config:
        config["mcpServers"] = {}

    # Always preserve existing env vars and merge with new ones
    if server_name in config["mcpServers"] and "env" in config["mcpServers"][server_name]:
        existing_env = config["mcpServers"][server_name]["env"]
        if env_vars:
            # New vars take precedence over existing ones
            env_vars = {**existing_env, **env_vars}
        else:
            env_vars = existing_env

    # Build uv run command
    args = ["run"]

    # Collect all packages in a set to deduplicate
    if with_editable:
        packages = {"fastmcp"}
    else:
        packages = {"fastmcp", "mcp-gravitino"}

    if with_packages:
        packages.update(pkg for pkg in with_packages if pkg)

    # Add all packages with --with
    for pkg in sorted(packages):
        args.extend(["--with", pkg])

    if with_editable:
        args.extend(["--with-editable", str(with_editable)])

    # Add fastmcp run command
    args.extend(["python", "-m", "mcp_server_gravitino.server"])

    server_config = {
        "command": "uv",
        "args": args,
    }

    # Add environment variables if specified
    if env_vars:
        server_config["env"] = env_vars

    config["mcpServers"][server_name] = server_config

    config_file.write_text(json.dumps(config, indent=2))

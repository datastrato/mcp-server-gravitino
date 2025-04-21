# Copyright 2024 Datastrato Pvt Ltd.
# This software is licensed under the Apache License version 2.
from mcp_server_gravitino.server.app import GravitinoMCPServer


def main():
    server = GravitinoMCPServer()
    server.run()


if __name__ == "__main__":
    main()

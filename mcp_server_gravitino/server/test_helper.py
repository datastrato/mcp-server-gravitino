# Copyright 2024 Datastrato Pvt Ltd.
# This software is licensed under the Apache License version 2.
import httpx
from httpx import MockTransport, Response

from mcp_server_gravitino.server.settings import Settings

LIST_CATALOG_TEST_RESPONSE = [
    {
        "name": "Hive_catalog",
        "type": "relational",
        "provider": "hive",
        "comment": "mock catalog",
    }
]
LIST_SCHEMA_TEST_RESPONSE = [
    {
        "name": "schema",
        "namespace": "demo_metalake.catalog",
    }
]
LIST_TABLE_TEST_RESPONSE = [
    {
        "name": "table1",
        "namespace": "demo_metalake.catalog.schema",
        "fullyQualifiedName": "demo_metalake.catalog.schema.table1",
    },
    {
        "name": "table2",
        "namespace": "demo_metalake.catalog.schema",
        "fullyQualifiedName": "demo_metalake.catalog.schema.table2",
    },
]
LIST_MODEL_TEST_RESPONSE = [
    {
        "name": "model1",
        "namespace": "demo_metalake.catalog.schema",
        "fullyQualifiedName": "demo_metalake.catalog.schema.model1",
    },
    {
        "name": "model2",
        "namespace": "demo_metalake.catalog.schema",
        "fullyQualifiedName": "demo_metalake.catalog.schema.model2",
    },
]


def mock_httpx_client(
    metalake: str,
    setting: Settings,
) -> httpx.Client:
    """
    Mock httpx client for testing

    Parameters
    ----------
    metalake : str
        The name of the metalake to mock.
    setting : Settings
        The settings to use for the mock.

    Returns
    -------
    httpx.Client
        The mocked httpx client.
    """

    def mock_handler(
        request: httpx.Request,
    ) -> Response:
        if request.method == "GET":
            # mock catalogs
            if request.url.path == f"/api/metalakes/{metalake}/catalogs":
                return Response(
                    200,
                    json={
                        "catalogs": LIST_CATALOG_TEST_RESPONSE,
                    },
                )
            # mock schemas
            elif request.url.path == f"/api/metalakes/{metalake}/catalogs/catalog/schemas":
                return Response(
                    200,
                    json={
                        "identifiers": LIST_SCHEMA_TEST_RESPONSE,
                    },
                )
            # mock tables
            elif request.url.path == f"/api/metalakes/{metalake}/catalogs/catalog/schemas/schema/tables":
                return Response(
                    200,
                    json={
                        "identifiers": LIST_TABLE_TEST_RESPONSE,
                    },
                )
            # mock models
            elif request.url.path == f"/api/metalakes/{metalake}/catalogs/catalog/schemas/schema/models":
                return Response(
                    200,
                    json={
                        "identifiers": LIST_MODEL_TEST_RESPONSE,
                    },
                )

        return Response(404, json={"path": str(request.url)})

    return httpx.Client(transport=MockTransport(mock_handler), base_url=setting.uri)

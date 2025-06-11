# Copyright 2024 Datastrato Pvt Ltd.
# This software is licensed under the Apache License version 2.


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

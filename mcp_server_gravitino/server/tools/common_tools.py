# Copyright 2024 Datastrato Pvt Ltd.
# This software is licensed under the Apache License version 2.
from typing import List, Optional, Tuple


def parse_four_level_fqn(fqn: List[str]) -> Tuple[Optional[str], str, str, str]:
    """
    Parse a fully qualified name (FQN) with optional metalake prefix.

    Parameters
    ----------
    fqn : List[str]
        A list representing a fully qualified name. It should contain either:
        - 4 levels: [metalake_name, catalog_name, schema_name, entity_name]
        - 3 levels: [catalog_name, schema_name, entity_name]

    Returns
    -------
     Tuple[Optional[str], str, str, str]
        A tuple containing (metalake_name, catalog_name, schema_name, entity_name).
        If metalake_name is not provided, it will be returned as None.

    Raises
    ------
    ValueError
         If the FQN does not have 3 or 4 components.
    """
    if len(fqn) >= 4:
        return fqn[0], fqn[1], fqn[2], fqn[3]
    elif len(fqn) == 3:
        return None, fqn[0], fqn[1], fqn[2]
    else:
        raise ValueError(
            "Invalid fully qualified name. Expected [catalog_name.schema_name.entity_name] or [metalake_name.catalog_name.schema_name.entity_name]"
        )

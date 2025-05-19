# Copyright 2024 Datastrato Pvt Ltd.
# This software is licensed under the Apache License version 2.
from typing import List, Optional, Tuple


def parse_four_level_fqn(fqn: List[str]) -> Tuple[Optional[str], str, str, str]:
    """
    Parse a fully qualified model name into its components.

    Parameters
    ----------
    fqn : List[str]
        The list obtained by splitting the model FQN by '.'

    Returns
    -------
    Tuple[Optional[str], str, str, str]
        A tuple of (metalake, catalog, schema, model).

    Raises
    ------
    ValueError
        If the name does not match the expected 3 or 4 level structure.
    """
    if len(fqn) >= 4:
        return fqn[0], fqn[1], fqn[2], fqn[3]
    elif len(fqn) == 3:
        return None, fqn[0], fqn[1], fqn[2]
    else:
        raise ValueError("Invalid fully qualified name. Expected [catalog.schema.XXX] or [metalake.catalog.schema.XXX]")

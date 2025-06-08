# Copyright 2024 Datastrato Pvt Ltd.
# This software is licensed under the Apache License version 2.

import functools
from typing import Callable, Dict, List

# A dictionary to store the all tools.
TOOLS: Dict[str, List[Callable]] = {}


def register_tool(category: str):
    """
    Register a tool function to a category.
    Parameters
    ----------
    category : str
        The category to register the tool to.
    """

    def decorator(func: Callable) -> Callable:
        TOOLS.setdefault(category, []).append(func)
        return func

    return decorator

# Copyright 2024 Datastrato Pvt Ltd.
# This software is licensed under the Apache License version 2.

import functools
from typing import Callable, Dict, List

TOOLS: Dict[str, List[Callable]] = {}


def register_tool(category: str):
    def decorator(func: Callable) -> Callable:
        TOOLS.setdefault(category, []).append(func)
        return func

    return decorator

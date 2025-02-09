# Copyright (c) 2023 - 2025, AG2ai, Inc., AG2ai open-source projects maintainers and core contributors
#
# SPDX-License-Identifier: Apache-2.0

__all__ = ["export_module"]

import os
from typing import Callable, TypeVar

T = TypeVar("T")


def export_module(module: str) -> Callable[[T], T]:
    def decorator(cls: T) -> T:
        if os.getenv("ADD_PDOC_PLACEHOLDER_TO_MODULE") is None:
            return cls

        original_module = getattr(cls, "__module__", None)
        setattr(cls, "__module__", f"{original_module}__PDOC_PLACEHOLDER__{module}")
        return cls

    return decorator

"""The typenames file contains type aliases. These must be in a separate
file from __init__, because they must be present before importing from
others files and modules. This is because type aliases are not allowed to
precede imports in accordance with PEP 8-E402."""
#  MIT License
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import TypeAlias, Any, Union

Args: TypeAlias = Union[tuple[Any], list[Any]]
Kwargs: TypeAlias = dict[str, Any]
ArgTuple: TypeAlias = tuple[Args, Kwargs]
Value: TypeAlias = tuple[Any, Args, Kwargs]

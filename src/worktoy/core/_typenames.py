"""The typenames file contains type aliases. These must be in a separate
file from __init__, because they must be present before importing from
others files and modules. This is because type aliases are not allowed to
precede imports in accordance with PEP 8-E402."""
#  MIT License
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import TypeAlias, Any, Union, Callable


class MaybeMeta(type):
  """By registering CallMeMaybe as a type, it is recognized correctly by
  the searchKeys procedure"""

  def __instancecheck__(self, instance: Any) -> bool:
    """Setting CallMeMaybe as a member"""
    return True if instance is CallMeMaybe else False


CallMeMaybe: TypeAlias = Callable
Args: TypeAlias = Union[tuple[Any], list[Any]]
Kwargs: TypeAlias = dict[str, Any]
ArgTuple: TypeAlias = tuple[Args, Kwargs]
Value: TypeAlias = tuple[Any, Args, Kwargs]

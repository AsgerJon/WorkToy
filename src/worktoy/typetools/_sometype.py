"""SomeType is any object other than None"""
#  Copyright (c) 2023 Asger Jon Vistisen
#  MIT Licence
from __future__ import annotations

from typing import TypeAlias, Any, Never

AllArgs: TypeAlias = tuple[tuple[Any, ...], dict[str, Any]]


class SomeType:
  """SomeType is every object other than None"""

  @classmethod
  def __instancecheck__(cls, instance: Any) -> bool:
    """The instance check simply checks if the instance is None"""
    return False if instance is None else True

  def __new__(cls, *__, **_) -> Never:
    """SomeType should not be instantiated"""
    from worktoy.waitaminute import InstantiationError
    raise InstantiationError(cls)

  def __init__(self, *__, **_) -> None:
    from worktoy.waitaminute import InstantiationError
    raise InstantiationError(self.__class__)

  def __repr__(self) -> str:
    """String representation"""
    msg = """SomeType contains all object other than None."""
    return msg

  def __str__(self) -> str:
    """String representation"""
    msg = """SomeType contains all object other than None."""
    return msg

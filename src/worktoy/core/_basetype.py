"""WorkToy - Core - BaseType
Type collection class"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Never

from worktoy.core import ParsingClass, Function
from types import GenericAlias


class BaseType(ParsingClass):

  def __call__(self, *args, **kwargs) -> Never:
    """Illegal callable"""
    raise TypeError

  def __str__(self) -> str:
    """String Representation"""
    return str(self._signature)

  def __repr__(self) -> str:
    """Code Representation"""
    return str(self._signature)


class MetaTypeClass(type):
  """SO CLOSE"""

  def __new__(mcls,
              name: str,
              bases: tuple,
              nameSpace: dict,
              **kwargs) -> type:
    return super().__new__(mcls, name, bases, nameSpace, **kwargs)

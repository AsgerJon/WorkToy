"""DEFAULT holds an object that disappears when accessed."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from worktoy.meta import Zeroton


class DEFAULT(Zeroton):
  """DEFAULT is a class that holds an object that disappears when
  accessed."""

  __default_object__ = None
  __has_object__ = False

  def __class_call__(self, defaultObject: object) -> None:
    self.__default_object__ = defaultObject
    self.__has_object__ = True

  @classmethod
  def getDefaultObject(cls) -> Any:
    """Getter-function for the default object."""
    if cls.__has_object__:
      cls.__has_object__ = False
      return cls.__default_object__
    e = """The DEFAULT Zeroton holds no object!"""
    raise RuntimeError(e)

"""WorkDictMeta is a metaclass for use by the WorkDict class, which is
itself used by the WorkToy metaclass"""
#  MIT License
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from worktoy import CallMeMaybe


class WorkDictMeta(type):
  """WorkDictMeta is a metaclass for use by the WorkDict class, which is
  itself used by the WorkToy metaclass"""

  #  MIT License
  #  Copyright (c) 2023 Asger Jon Vistisen

  @classmethod
  def __prepare__(mcls, name, bases, **kwargs) -> dict:
    """Prepares the name space"""
    return {}

  def __new__(mcls,
              name: str,
              bases: tuple[type],
              nameSpace: dict[str, Any],
              **kwargs) -> dict:
    """Implements the class creation"""

  def __call__(cls, *args, **kwargs) -> Any:
    """Implementation of instance creation"""
    args = [*args, None, None]
    if isinstance(args[0], CallMeMaybe):
      cls.overload(args[0])
      return args[0]
    else:
      instance = cls.__call__(cls, *args, **kwargs)
      cls.__init__(instance, *args, **kwargs)
      return instance

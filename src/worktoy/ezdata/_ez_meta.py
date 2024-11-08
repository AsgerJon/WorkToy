"""EZMeta provides the metaclass used by the EZData. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.base import FastMeta

try:
  from typing import Any
except ImportError:
  Any = object


class EZMeta(FastMeta):
  """EZMeta provides the metaclass used by the EZData. """
  __field_name__ = None
  __field_owner__ = None

  def __set_name__(cls, owner: Any, name: str) -> None:
    """The '__set_name__' method sets the name of the field. """
    cls.__field_name__ = name
    cls.__field_owner__ = owner
    setattr(cls, '__name__', name)

  def __call__(cls, *args, **kwargs) -> Any:
    """The '__call__' method creates an instance of the class. """
    fallbackName = """EZDataClass"""
    name = kwargs.get('__name__', fallbackName)
    bases = (EZBase,)
    space = FastSpace(EZMeta, name, bases)
    for (key, val) in kwargs.items():
      if key.startswith('__') and key.endswith('__'):
        continue
      box = EZBox(val)
      space[key] = box
    return FastMeta(name, bases, space)

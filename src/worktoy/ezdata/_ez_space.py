"""EZSpace provides the namespace object class for the EZData class."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.base import FastSpace

try:
  from typing import Callable
except ImportError:
  Callable = object

from worktoy.desc import AttriBox


class EZSpace(FastSpace):
  """EZSpace provides the namespace object class for the EZData class."""

  def __setitem__(self, key: str, value: object) -> None:
    """This method sets the key, value pair in the namespace."""
    if self.getClassName() != 'EZData':
      if key == '__init__':
        e = """EZData subclasses are not permitted to implement the 
        '__init__' method!"""
        raise AttributeError(e)
    return FastSpace.__setitem__(self, key, value)

  @staticmethod
  def _initFactory(attriBoxes: list[tuple[str, AttriBox]]) -> Callable:
    """This factory creates the '__init__' method which automatically
    populates the AttriBox instances."""

    keys = [key for (key, box) in attriBoxes]

    def __init__(self, *args, **kwargs) -> None:
      """This automatically generated '__init__' method populates the
      AttriBox instances."""

      popKeys = []

      for (key, arg) in zip(keys, args):
        setattr(self, key, arg)
        popKeys.append(key)

      for key in keys:
        if key in kwargs:
          setattr(self, key, kwargs[key])
          if key not in popKeys:
            popKeys.append(key)

    return __init__

  def compile(self) -> dict:
    """The namespace created by the BaseNamespace class is updated with
    the '__init__' function created by the factory function."""
    namespace = FastSpace.compile(self)
    boxes = self._getFieldBoxes()
    newInit = self._initFactory(boxes)
    namespace['__init__'] = newInit
    return namespace

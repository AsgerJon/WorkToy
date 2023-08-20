"""Main class"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from icecream import ic

from worktoy.core import monoSpace

ic.configureOutput(includeContext=True)

Function = (lambda: None).__class__


class DescriptorType:
  """Dataclass like class"""

  def __init__(self, *args, **_) -> None:
    if not args:
      self._defVal = None
      self._type = None
    elif len(args) == 1:
      if isinstance(args[0], type):
        self._type = args[0]
      else:
        self._defVal = args[0]
        self._type = type(self._defVal)
    else:
      if all([isinstance(arg, type) for arg in args[:2]]):
        if type not in args[:2]:
          raise TypeError
        self._type = type
        self._defVal = args[0] if args[0] is not type else args[1]
      if any([isinstance(arg, type) for arg in args[:2]]):
        self._type = args[0] if isinstance(args[0], type) else args[1]
        self._defVal = args[1] if isinstance(args[0], type) else args[0]

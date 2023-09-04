"""WorkToy - MetaClass - Dispatcher
This module provides a dispatcher for use with overloaded functions."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from worktoy.core import Function


class Dispatcher:
  """WorkToy - MetaClass - Dispatcher
  This module provides a dispatcher for use with overloaded functions."""

  def __init__(self, *func: Function) -> None:
    self._funcs = [f for f in func]

  def __call__(self, *args) -> Any:
    for func in self._funcs:
      note = getattr(func, '__annotations__', None)
      if note is None:
        from worktoy.waitaminute import MissingAnnotationsError
        raise MissingAnnotationsError
      if len(args) == len(note.keys()):
        run = 1
        for arg, (key, typeName) in zip(args, note.items()):
          argTypeNames = [
            getattr(type(arg), '__qualname__', None),
            getattr(type(arg), '__name__', None),
            str(type(arg)),
          ]
          if typeName not in argTypeNames:
            run = 0
        if run:
          return func(*args)

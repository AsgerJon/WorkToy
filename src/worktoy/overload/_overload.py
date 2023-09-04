"""WorkToy - MetaClass - Overload"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.base import DefaultClass
from worktoy.core import Function


class OverLoad(DefaultClass):
  """Instances should specify how the overloader works."""

  def __init__(self, *args, **kwargs) -> None:
    DefaultClass.__init__(self, *args, **kwargs)
    self._types = self.maybeTypes(type, *args)

  def __call__(self, func: Function) -> Function:
    """Decorates the function"""
    setattr(func, '__overload_signature__', (*self._types,))
    return func

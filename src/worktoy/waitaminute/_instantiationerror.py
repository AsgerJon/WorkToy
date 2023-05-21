"""InstantiationError should be raised when an attempt is made to
instantiate a class which does not allow instantiation."""
#  MIT License
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.waitaminute import ExceptionCore


class InstantiationError(ExceptionCore):
  """InstantiationError should be raised when an attempt is made to
  instantiate a class which does not allow instantiation.
  #  Copyright (c) 2023 Asger Jon Vistisen
  #  MIT Licence"""

  def __init__(self, *args, **kwargs) -> None:
    ExceptionCore.__init__(self, *args, **kwargs)
    self._msg = '%s is not allowed to be instantiated!' % (self.insClass)

  def __str__(self, ) -> str:
    """String Representation"""
    return self._msg

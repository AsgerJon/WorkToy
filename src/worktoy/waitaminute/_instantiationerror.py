"""InstantiationError should be raised when an attempt is made to
instantiate a class which does not allow instantiation."""
#  MIT License
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn

from worktoy.stringtools import justify
from worktoy.waitaminute import ExceptionCore


class InstantiationError(ExceptionCore):
  """InstantiationError should be raised when an attempt is made to
  instantiate a class which does not allow instantiation.
  #  Copyright (c) 2023 Asger Jon Vistisen
  #  MIT Licence"""

  def __init__(self, *args, **kwargs) -> None:
    ExceptionCore.__init__(self, *args, **kwargs)

  def _createMsg(self, *args, **kwargs) -> NoReturn:
    """This method is responsible for building the message issued by the
    error. """
    self._msg = justify("""Attempted to instantiate a restricted class.""")

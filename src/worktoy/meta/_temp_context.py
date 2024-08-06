"""TempContext class allows an object to open a context in a new state
from which it then returns. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

try:
  from typing import Self
except ImportError:
  Self = object

from worktoy.meta import BaseObject


class TempContext(BaseObject):
  """TempContext class allows an object to open a context in a new state
  from which it then returns. """

  __enter_callable__ = None
  __exit_callable__ = None

  def _setEnterCallable(self, callMeMaybe: Callable) -> None:
    """Set the enter callable. """
    self.__enter_callable__ = callMeMaybe

  def __enter__(self, *args, **kwargs) -> Self:
    """Enter the context. """
    return self

  def __exit__(self, *args, **kwargs) -> None:
    """Exit the context. """

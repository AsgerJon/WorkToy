"""BadValue is a temporary custom exception used to create more
informative exceptions. """
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from . import _Attribute

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Optional, Self


class BadValue(Exception):
  """
  BadValue is a temporary custom exception used to create more
  informative exceptions.
  """

  __wrapped__ = _Attribute()

  def __init__(self, wrapped: Exception) -> None:
    """
    Initialize the BadValue instance.
    """
    self.__wrapped__ = wrapped
    Exception.__init__(self, )

  def __eq__(self, other: Exception) -> bool:
    """
    Check if the wrapped exception is equal to another exception.
    """
    if not isinstance(other, Exception):
      return False
    cls = type(self)
    if isinstance(other, cls):
      return True if self.__wrapped__ is other.__wrapped__ else False
    return True if self.__wrapped__ is other else False

  def unwrap(self, ) -> Exception:
    """
    Unwrap the wrapped exception.
    """
    return self.__wrapped__

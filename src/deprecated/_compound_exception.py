"""
CompoundException is a custom exception raised from multiple exceptions.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from . import _Attribute
from ..parse import maybe
from ..text import joinWords, monoSpace

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Self, Any, Iterator


class CompoundException(Exception):
  """
  CompoundException is a custom exception raised from multiple exceptions.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private variables
  __exception_list__ = None

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  def _getExceptionList(self, ) -> tuple[Exception, ...]:
    """Getter-function for the exceptions."""
    return maybe(self.__exception_list__, ())

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, *exceptions: Exception) -> None:
    """Initialize the CompoundException with the given exceptions."""
    self.__exception_list__ = exceptions
    infoSpec = """Encountered multiple exceptions: \n  %s"""
    excStr = '<br><tab>'.join(str(e) for e in self)
    info = monoSpace(infoSpec % excStr)
    Exception.__init__(self, info)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __iter__(self) -> Iterator[Exception]:
    """Iterate over the exceptions."""
    for exception in self._getExceptionList():
      yield exception

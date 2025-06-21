"""
HashError provides a custom exception raised to indicate an unexpected
hash value.

Provide expected value and then actual value to the constructor. If a
single value is provided, it is understood to be the actual unexpected
value.

"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from . import _Attribute

try:
  from typing import TYPE_CHECKING
except ImportError:  # pragma: no cover
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any, Self


class HashError(RuntimeError):
  """
  HashError provides a custom exception raised to indicate an unexpected
  hash value.
  """

  expectedValue = _Attribute()
  actualValue = _Attribute()

  @staticmethod
  def _getInfoNoValues() -> str:
    """Return the error message without values."""
    infoSpec = """Received unexpected hash value!"""
    return infoSpec

  @staticmethod
  def _getInfoOneValue(value: int) -> str:
    """Return the error message with one value. The given value is
    understood to be the actual value, not the expected value."""
    infoSpec = """Received unexpected hash value: %d!"""
    return infoSpec % value

  @staticmethod
  def _getInfoTwoValues(expected: int, actual: int) -> str:
    """Return the error message with two values."""
    infoSpec = """Received unexpected hash value: %d! Expected: %d!"""
    return infoSpec % (actual, expected)

  def _getInfo(self, ) -> str:
    """
    Parses the values to info specification.
    """
    if self.expectedValue is None and self.actualValue is None:
      return self._getInfoNoValues()
    if self.actualValue is None:
      return self._getInfoOneValue(self.expectedValue)
    if self.expectedValue is None:
      return self._getInfoNoValues()
    return self._getInfoTwoValues(self.expectedValue, self.actualValue)

  def __init__(self, *values) -> None:
    """
    Initialize the HashError exception.

    Args:
      values: int
        The expected and actual hash values.
    """
    intArgs = [i for i in values if isinstance(i, int)]
    self.expectedValue, self.actualValue = [*intArgs, None, None][:2]
    RuntimeError.__init__(self, self._getInfo())

  def __eq__(self, other: Any) -> bool:
    """
    Check if the other object is a HashError and has the same values.
    """
    cls = type(self)
    if not isinstance(other, cls):
      return False
    if self.expectedValue is None and self.actualValue is None:
      return True if self is other else False
    if self.actualValue is None and other.actualValue is None:
      return True if self.expectedValue == other.expectedValue else False
    if self.expectedValue is None and other.expectedValue is None:
      return True if self.actualValue == other.actualValue else False
    return False

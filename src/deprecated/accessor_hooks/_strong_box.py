"""
StrongBox subclasses 'WeakBox' by adding type guarding.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from ...core import unpack
from ...waitaminute import TypeException, UnpackException
from . import WeakBox

#  Below provides compatibility back to Python 3.7
try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any


class StrongBox(WeakBox):
  """
  StrongBox subclasses 'WeakBox' by adding type guarding.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables

  #  Fallback Variables

  #  Private Variables

  #  Public Variables

  #  Virtual Variables

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _typeGuard(self, value: Any) -> Any:
    """
    Raises 'TypeException' if the value is not 'None' and not an instance
    of the current field type.
    """
    if value is None:
      return
    fieldType = self.getFieldType()
    if not isinstance(value, fieldType):
      raise TypeException('value', value, fieldType, )
    return value

  def postGet(self, value: Any) -> Any:
    """
    If value is None, the 'WeakBox' attempts to instantiate the field
    type. Otherwise, this method does nothing.
    """
    return WeakBox.postGet(self, self._typeGuard(value))

  def postSet(self, newValue: Any, oldValue: Any) -> Any:
    """
    Caches the value on the instance at the private name of this
    descriptor.
    """
    return WeakBox.postSet(self, self._typeGuard(newValue), oldValue)

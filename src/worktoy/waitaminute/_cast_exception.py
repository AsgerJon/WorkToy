"""CastException is a custom exception raised to indicate a failure for
the 'Cast' class to cast a value to a target type."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from . import _Attribute

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any, Self, Iterator

  from ..static import Cast


class CastException(TypeError):
  """CastException is a custom exception raised to indicate a failure for
  the 'Cast' class to cast a value to a target type."""

  value = _Attribute()
  target = _Attribute()
  why = _Attribute()
  cast = _Attribute()

  def __init__(self, castObject: Cast, exception: Exception) -> None:
    """Initialize the CastException object."""
    self.cast = castObject
    self.value = castObject.__inner_value__
    self.target = castObject._getTargetType()
    self.why = exception

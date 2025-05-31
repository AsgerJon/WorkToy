"""AbstractDescriptor provides a common abstract baseclass for all
descriptor classes. """
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod

from ..static import AbstractObject
from ..waitaminute import MissingVariable

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any


class _MetaDescriptor(type):
  """MetaDescriptor is a metaclass for the AbstractDescriptor class."""

  def __getitem__(cls, fieldType: type) -> Any:
    """Get the field type."""
    self = cls()
    self._addFieldType(fieldType)
    return self


class AbstractDescriptor(AbstractObject):
  """AbstractDescriptor provides a common abstract baseclass for all
  descriptor classes. """
  pass

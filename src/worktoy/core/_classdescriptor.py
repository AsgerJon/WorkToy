"""WorkToy - Core - ClassDescriptor
Descriptor class for other classes and types."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Never

from worktoy.core import AbstractDescriptor


class ClassDescriptor(AbstractDescriptor):
  """WorkToy - Core - ClassDescriptor
  Descriptor class for other classes and types."""

  def __init__(self, *args, **kwargs) -> None:
    AbstractDescriptor.__init__(self, *args, **kwargs)
    self._valueType = type

  def explicitGetter(self, obj: object, cls: type) -> object:
    """Implement error check if called before class is set. """
    existing = AbstractDescriptor.explicitGetter(obj, self.getOwner())
    if existing is None:
      raise TypeError
    return existing

  def explicitSetter(self, obj: object, newValue: object) -> None:
    """Implements the write-once behaviour."""
    existing = AbstractDescriptor.explicitGetter(obj, self.getOwner())
    if existing is not None:
      raise TypeError
    AbstractDescriptor.explicitSetter(obj, newValue)

  def explicitDeleter(self, *_) -> Never:
    """Illegal deleter"""
    raise TypeError


CLASS = ClassDescriptor

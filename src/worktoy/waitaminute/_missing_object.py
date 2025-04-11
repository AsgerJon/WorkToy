"""MissingObject raised to indicate that an object is missing from the
descriptor box system."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.text import monoSpace

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False


class MissingObject(Exception):
  """MissingObject raised to indicate that an object is missing from the
  descriptor box system."""

  __owning_instance__ = None
  __owning_class__ = None
  __descriptor_instance__ = None

  def __init__(self, descriptor: object, instance: object) -> None:
    """Initialize the MissingObject exception."""
    self.__descriptor_instance__ = descriptor
    self.__owning_instance__ = instance
    self.__owning_class__ = type(instance)

    info = """Unable to retrieve: '%s.%s' object!"""
    ownerName = self.__owning_class__.__name__
    fieldName = getattr(descriptor, '__field_name__', None)
    Exception.__init__(self, monoSpace(info % (ownerName, fieldName)))

"""FilterException is raised by namespace filters to indicate that the
filter has not handled the key and value passed to the __setitem__ method."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any, Callable


class _Space:
  """Descriptor class for the __namespace_object__ attribute."""

  __attr_name__ = '__namespace_object__'

  def _getAttrName(self) -> str:
    """Get the name of the attribute."""
    return self.__attr_name__

  def __get__(self, instance: object, owner: type) -> Any:
    """Get the namespace object."""
    if instance is None:
      return self
    return getattr(instance, self._getAttrName(), )


class _Key:
  """Descriptor class for the __namespace_key__ attribute."""

  __attr_name__ = '__namespace_key__'

  def _getAttrName(self) -> str:
    """Get the name of the attribute."""
    return self.__attr_name__

  def __get__(self, instance: object, owner: type) -> Any:
    """Get the namespace key."""
    if instance is None:
      return self
    return getattr(instance, self._getAttrName(), )


class _Value:
  """Descriptor class for the __namespace_value__ attribute."""

  __attr_name__ = '__namespace_value__'

  def _getAttrName(self) -> str:
    """Get the name of the attribute."""
    return self.__attr_name__

  def __get__(self, instance: object, owner: type) -> Any:
    """Get the namespace value."""
    if instance is None:
      return self
    return getattr(instance, self._getAttrName(), )


class _FilterClass:
  """Descriptor class for the __filter_class__ attribute."""

  __attr_name__ = '__filter_class__'

  def _getAttrName(self) -> str:
    """Get the name of the attribute."""
    return self.__attr_name__

  def __get__(self, instance: object, owner: type) -> Any:
    """Get the filter class."""
    if instance is None:
      return self
    return getattr(instance, self._getAttrName(), )


class FilterException(Exception):
  """FilterException is raised by namespace filters to indicate that the
  filter has not handled the key and value passed to the __setitem__ method.
  """

  __namespace_object__ = None
  __namespace_key__ = None
  __namespace_value__ = None
  __filter_class__ = None

  namespaceObject = _Space()
  namespaceKey = _Key()
  namespaceValue = _Value()
  filterClass = _FilterClass()

  def __init__(
      self,
      space: dict,
      key: str,
      value: object,
      cls: type
  ) -> None:
    """Initialize the FilterException object."""
    self.__namespace_object__ = space
    self.__namespace_key__ = key
    self.__namespace_value__ = value
    self.__filter_class__ = cls
    info = """The filterClass: '%s' did not handle the call to __setitem__ 
    with key: '%s' and value: '%s'"""
    Exception.__init__(self, info % (cls, key, value))

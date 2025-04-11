"""FilterFunction wraps a method in a namespace class and implements
access to it through the descriptor protocol."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.waitaminute import ReadOnlyError

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any, Callable, Never


class FilterFunction:
  """FilterFunction wraps a method in a namespace class and implements
  access to it through the descriptor protocol. """

  __wrapped__ = None

  __field_name__ = None  # Should equal __wrapped__.__name__
  __field_owner__ = None  # The class whose body defines __wrapped__

  def __set_name__(self, owner: type, name: str) -> None:
    """Set the name of the field and the owner of the field."""
    self.__field_name__ = name
    self.__field_owner__ = owner

  def __init__(self, callMeMaybe: Callable) -> None:
    """Initialize the FilterFunction object."""
    self.__wrapped__ = callMeMaybe

  def __get__(self, instance: object, owner: type) -> Any:
    """Get the wrapped function. The owner is the class through which the
    descriptor is accessed. This is either __field_class__ or a subclass
    hereof. """
    if instance is None:
      return self.__wrapped__  # Unbound method

    def wrapped(*args, **kwargs):
      """Call the wrapped function."""
      return self.__wrapped__(instance, *args, **kwargs)

    return wrapped  # Bound method

  def __set__(self, instance: object, value: object) -> Never:
    """Set is not allowed on FilterFunction."""
    raise ReadOnlyError(instance, self, value)

  def __delete__(self, instance: object) -> Never:
    """Delete is not allowed on FilterFunction."""
    raise ReadOnlyError(instance, self, None)

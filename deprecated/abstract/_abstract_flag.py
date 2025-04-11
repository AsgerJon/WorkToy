"""AbstractFlag provides a descriptor protocol for a flag on classes and
functions that indicate abstractness. Specifically, a class with abstract
methods should have an instance of this flag indicate this. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.text import typeMsg
from worktoy.waitaminute import MissingVariable

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any, Callable
  from worktoy.mcls import CallMeMaybe


class _Name:
  """Private descriptor allowing attribute access to the name of the
  wrapped function. """

  def __get__(self, instance: object, owner: type) -> Any:
    """Get the name of the function."""
    if instance is None:
      return self
    if TYPE_CHECKING:
      assert isinstance(instance, AbstractFlag)
    return instance.__field_name__


class _Owner:
  """Private descriptor allowing attribute access to the owner of the
  wrapped function. """

  def __get__(self, instance: object, owner: type) -> Any:
    """Get the name of the function."""
    if instance is None:
      return self
    if TYPE_CHECKING:
      assert isinstance(instance, AbstractFlag)
    return instance.__field_owner__


class AbstractFlag:
  """AbstractFlag provides a descriptor protocol for a flag on classes and
  functions that indicate abstractness. Specifically, a class with abstract
  methods should have an instance of this flag indicate this. """

  __field_name__ = None
  __field_owner__ = None
  __getter_name__ = None

  fieldName = _Name()
  fieldOwner = _Owner()

  def __init__(self, *args) -> None:
    """Initialize the AbstractFlag object."""
    for arg in args:
      if isinstance(arg, str):
        self.__getter_name__ = arg
        break

  def __set_name__(self, owner: object, name: str) -> None:
    """Set the name of the field and the owner of the field."""
    self.__field_name__ = name
    self.__field_owner__ = owner

  def _getGetter(self, ) -> Callable:
    """Getter-function for the getter function."""
    if self.__getter_name__ is None:
      raise MissingVariable('__getter_name__', str)
    getter = getattr(self.__field_owner__, self.__getter_name__, None)
    if getter is None:
      raise MissingVariable(self.__getter_name__, Callable)
    if not callable(getter):
      raise TypeError(typeMsg(self.__getter_name__, getter, Callable))
    return getter

  def _setGetter(self, callMeMaybe: CallMeMaybe) -> None:
    """Set the getter function."""
    if isinstance(callMeMaybe, str):
      self.__getter_name__ = callMeMaybe
    elif callable(callMeMaybe):
      self.__getter_name__ = callMeMaybe.__name__
    else:
      raise TypeError(typeMsg('__getter_name__', callMeMaybe, Callable))

  def GET(self, callMeMaybe: CallMeMaybe) -> AbstractFlag:
    """Set the getter function."""
    self._setGetter(callMeMaybe)
    return self

  def __get__(self, instance: object, owner: type) -> Any:
    """Get the state of the flag."""
    if instance is None:
      return self
    getter = self._getGetter()
    return getter(instance, )

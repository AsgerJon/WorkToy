"""AbstractFlag provides a descriptor protocol for a flag on classes and
functions that indicate abstractness. Specifically, a class with abstract
methods should have an instance of this flag indicate this. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any
  from worktoy.mcls import CallMeMaybe


class AbstractFlag:
  """AbstractFlag provides a descriptor protocol for a flag on classes and
  functions that indicate abstractness. Specifically, a class with abstract
  methods should have an instance of this flag indicate this. """

  __field_name__ = None
  __field_owner__ = None
  __pvt_name__ = None
  __explicit_get_key__ = None

  def __init__(self, *args) -> None:
    for arg in args:
      if isinstance(arg, str):
        self.__pvt_name__ = arg
        break

  def GET(self, callMeMaybe: CallMeMaybe) -> CallMeMaybe:
    """Sets a specific function as the getter for the flag."""
    if self.__explicit_get_key__ is not None:
      e = """The getter for the flag is already set!"""
      raise AttributeError(e)
    self.__explicit_get_key__ = callMeMaybe.__name__
    return callMeMaybe

  def __set_name__(self, owner: type, name: str) -> None:
    """Set the name of the field and the owner of the field."""
    self.__field_name__ = name
    self.__field_owner__ = owner

  def __get__(self, instance: object, owner: type) -> Any:
    if instance is None:
      return self
    if self.__pvt_name__ is not None:
      out = getattr(instance, self.__pvt_name__, None)
      if out is None:
        e = """The attribute '%s' is not set on the instance!"""
        raise AttributeError(e % self.__pvt_name__)
      return True if out else False
    getterFunction = getattr(owner, self.__explicit_get_key__, None)
    if getterFunction is None:
      e = """The getter for the flag is not set!"""
      raise AttributeError(e)
    return getterFunction(instance)

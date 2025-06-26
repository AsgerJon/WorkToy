"""
Object provides the most basic object used by the 'worktoy' library. It
stands in for the 'object' type by adding functionality that must be
shared by every object in the library.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, TypeVar, Type, Self, Optional


class Object:
  """
  Object provides the most basic object used by the 'worktoy' library. It
  stands in for the 'object' type by adding functionality that must be
  shared by every object in the library.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  __slots__ = (
      '__field_owner__',
      '__field_name__',
      '__pos_args__',
      '__key_args__',
      '__dyn_dict__'
  )

  #  Private Variables
  __field_owner__: Optional[Type[object]]
  __field_name__: Optional[str]
  __pos_args__: Optional[tuple[Any, ...]]
  __key_args__: Optional[dict[str, Any]]
  __dyn_dict__: Optional[dict[str, Any]]

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, *args: Any, **kwargs: Any) -> None:
    """
    Initializes the object with the given arguments and keyword arguments.
    """
    object.__init__(self)
    self.__pos_args__ = args
    self.__key_args__ = kwargs

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init_subclass__(cls, **kwargs) -> None:
    """
    Initializes the subclass with the given keyword arguments.
    """
    object.__init_subclass__()

  def __setattr__(self, name: str, value: Any) -> None:
    """
    Sets the attribute of the object with the given name to the given value.
    """
    if name in self.__slots__:
      return object.__setattr__(self, name, value)
    if not self.__setattr_fallback__(name, value):
      return object.__setattr__(self, name, value)

  def __getattr__(self, name: str) -> Any:
    """
    Attempts to retrieve the attribute from the dynamic dictionary.
    Subclasses should implement functionality to collect dynamic
    attributes in the `__dyn_dict__` attribute.
    """
    try:
      return self.__dyn_dict__[name]
    except Exception as exception:
      infoSpec = """%s has not attribute '%s'"""
      info = infoSpec % (self.__class__.__name__, name)
      raise AttributeError(info) from exception

  def __set_name__(self, owner: Type[object], name: str) -> None:
    """
    Sets the name of the object in the owner class.
    """
    self.__field_owner__ = owner
    self.__field_name__ = name

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __setattr_fallback__(self, name: str, value: Any) -> None:
    """
    Fallback method for setting attributes that are not in __slots__.
    Subclasses may implement this method to handle dynamic attributes.
    """

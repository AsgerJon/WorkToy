"""AbstractDescriptor provides the abstract base class for all general
implementations of the descriptor protocol in the 'worktoy' library. Some
modules might implement simple descriptor implementations, but these
should be considered private to those modules."""
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.text import monoSpace, typeMsg
from worktoy.waitaminute import SubclassException
from worktoy.waitaminute.descriptor_exceptions import MissingGetterException
from worktoy.waitaminute.descriptor_exceptions import MissingSetterException
from worktoy.waitaminute.descriptor_exceptions import MissingDeleterException

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any


class AbstractDescriptor:
  """AbstractDescriptor provides the abstract base class for all general
  implementations of the descriptor protocol in the 'worktoy' library. Some
  modules might implement simple descriptor implementations, but these
  should be considered private to those modules."""

  __field_name__ = None
  __field_owner__ = None
  __current_owner__ = None

  def getFieldName(self) -> str:
    """Getter-function for the field name."""
    if self.__field_name__ is None:
      e = """Instance of 'AttriBox' does not belong to class. This 
      typically indicates that the owning class is still being created."""
      raise RuntimeError(monoSpace(e))
    if isinstance(self.__field_name__, str):
      return self.__field_name__
    e = typeMsg('__field_name__', self.__field_name__, str)
    raise TypeError(monoSpace(e))

  def setFieldName(self, name: str) -> None:
    """Setter-function for the field name."""
    if self.__field_name__ is not None:
      e = """The field name is already set!"""
      raise AttributeError(monoSpace(e))
    if not isinstance(name, str):
      e = typeMsg('name', name, str)
      raise TypeError(monoSpace(e))
    self.__field_name__ = name

  def getFieldOwner(self) -> type:
    """Getter-function for the field owner."""
    if self.__field_owner__ is None:
      e = """Instance of 'AttriBox' does not belong to class. This 
      typically indicates that the owning class is still being created. """
      raise RuntimeError(monoSpace(e))
    if isinstance(self.__field_owner__, type):
      return self.__field_owner__
    e = typeMsg('__field_owner__', self.__field_owner__, type)
    raise TypeError(monoSpace(e))

  def setFieldOwner(self, owner: type) -> None:
    """Setter-function for the field owner."""
    if self.__field_owner__ is not None:
      e = """The field owner is already set!"""
      raise AttributeError(monoSpace(e))
    if not isinstance(owner, type):
      e = typeMsg('owner', owner, type)
      raise TypeError(monoSpace(e))
    self.__field_owner__ = owner

  def getCurrentOwner(self, ) -> type:
    """Getter-function for the current owner."""
    if self.__current_owner__ is None:
      e = """The current owner is not set!"""
      raise AttributeError(monoSpace(e))
    if isinstance(self.__current_owner__, type):
      return self.__current_owner__
    e = typeMsg('__current_owner__', self.__current_owner__, type)
    raise TypeError(monoSpace(e))

  # -----------------------------------------------------------------------
  #  Instance specific methods

  def __instance_get__(self, instance: object) -> Any:
    """Getter-function for the inner object."""
    raise MissingGetterException(self)

  def __instance_set__(self, instance: object, value: Any) -> None:
    """Setter-function for the inner object."""
    raise MissingSetterException(self)

  def __instance_del__(self, instance: object) -> None:
    """Deleter-function for the inner object."""
    raise MissingDeleterException(self)

  # -----------------------------------------------------------------------
  #  Hooks

  def __pre_get__(self, instance: object, ) -> Any:
    """Pre-get hook. """

  def __pre_set__(self, instance: object, value: Any) -> None:
    """Pre-set hook. """

  def __post_set__(self, instance: object, ) -> None:
    """Post-set hook. """

  def __pre_del__(self, instance: object, ) -> None:
    """Pre-delete hook. """

  def __post_del__(self, instance: object, ) -> None:
    """Post-delete hook. """

  # -----------------------------------------------------------------------
  #  Validation methods

  def _validateOwner(self, owner: type, **kwargs) -> type:
    """Validates the owner type. """
    if owner is self.__current_owner__:
      return owner
    if kwargs.get('_recursion', False):
      raise RecursionError
    if not issubclass(owner, self.__field_owner__):
      raise SubclassException(owner, self.__field_owner__)
    self.__current_owner__ = owner
    return self._validateOwner(owner, _recursion=True)

  # -----------------------------------------------------------------------
  #  Descriptor protocol methods

  def __set_name__(self, owner: type, name: str) -> None:
    """Set the name of the field and the owner of the field."""
    self.__field_name__ = name
    self.__field_owner__ = owner
    self.__current_owner__ = owner

  def __get__(self, instance: object, owner: type) -> Any:
    owner = self._validateOwner(owner)
    if instance is None:
      return self
    self.__pre_get__(instance)
    return self.__instance_get__(instance)

  def __set__(self, instance: object, value: Any) -> None:
    owner = self._validateOwner(type(instance).__mro__[0])
    self.__pre_set__(instance, value)
    self.__instance_set__(instance, value)
    self.__post_set__(instance, )

  def __delete__(self, instance: object) -> None:
    owner = self._validateOwner(type(instance).__mro__[0])
    self.__pre_del__(instance)
    self.__instance_del__(instance)
    self.__post_del__(instance)

  # -----------------------------------------------------------------------
  #  Fallback __init__ and __init_subclass__ methods

  def __init__(self, *args, **kwargs) -> None:
    """Why are we still here?"""

  def __init_subclass__(cls, *args, **kwargs) -> None:
    """Just to suffer?"""

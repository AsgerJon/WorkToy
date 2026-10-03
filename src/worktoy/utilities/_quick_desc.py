"""
QuickDesc is a minimal read-only descriptor exposing a private slot.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, overload, TypeVar, Generic

from . import textFmt, NoPickle

T = TypeVar('T')

if TYPE_CHECKING:  # pragma: no cover
  from typing import Self, Any, Union, Optional, Never


class QuickDesc(NoPickle, Generic[T]):
  """Read-only descriptor exposing a named private slot.

  Constructed with the name of a private attribute (typically
  dunder-prefixed), 'QuickDesc' reads that attribute on access
  and refuses writes with 'ReadOnlyError' and deletions with
  'ProtectedError', as every other read-only descriptor in 'worktoy'
  does; both are 'AttributeError's. This is enough for the descriptor
  needs internal to the foundation packages.

  'QuickDesc' is intentionally minimal. Project authors using
  'worktoy' should prefer the descriptors in 'worktoy.desc':
  'AttriBox' for type-enforced read-write attributes, and
  'Field' for descriptors with explicit accessor decorators.

  Examples
  --------
  >>> class Box:
  ...   __value__ = 42
  ...   value = QuickDesc('__value__')
  >>> Box().value
  42
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private Variables
  __private_key__: Optional[str] = None
  __field_name__: Optional[str] = None
  __field_owner__: Optional[type] = None

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # @formatter:off
  @overload
  def __get__(self, instance: None, owner: type) -> Self: ...
  @overload
  def __get__(self, instance: Any, owner: type) -> T: ...
  # @formatter:on

  def __get__(self, instance: Any, owner: type) -> Union[Self, T]:
    if instance is None:
      return self
    if self.__private_key__ is None:
      #  Local import: 'worktoy.utilities' is the foundation package
      #  and loads before 'worktoy.waitaminute', which depends on it.
      #  A module-level import would cycle. By the time __get__ is
      #  called the full library is loaded and the import is cheap.
      from ..waitaminute import MissingVariable
      raise MissingVariable(self, '__private_key__', str)
    return getattr(instance, self.__private_key__)

  def __set__(self, instance: Any, value: Any) -> Never:
    #  Local import, as in '__get__': 'worktoy.waitaminute' loads after
    #  'worktoy.utilities'.
    from ..waitaminute.desc import ReadOnlyError
    raise ReadOnlyError(instance, self, value)

  def __delete__(self, instance: Any) -> Never:
    from ..waitaminute.desc import ProtectedError
    raise ProtectedError(instance, self)

  def __set_name__(self, owner: type, name: str) -> None:
    if self.__private_key__ == name:
      infoSpec = """Name collision between private key and field name 
      both being: '%s'"""
      info = infoSpec % name
      raise ValueError(textFmt(info))
    self.__field_name__ = name
    self.__field_owner__ = owner

  def __init__(self, key: str) -> None:
    self.__private_key__ = key

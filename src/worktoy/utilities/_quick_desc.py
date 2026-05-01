"""
QuickDesc provides a basic implementation of the descriptor protocol.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, overload, TypeVar, Generic

from . import textFmt

T = TypeVar('T')

if TYPE_CHECKING:  # pragma: no cover
  from typing import Self, Any, Union, Optional


class QuickDesc(Generic[T]):
  """
  QuickDesc provides a basic implementation of the descriptor protocol.

  Please note that QuickDesc is used internally by 'worktoy' to avoid
  certain boilerplate code. Those developing projects using 'worktoy' are
  encouraged to direct their attention to the 'worktoy.desc' package,
  which provides much more powerful and flexible descriptor
  implementations. In particular:
  - 'AttriBox' providing lazily-initialized, read-write attributes with
  strict type enforcement.
  - 'Field' providing descriptors with decorators specifying accessor
  functions.
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

  def __set__(self, instance: Any, value: Any) -> None:
    cls = type(instance).__name__
    name = self.__field_name__ or '<unbound>'
    infoSpec = """Cannot set attribute '%s' on '%s' object — 
    QuickDesc is read-only."""
    raise AttributeError(textFmt(infoSpec % (name, cls)))

  def __delete__(self, instance: Any) -> None:
    cls = type(instance).__name__
    name = self.__field_name__ or '<unbound>'
    infoSpec = """Cannot delete attribute '%s' on '%s' object — 
    QuickDesc is read-only."""
    raise AttributeError(textFmt(infoSpec % (name, cls)))

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

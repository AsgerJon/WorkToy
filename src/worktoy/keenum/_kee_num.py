"""
KeeNum provides the shared baseclass for KeeNum enumerating classes.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, overload, TypeVar

from ..core import Object
from ..desc import Field
from ..waitaminute import MissingVariable
from ..waitaminute.desc import ReadOnlyError, ProtectedError
from ..waitaminute.keenum import KeeWriteOnceError
from . import Kee

T = TypeVar('T')

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Never, Self, Optional, TypeAlias

  MaybeInt: TypeAlias = Optional[int]
  MaybeStr: TypeAlias = Optional[str]
  MaybeKee: TypeAlias = Optional[Kee]
  MaybeBool: TypeAlias = Optional[bool]


class _KeeBase(Object, ):
  """
  KeeNum is the base class for all enumerating classes in the KeeNum
  framework. It provides a common interface and functionality for
  enumerating members."""

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private Variables
  __field_value__: Optional[Any] = None
  __frozen_state__: MaybeBool = None
  __field_kee__: MaybeKee = None  # The 'Kee' object of this member.

  #  Public Variables
  index: Field[int] = Field()
  value: Field[Any] = Field()
  valueType: Field[type] = Field()
  kee: Field[Kee] = Field()

  #  Virtual Variables
  name: Field[str] = Field()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @kee.GET
  def _getKee(self) -> Kee:
    if self.__field_kee__ is None:
      raise MissingVariable(self, '__field_kee__', Kee)
    return self.__field_kee__

  @name.GET
  def _getName(self) -> str:
    return self.kee.name

  @index.GET
  def _getIndex(self) -> int:
    return self.kee.index

  @value.GET
  def _getValue(self) -> Any:
    """Return the value of the member."""
    return self.kee.getValue()

  @valueType.GET
  def _getValueType(self) -> type:
    """Return the type of the value of the member."""
    return self.kee.getFieldType()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # @formatter:off
  @overload
  def __init__(self, identifier: Any) -> None: ...
  @overload
  def __init__(self, member: Kee) -> None: ...
  # @formatter:on

  def __init__(self, member: Kee) -> None:
    object.__setattr__(self, '__frozen_state__', False)
    self.__field_kee__ = member
    object.__setattr__(self, '__frozen_state__', True)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __setattr__(self, name: str, value: Any) -> None:
    """Set an attribute of the member."""
    if object.__getattribute__(self, '__frozen_state__'):
      raise KeeWriteOnceError(self, name)
    object.__setattr__(self, name, value)

  def __set_name__(self, owner: type, name: str) -> None:
    """This reimplementation of '__set_name__' is necessary to prevent the
    '__setattr__' method above from raising when a class wants an
    enumeration defined in its namespace. """
    pass

  def __get__(self, instance: Any, owner: type, **kw) -> KeeNum:
    """Implementation of '__get__' is necessary for the same reason as
    '__set_name__'. """
    return self

  def __set__(self, instance: Any, value: Any, **kwargs) -> Never:
    """Ensures 'ReadOnlyError' is raised instead of 'KeeWriteOnceError'."""
    raise ReadOnlyError(instance, self, value)

  def __delete__(self, instance: Any, **kwargs) -> Never:
    """Ensures 'ProtectedError' is raised instead of 'KeeWriteOnceError'."""
    raise ProtectedError(instance, self, self)

  def __bool__(self, ) -> bool:
    """
    Members named 'NULL' are always falsy. Other members reflect the
    truthiness of their value.
    """
    if self.name.lower() == 'null':
      return False
    return True if self.value else False

  def __int__(self) -> int:
    """Return the index of the member."""
    return self.index

  __index__ = __int__

  def __hash__(self) -> Optional[int]:
    try:
      _ = hash((self.value,))
    except TypeError:
      return
    else:
      base = str.join('::', (type(self).__name__, self.name,))
      return int.from_bytes(base.encode(), 'big')

  def __eq__(self, other: Any) -> bool:
    if type(self) is not type(other):
      return NotImplemented
    return True if self is other else False

  def __str__(self) -> str:
    infoSpec = """%s.%s"""
    clsName = type(self).__name__
    info = infoSpec % (clsName, self.name)
    return info

  __repr__ = __str__

  if TYPE_CHECKING:  # pragma: no cover
    # @formatter:off
    def __call__(self, identifier: Any) -> Self: ...
    # @formatter:on

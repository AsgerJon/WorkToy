"""
FastBox is a lean, type-enforced attribute descriptor that trades the
ergonomics of 'AttriBox' for speed.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, Generic, overload

from ..waitaminute import TypeException, MissingVariable

T = TypeVar('T')

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Self, Optional


class FastBox(Generic[T]):
  """
  FastBox is a lean, type-enforced attribute descriptor that trades the
  ergonomics of 'AttriBox' for speed. It carries no descriptor context,
  no access hooks, and no sentinel resolution: the value lives directly
  in the instance dict, so a read is one dict lookup and a write is one
  type check plus one dict store.

  Sacrificed relative to 'AttriBox':
  - access hooks (preGet / onSet / preDelete / ...),
  - 'self.instance' / 'self.owner' context inside accessors,
  - 'THIS' / 'OWNER' sentinels in the deferred default arguments,
  - set-time coercion: a write must already be an instance of the field
    type, the numeric tower is not applied ('x: float' rejects an int).

  Nesting is still correct without any context machinery: '__get__'
  reads the 'instance' parameter rather than shared descriptor state, so
  re-entrant access to the same descriptor lives on the call stack. The
  owning instance must have a '__dict__' (no '__slots__'-only owners).
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private Variables
  __field_type__: Optional[type] = None
  __field_name__: Optional[str] = None
  __private_name__: Optional[str] = None
  __default_args__: tuple = ()
  __default_kwargs__: Optional[dict] = None

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  if TYPE_CHECKING:  # pragma: no cover
    # @formatter:off
    @overload
    def __init__(self, value: T) -> None: ...
    @overload
    def __init__(self, ) -> None: ...
    def __init__(self, *args, **kwargs) -> None: ...
    # @formatter:on

  @classmethod
  def __class_getitem__(cls, fieldType: type) -> FastBox:
    """
    The '__class_getitem__' method captures the field type from the
    'FastBox[T]' subscript.

    Parameters
    ----------
    fieldType : type
        The field type fixed by the subscript.

    Returns
    -------
    FastBox
        A new 'FastBox' carrying 'fieldType', ready for the deferred
        '__call__'.
    """
    self = cls.__new__(cls)
    self.__field_type__ = fieldType
    return self

  def __call__(self, *args, **kwargs) -> Self:
    """
    The '__call__' method captures the arguments used to build the
    default value, forwarded to the field-type constructor on first
    access.

    Returns
    -------
    Self
        'self', so the call site can chain straight into a class-body
        assignment, for example 'x = FastBox[int](42)'.
    """
    self.__default_args__ = args
    self.__default_kwargs__ = kwargs
    return self

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __set_name__(self, owner: type, name: str) -> None:
    self.__field_name__ = name
    self.__private_name__ = '__fast_%s__' % name

  def __get__(self, instance: Any, owner: type) -> Any:
    if instance is None:
      return self
    store = instance.__dict__
    try:
      return store[self.__private_name__]
    except KeyError:
      value = self._build()
      store[self.__private_name__] = value
      return value

  def __set__(self, instance: Any, value: Any) -> None:
    if TYPE_CHECKING:  # pragma: no cover
      assert isinstance(self.__field_type__, type)
      assert isinstance(self.__field_name__, str)
    if isinstance(value, self.__field_type__):
      instance.__dict__[self.__private_name__] = value
      return
    raise TypeException(self.__field_name__, value, self.__field_type__)

  def __delete__(self, instance: Any) -> None:
    if TYPE_CHECKING:  # pragma: no cover
      assert isinstance(self.__field_name__, str)
    try:
      del instance.__dict__[self.__private_name__]
    except KeyError as keyError:
      raise MissingVariable(instance, self.__field_name__) from keyError

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _build(self) -> Any:
    """
    The '_build' method constructs a fresh default value from the
    captured arguments.

    Returns
    -------
    Any
        A new field-type instance built from the captured arguments.

    Raises
    ------
    MissingVariable
        If no field type has been captured.
    """
    if self.__field_type__ is None:
      raise MissingVariable(self, '__field_type__', type)
    kwargs = self.__default_kwargs__ or {}
    return self.__field_type__(*self.__default_args__, **kwargs)

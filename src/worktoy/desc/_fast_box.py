"""
FastBox is a lean, type-enforced attribute descriptor that trades the
ergonomics of 'AttriBox' for speed.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, Generic, overload

from . import _RootAlias
from ..utilities import NoPickle, typeCast, castRule
from ..waitaminute import TypeException, MissingVariable
from ..waitaminute.dispatch import TypeCastException

T = TypeVar('T')

#  The builtin containers, the text types and the number types, as
#  'AttriBox' names them: a container field type refuses a lone text default
#  rather than splitting it into characters or integers, and a number field
#  type casts a lone default rather than rounding it.
_CONTAINERS = (list, tuple, set, frozenset, dict)
_TEXT_TYPES = (str, bytes, bytearray)
_NUMBER_TYPES = (bool, int, float, complex)

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Self, Optional, Union


class FastBox(NoPickle, Generic[T]):
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

  Deleting the field removes its value from the instance dict, so the
  next read builds a fresh default, where the other boxes raise
  'MissingVariable' for a deleted field. Deleting a field that holds no
  value, never read or already deleted, raises 'MissingVariable'.
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
  def __class_getitem__(cls, fieldType: Union[type, TypeVar]) -> FastBox:
    """
    The '__class_getitem__' method captures the field type from the
    'FastBox[T]' subscript. A plain class produces a fresh 'FastBox'
    parametrized with it. Anything else is forwarded to the generic
    machinery: a 'TypeVar', so 'class Sub(FastBox[T])' declares a generic
    subclass, or a parametrized generic such as 'list[int]', whose alias
    raises 'PhantomBoxError' when a class body binds it.

    Parameters
    ----------
    fieldType : type or TypeVar
        The field type fixed by the subscript.

    Returns
    -------
    FastBox
        A new 'FastBox' carrying 'fieldType', ready for the deferred
        '__call__'.

    Raises
    ------
    TypeException
        If 'fieldType' is neither a class nor anything the generic
        machinery accepts.
    """
    #  'isinstance(fieldType, type)' reads '__class__', which a builtin
    #  parametrized generic such as 'list[int]' forwards to its origin on
    #  Python 3.9 and 3.10, answering 'True'. The type of the subscript is
    #  a metaclass exactly when the subscript is a plain class, on every
    #  version, without an attribute lookup a class-level hook could answer.
    if issubclass(type(fieldType), type):
      self = cls.__new__(cls)
      self.__field_type__ = fieldType
      return self
    try:
      out = super().__class_getitem__(fieldType)  # noqa
    except Exception as exception:
      name, value = 'fieldType', fieldType
      raise TypeException(name, value, type, TypeVar) from exception
    else:
      return _RootAlias.fromAlias(out)

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
    """
    A box that never captured a field type, written 'FastBox()' or
    produced by calling the alias of a generic subscript, is refused as
    the class is created, since '__class_getitem__' is the only place a
    field type is ever assigned. Python 3.7 through 3.11 re-raise the
    exception wrapped in a 'RuntimeError'.
    """
    if self.__field_type__ is None:
      raise MissingVariable(self, '__field_type__', type)
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
    captured arguments. It follows three rules of 'AttriBox': a builtin
    container field type refuses a lone 'str', 'bytes' or 'bytearray'
    rather than splitting it, a number field type, 'bool', 'int', 'float'
    or 'complex' or a subclass keeping the constructor of one, casts a
    lone value through 'typeCast' rather than rounding it, and what the
    field type returns must be an instance of it. It runs once per
    instance and field, on the first read.

    Returns
    -------
    Any
        A new field-type instance built from the captured arguments.

    Raises
    ------
    MissingVariable
        If no field type has been captured.
    TypeException
        If a container field type receives a lone text argument, a number
        field type a lone value the cast refuses, or the field type
        returns something that is not an instance of it.
    """
    fieldType = self.__field_type__
    if fieldType is None:
      raise MissingVariable(self, '__field_type__', type)
    args, kwargs = self.__default_args__, self.__default_kwargs__ or {}
    if len(args) == 1 and not kwargs:
      if fieldType in _CONTAINERS and isinstance(args[0], _TEXT_TYPES):
        raise TypeException(self.__field_name__, args[0], fieldType)
      if castRule(fieldType) in _NUMBER_TYPES:
        return self._castNumber(args[0])
    value = fieldType(*args, **kwargs)
    if isinstance(value, fieldType):
      return value
    raise TypeException(self.__field_name__, value, fieldType)

  def _castNumber(self, value: Any) -> Any:
    """
    The '_castNumber' method casts the lone default of a number field
    through 'typeCast', and raises 'TypeException' naming the field when
    the cast refuses.
    """
    fieldType = self.__field_type__
    try:
      return typeCast(fieldType, value)
    except TypeCastException as typeCastException:
      name = self.__field_name__
      raise TypeException(name, value, fieldType) from typeCastException

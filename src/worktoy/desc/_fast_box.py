"""
FastBox is 'AttriBox' made stricter and faster.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, Generic, overload

from . import _RootAlias
from ..core.sentinels import SentinelMeta, THIS
from ..utilities import textFmt, typeCast
from ..waitaminute import TypeException, MissingVariable
from ..waitaminute.desc import MissingInstanceDict

T = TypeVar('T')

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Self, Optional, Union


class FastBox(Generic[T]):
  """
  FastBox is 'AttriBox' made stricter and faster. An attribute is declared
  the same way, 'mass = FastBox[float](1.0)', and the class docstring of
  'AttriBox' explains how a box works; this one says only where 'FastBox'
  differs.

  It is faster because it keeps none of the machinery of 'AttriBox': no
  notification hooks such as 'onSet', no 'self.instance' or 'self.owner',
  no 'THIS', 'OWNER' or 'DESC' in the parentheses and no tags on the
  field object. A read is one lookup in the instance dict, and a write
  one 'isinstance' check and one store. It suits an attribute read in a
  hot loop that needs none of that.

  It is stricter in what it accepts. The parentheses take one value, not
  the arguments of a constructor, checked on the line that writes it, and
  every instance shares that value; see '__call__'. A write must already
  be of the field type, since nothing is cast on assignment. Deleting the
  attribute lets the next read start it over, where 'AttriBox' raises
  'MissingVariable' until the attribute is assigned again.

    class Particle:
      mass = FastBox[float](1)       # holds 1.0
      tags = FastBox[tuple](())

    p = Particle()
    p.mass = 2.0                     # fine
    p.mass = 2                       # TypeException: a write is not cast
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private Variables
  __field_type__: Optional[type] = None
  __field_name__: Optional[str] = None
  __private_name__: Optional[str] = None
  #  The value of the parentheses as a one-tuple, or empty for none.
  __declared_value__: tuple = ()

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

  def clone(self) -> Self:
    """
    Works as 'BaseDescriptor.clone' does for an 'AttriBox', giving the
    second name of 'width = height = FastBox[int](1)' a box of its own; the
    clone carries the declared value where the clone of an 'AttriBox'
    carries the arguments of its declaration.

    Returns
    -------
    Self
        A new box, ready to be placed on a class.
    """
    new = object.__new__(type(self))
    skipped = ('__field_name__', '__private_name__')
    for key, value in vars(self).items():
      if key in skipped:
        continue
      object.__setattr__(new, key, value)
    return new

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __call__(self, *args, **kwargs) -> Self:
    """
    Takes the place of 'AttriBox.__call__' and differs from it in what the
    parentheses hold: one value, not the arguments of a constructor,
    checked on the line that writes it. The value must be of the field
    type, or one 'typeCast' converts without loss, and since every
    instance shares it, it must be hashable. Empty parentheses give each
    instance a new 'fieldType()' at its first read instead.

        class Point:
          x = FastBox[float](1)      # holds 1.0
          tags = FastBox[list]()     # a new list for each instance

        FastBox[int]('abc')          # TypeCastException
        FastBox[list]([1, 2])        # TypeError: not hashable

    Parameters
    ----------
    *args : Any
        Nothing, or the one value every instance starts with.
    **kwargs : Any
        Nothing; any keyword is refused.

    Returns
    -------
    Self
        'self', so the call site can chain straight into a class-body
        assignment, for example 'x = FastBox[int](42)'.

    Raises
    ------
    MissingVariable
        If the box has no field type.
    TypeCastException
        If the value is no instance of the field type and 'typeCast'
        refuses to convert it.
    TypeError
        If the value cannot be hashed, or several arguments or a keyword
        are given.
    """
    fieldType = self.__field_type__
    if fieldType is None:
      raise MissingVariable(self, '__field_type__', type)
    if kwargs or len(args) > 1:
      infoSpec = """'%s[%s]' takes one value of its field type, not the
      arguments of a constructor; give it a '%s', or leave the parentheses
      empty."""
      names = (type(self).__name__, fieldType.__name__, fieldType.__name__)
      raise TypeError(textFmt(infoSpec % names))
    if not args:
      self.__declared_value__ = ()
      return self
    value = typeCast(fieldType, args[0])
    try:
      hash(value)
    except TypeError as typeError:
      infoSpec = """'%s[%s]' shares its value among every instance, so the
      value must be hashable, which a '%s' is not. Leave the parentheses
      empty for a new '%s()' per instance, or use 'AttriBox'."""
      names = (
        type(self).__name__, fieldType.__name__, type(value).__name__,
        fieldType.__name__,
      )
      raise TypeError(textFmt(infoSpec % names)) from typeError
    self.__declared_value__ = (value,)
    return self

  @classmethod
  def __class_getitem__(cls, fieldType: Union[type, TypeVar]) -> FastBox:
    """
    Works as 'AttriBox.__class_getitem__', with no difference.

    Parameters
    ----------
    fieldType : type or TypeVar
        The field type fixed by the subscript.

    Returns
    -------
    FastBox
        A new box of the class subscripted, carrying 'fieldType'.

    Raises
    ------
    TypeException
        If 'fieldType' is neither a class nor anything 'typing' accepts.
    TypeError
        If 'fieldType' is a sentinel other than 'THIS', such as 'OWNER'.
    """
    if isinstance(fieldType, SentinelMeta) and fieldType is not THIS:
      infoSpec = """The subscript '%s[%s]' names a sentinel as the field
      type. A sentinel stands for a meaning, such as the enclosing class,
      and is no type of value a field could hold; the field type is the
      class of the values the field holds."""
      info = infoSpec % (cls.__name__, fieldType.__name__)
      raise TypeError(textFmt(info))
    #  'isinstance(fieldType, type)' reads '__class__', which a builtin
    #  parametrized generic such as 'list[int]' forwards to its origin on
    #  Python 3.9 and 3.10, answering 'True'. The type of the subscript is
    #  a metaclass exactly when the subscript is a plain class, on every
    #  version, without an attribute lookup a class-level hook could answer.
    if issubclass(type(fieldType), type) or fieldType is THIS:
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

  def __set_name__(self, owner: type, name: str) -> None:
    """
    Works as 'AttriBox.__set_name__', with the same refusals on the class
    statement. The difference is where an instance keeps its value: in its
    own '__dict__' under '__fast_<name>__'.

      class Point:
        x = FastBox[int](0)

      p = Point()
      p.x = 3
      vars(p)                        # {'__fast_x__': 3}

    Parameters
    ----------
    owner : type
        The class being created that holds the box.
    name : str
        The name the box is bound to in the class body.

    Returns
    -------
    None

    Raises
    ------
    MissingVariable
        If the box was never subscripted.
    MissingInstanceDict
        If the instances of 'owner' have no '__dict__'.
    """
    held = self.__field_name__
    if held is not None and held != name:
      #  'type.__new__' runs '__set_name__' over a copy of the class dict,
      #  so the second name may take the clone here.
      clone = self.clone()
      type.__setattr__(owner, name, clone)
      return clone.__set_name__(owner, name)
    if self.__field_type__ is None:
      raise MissingVariable(self, '__field_type__', type)
    #  Zero exactly when instances of 'owner' have no '__dict__'.
    if not type.__getattribute__(owner, '__dictoffset__'):
      raise MissingInstanceDict(owner, name)
    if self.__field_type__ is THIS:
      self.__field_type__ = owner
    self.__field_name__ = name
    self.__private_name__ = '__fast_%s__' % name

  def __get__(self, instance: Any, owner: type) -> Any:
    """
    Works as 'AttriBox.__get__', except that a read through an instance is
    one lookup in its '__dict__' and runs no hooks; the first read takes
    the declared value or a new 'fieldType()', see '_build'.

    Parameters
    ----------
    instance : Any
        The instance the attribute is read through, or None when read
        through the class.
    owner : type
        The class the attribute is read through.

    Returns
    -------
    Any
        The box itself through the class, the value through an instance.

    Raises
    ------
    MissingInstanceDict
        If the instance has no '__dict__', as for a box set with 'setattr'
        on a class declaring '__slots__' without one.
    """
    if instance is None:
      return self
    try:
      store = instance.__dict__
    except AttributeError as attributeError:
      fieldName = self.__field_name__
      raise MissingInstanceDict(instance, fieldName) from attributeError
    try:
      return store[self.__private_name__]
    except KeyError:
      value = self._build()
      store[self.__private_name__] = value
      return value

  def __set__(self, instance: Any, value: Any) -> None:
    """
    Works as an assignment to an 'AttriBox', see
    'AttriBox.__instance_set__', except that nothing is cast and no hooks
    run: the value must already be of the field type, so 'p.mass = 2' on a
    'FastBox[float]' raises 'TypeException'.

    Parameters
    ----------
    instance : Any
        The instance the attribute is assigned through.
    value : Any
        The assigned value.

    Returns
    -------
    None

    Raises
    ------
    TypeException
        If the value is not an instance of the field type.
    MissingInstanceDict
        If the instance has no '__dict__'.
    """
    if TYPE_CHECKING:  # pragma: no cover
      assert isinstance(self.__field_type__, type)
      assert isinstance(self.__field_name__, str)
    if isinstance(value, self.__field_type__):
      try:
        store = instance.__dict__
      except AttributeError as attributeError:
        fieldName = self.__field_name__
        raise MissingInstanceDict(instance, fieldName) from attributeError
      store[self.__private_name__] = value
      return
    raise TypeException(self.__field_name__, value, self.__field_type__)

  def __delete__(self, instance: Any) -> None:
    """
    Works as 'AttriBox.__instance_delete__' except in what follows: the
    next read starts the attribute over from the declared value instead of
    raising 'MissingVariable', and deleting an attribute that holds
    nothing, never read or already deleted, raises.

    Parameters
    ----------
    instance : Any
        The instance the attribute is deleted from.

    Returns
    -------
    None

    Raises
    ------
    MissingVariable
        If the instance holds no value for the attribute.
    MissingInstanceDict
        If the instance has no '__dict__'.
    """
    if TYPE_CHECKING:  # pragma: no cover
      assert isinstance(self.__field_name__, str)
    try:
      store = instance.__dict__
    except AttributeError as attributeError:
      fieldName = self.__field_name__
      raise MissingInstanceDict(instance, fieldName) from attributeError
    try:
      del store[self.__private_name__]
    except KeyError as keyError:
      raise MissingVariable(instance, self.__field_name__) from keyError

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _build(self) -> Any:
    """
    Takes the place of 'AttriBox._resolve': instead of calling the
    constructor on the arguments of the declaration, it gives the declared
    value, which every instance shares, or for empty parentheses a new
    'fieldType()'.

    Returns
    -------
    Any
        The declared value, or a new instance of the field type.

    Raises
    ------
    MissingVariable
        If no field type has been captured.
    TypeException
        If 'fieldType()' returns something that is not an instance of it.
    """
    fieldType = self.__field_type__
    if fieldType is None:
      raise MissingVariable(self, '__field_type__', type)
    if self.__declared_value__:
      return self.__declared_value__[0]
    value = fieldType()
    if isinstance(value, fieldType):
      return value
    raise TypeException(self.__field_name__, value, fieldType)

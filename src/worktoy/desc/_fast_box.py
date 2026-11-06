"""
FastBox is 'AttriBox' made stricter and faster.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, Generic, overload

from . import _RootAlias
from ..core.sentinels import SentinelMeta, THIS
from ..dispatch import TypeSig
from ..utilities import textFmt, typeCast
from ..waitaminute import TypeException, MissingVariable
from ..waitaminute.desc import MissingInstanceDict, SharedDescriptor

T = TypeVar('T')

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any, Self, Optional, Union


class FastBox(Generic[T]):
  """
  An attribute read in a hot loop cannot afford the machinery of an
  'AttriBox': frames, notification hooks, placeholders, casts and tags.
  It still needs a declared type and a default, and a write of the wrong
  type must still fail. What it gives up must be plain, not hidden in
  conveniences that cost time.

  Implementation
  --------------

  The attribute is declared as with 'AttriBox', 'mass =
  FastBox[float](1.0)', but the parentheses hold one value, checked and
  cast once on the declaration line, which every instance shares; empty
  parentheses give each instance a new 'fieldType()' at its first read
  instead. A box declared without parentheses is refused as the class is
  created, and so is one placed on a second class, as an 'AttriBox' is;
  a placed box called again, as 'Particle.mass(9.0)', is refused as well,
  since it would change the value of every instance not read yet. A shared
  value must be hashable, which keeps out
  the mutable builtins, though an object hashed by identity, such as a
  'BaseObject', passes and is then shared. A read is one lookup in the
  instance dictionary, under '__fast_<name>__'. A write is one
  'isinstance' check and one store, with no cast, so assigning '2' to a
  'FastBox[float]' raises 'TypeException'. Deleting the attribute lets
  the next read start over from the declared value. No tags, no hooks, no
  'self.instance'.

  Attributes
  ----------

  __field_type__ : type
    The class of the values.

  __field_name__ : str
    The name the box is placed at.

  __field_owner__ : type
    The class the box is placed in, for the refusal of a call.

  __private_name__ : str
    The key in the instance dictionary.

  __declared_value__ : tuple or None
    The declared value in a one-element tuple, or empty, or 'None' until
    the parentheses are given.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private Variables
  __field_type__: Optional[type] = None
  __field_name__: Optional[str] = None
  __field_owner__: Optional[type] = None
  __private_name__: Optional[str] = None
  #  The value of the parentheses as a one-tuple, empty for none, or 'None'
  #  until the parentheses are given.
  __declared_value__: Optional[tuple] = None

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  if TYPE_CHECKING:  # pragma: no cover, no mutate
    # @formatter:off
    @overload
    def __init__(self, value: T) -> None: ...
    @overload
    def __init__(self, ) -> None: ...
    def __init__(self, *args, **kwargs) -> None: ...
    # @formatter:on

  def clone(self) -> Self:
    """
    The second name of 'width = height = FastBox[int](1)', and
    'THIS[Parent].name', need a box of their own with the same type and
    declared value.

    Returns
    -------

    FastBox
      An unplaced copy of the same class.
    """
    new = object.__new__(type(self))
    skipped = ('__field_name__', '__field_owner__', '__private_name__')
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
    The declaration line must give the one value every instance starts
    with, and refuse at that line a value that is of the wrong type or
    that cannot be safely shared. A placed box called again, as
    'Particle.mass(9.0)', would change the value of every instance not
    read yet, and is refused.

    Implementation
    --------------

    A placed box is refused in the words 'AttriBox' uses. One value is
    cast by 'typeCast' and must hash; none means a new 'fieldType()' per
    instance.

      class Point:
        x = FastBox[float](1)      # holds 1.0
        tags = FastBox[list]()     # a new list for each instance

    Parameters
    ----------

    *args
      Nothing, or the one declared value.

    **kwargs
      Nothing; any keyword is refused.

    Returns
    -------

    FastBox
      The box itself.

    Raises
    ------

    MissingVariable
      The box was never subscripted.

    TypeCastException
      The value is not of the field type and does not convert.

    TypeError
      The box is placed in a class already, the value cannot be hashed,
      or several arguments or a keyword are given.
    """
    if self.__field_owner__ is not None:
      infoSpec = """The box at '%s.%s' took its value as its class was
      created, and cannot take a new one."""
      ownerName = self.__field_owner__.__name__
      info = infoSpec % (ownerName, self.__field_name__)
      raise TypeError(textFmt(info))
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
      object.__setattr__(self, '__declared_value__', ())
      return self
    value = typeCast(fieldType, args[0])
    try:
      hash(value)
    except TypeError as typeError:
      infoSpec = """'%s[%s]' shares one value among every instance and
      refuses one that cannot be hashed, as this '%s' cannot. Leave the
      parentheses empty for a new '%s()' per instance, or use 'AttriBox'
      for a value of its own per instance."""
      names = (
        type(self).__name__, fieldType.__name__, type(value).__name__,
        fieldType.__name__,
      )
      raise TypeError(textFmt(infoSpec % names)) from typeError
    object.__setattr__(self, '__declared_value__', (value,))
    return self

  @classmethod
  def __class_getitem__(cls, fieldType: Union[type, TypeVar]) -> FastBox:
    """
    As for 'AttriBox': a plain class, or 'THIS', makes a box, and anything
    'typing' accepts makes a type alias for hints and bases. A class
    'isinstance' refuses is refused at the subscript by
    'TypeSig.validateTypes', as there.

    Parameters
    ----------

    fieldType : type or TypeVar
      The class of the values.

    Returns
    -------

    FastBox or _RootAlias
      A new box, or a type alias.

    Raises
    ------

    TypeError
      'fieldType' is a sentinel other than 'THIS'.

    UncheckableType
      'fieldType' is a class 'isinstance' refuses.

    TypeException
      'fieldType' is neither a class nor anything 'typing' accepts.
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
      declaration = '%s[%s]' % (cls.__name__, fieldType.__name__)
      TypeSig.validateTypes(
        fieldType,
        variadic=False,
        declaration=declaration
        )
      self = cls.__new__(cls)
      object.__setattr__(self, '__field_type__', fieldType)
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
    The box must learn where to keep the values of its instances, and a
    class it cannot serve must be refused as the class is created.

    Implementation
    --------------

    A box placed on another class already is refused, as
    'BaseDescriptor.__set_name__' refuses it. A box placed already under
    another name of the same class places a clone at the new name. 'THIS'
    as field type becomes the class, a box declared without parentheses is
    refused, the name and the owner are recorded, and the key is
    '__fast_<name>__'.

    Parameters
    ----------

    owner : type
      The class being created.

    name : str
      The name the box is bound to.

    Raises
    ------

    MissingVariable
      The box was never subscripted.

    MissingInstanceDict
      The instances of 'owner' have no '__dict__'.

    TypeError
      The box is declared without parentheses.

    SharedDescriptor
      The box is placed on another class already.
    """
    placedOwner = self.__field_owner__
    if placedOwner is not None and placedOwner is not owner:
      placedName = self.__field_name__
      raise SharedDescriptor(self, placedOwner, placedName, owner, name)
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
      object.__setattr__(self, '__field_type__', owner)
    if self.__declared_value__ is None:
      infoSpec = """The box at '%s.%s' is declared without parentheses. A
      box takes its declared value in parentheses, as '%s[%s](...)', or
      empty parentheses for a new '%s()' per instance."""
      boxName = type(self).__name__
      typeName = self.__field_type__.__name__
      names = (owner.__name__, name, boxName, typeName, typeName)
      raise TypeError(textFmt(infoSpec % names))
    object.__setattr__(self, '__field_name__', name)
    object.__setattr__(self, '__field_owner__', owner)
    object.__setattr__(self, '__private_name__', '__fast_%s__' % name)

  def __get__(self, instance: Any, owner: type) -> Any:
    """
    A read through an instance must cost one dictionary lookup.

    Implementation
    --------------

    Only a miss checks that the box was named, builds the value with
    '_build' and stores it.

    Parameters
    ----------

    instance : Any
      The instance read through, or 'None'.

    owner : type
      The class read through.

    Returns
    -------

    Any
      The box through the class, the value through an instance.

    Raises
    ------

    MissingInstanceDict
      The instance has no '__dict__'.

    MissingVariable
      The box never learned its name.
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
    except KeyError as keyError:
      #  Only a miss pays for this test, so a placed box reads in one
      #  lookup as before.
      if self.__private_name__ is None:
        raise MissingVariable(self, '__field_name__', str) from keyError
      value = self._build()
      store[self.__private_name__] = value
      return value

  def __set__(self, instance: Any, value: Any) -> None:
    """
    A write must cost one check and one store, and nothing is converted on
    the way.

    Parameters
    ----------

    instance : Any
      The instance written through.

    value : Any
      The value assigned, already of the field type.

    Raises
    ------

    TypeException
      The value is not an instance of the field type.

    MissingInstanceDict
      The instance has no '__dict__'.

    MissingVariable
      The box never learned its name.
    """
    if TYPE_CHECKING:  # pragma: no cover, no mutate
      assert isinstance(self.__field_type__, type)
      assert isinstance(self.__field_name__, str)
    if isinstance(value, self.__field_type__):
      try:
        store = instance.__dict__
      except AttributeError as attributeError:
        fieldName = self.__field_name__
        raise MissingInstanceDict(instance, fieldName) from attributeError
      if self.__private_name__ is None:
        raise MissingVariable(self, '__field_name__', str)
      store[self.__private_name__] = value
      return
    raise TypeException(self.__field_name__, value, self.__field_type__)

  def __delete__(self, instance: Any) -> None:
    """
    A deleted attribute starts over from the declared value at the next
    read.

    Parameters
    ----------

    instance : Any
      The instance deleted through.

    Raises
    ------

    MissingVariable
      The instance holds no value, or the box never learned its name.

    MissingInstanceDict
      The instance has no '__dict__'.
    """
    if TYPE_CHECKING:  # pragma: no cover, no mutate
      assert isinstance(self.__field_name__, str)
    try:
      store = instance.__dict__
    except AttributeError as attributeError:
      fieldName = self.__field_name__
      raise MissingInstanceDict(instance, fieldName) from attributeError
    if self.__private_name__ is None:
      raise MissingVariable(self, '__field_name__', str)
    try:
      del store[self.__private_name__]
    except KeyError as keyError:
      raise MissingVariable(instance, self.__field_name__) from keyError

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _build(self) -> Any:
    fieldType = self.__field_type__
    if fieldType is None:
      raise MissingVariable(self, '__field_type__', type)
    if self.__declared_value__:
      return self.__declared_value__[0]
    value = fieldType()
    if isinstance(value, fieldType):
      return value
    raise TypeException(self.__field_name__, value, fieldType)

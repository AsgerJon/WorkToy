"""
AttriBox is a lazily built, strongly typed attribute descriptor.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

import copyreg
from copy import deepcopy, Error
from typing import TYPE_CHECKING, TypeVar, overload

from . import _RootAlias, Field, BaseDescriptor
from ..core import Object
from ..core.sentinels import DELETED, SentinelMeta, THIS
from ..dispatch import TypeSig
from ..utilities import typeCast, textFmt
from ..waitaminute import TypeException, MissingVariable
from ..waitaminute.desc import MissingInstanceDict
from ..waitaminute.dispatch import TypeCastException

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any, Self, Union, Optional, TypeAlias

  FieldType: TypeAlias = Union[type, TypeVar]

T = TypeVar('T')


class AttriBox(BaseDescriptor[T]):
  """
  A class with typed attributes and defaults would otherwise need an
  '__init__' assigning each one, a property per attribute to check its
  type, and care that no two instances share a mutable default. Some
  defaults cannot even be built when the class body runs: a Qt widget
  needs a running application, and a part may need the very instance it
  belongs to. A declaration in the class body must therefore give the
  type and the arguments of the default, and leave the building to the
  first read, for each instance apart. An assigned value must be held to
  the type, converting what converts without loss, as an 'int' for a
  'float', and refusing the rest; and the class must be able to react to
  reads and writes.

    class Point(BaseObject):
      x = AttriBox[float](0.)
      y = AttriBox[float](0.)

    class Circle(BaseObject):
      center = AttriBox[Point](69, 420)
      radius = AttriBox[float](1.)

  Implementation
  --------------

  The subscript fixes the field type and the parentheses keep the
  arguments. At the first read through an instance, the constructor of
  the field type is called with them, 'Point(69, 420)', and the result is
  kept in the instance dictionary under '__center__attribox_field_object__'
  and returned by every later read. Among the arguments, 'THIS' becomes
  the instance, 'OWNER' its class and 'DESC' the box; a placeholder
  inside a container is left alone. A single argument already of the
  field type is deep-copied instead, so 'AttriBox[list](['a'])' gives
  each instance a list of its own; one that cannot be copied, such as a
  lock, raises 'TypeError' at the first read. 'AttriBox[THIS]' types the
  attribute with the class declaring it.

  An assigned value of the field type is kept as it is, so a 'bool' in
  an 'AttriBox[int]' stays a 'bool'; any other goes through 'typeCast':
  numbers among numbers and texts among texts without loss, anything
  else only through a classmethod '__cast_as__' of the field type. No
  constructor runs on an assigned value. A deletion stores 'DELETED', so
  the next read raises 'MissingVariable' until the attribute is assigned
  again. The notification decorators of 'BaseDescriptor' apply, an
  'onSet' callback receiving the value as stored.

  An 'Object' the box builds is tagged with '__field_name__',
  '__field_owner__' and '__field_box__', so that it can ask the box for
  the instance of the access in progress; any other value is held
  untagged, whatever field type the box declares. A default whose copy is
  the default itself, such as a function, is untagged as well, since the
  box built nothing there. Copying a box gives the box itself,
  and a placed box
  pickles as a reference to its class and name, so instances holding
  box-built values copy and pickle. As the class is created, a box never
  subscripted, a box declared without parentheses and a class whose
  instances have no '__dict__' are refused, before Python 3.12 inside a
  'RuntimeError'. The parentheses reach the '__init__' of the class of the
  box, so a subclass of 'AttriBox' may take options of its own there.
  'FastBox' is the strict and fast alternative.

  Attributes
  ----------

  fieldType : type
    The field type, read-only.

  __field_type__ : type or None
    The field type as stored, 'THIS' until the box is placed.

  __storage_name__ : str or None
    The cached key in the instance dictionary.

  __reads_plainly__ : bool or None
    Whether the read hooks and the fetch are those of 'AttriBox', settled
    at the first read through an instance and 'None' until then.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private Variables
  __field_type__: Optional[type] = None
  __storage_name__: Optional[str] = None  # kept by '_getStorageName'
  __reads_plainly__: Optional[bool] = None  # kept by '_settleReadsPlainly'

  #  Public Variables
  fieldType: Field[type] = Field()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @fieldType.GET
  def getFieldType(self) -> type:
    """
    Code holding a box must be able to ask which class its values are
    instances of, 'THIS' already resolved.

    Returns
    -------

    type
      The field type.

    Raises
    ------

    MissingVariable
      The box was never subscripted.
    """
    if self.__field_type__ is None:
      raise MissingVariable(self, '__field_type__', type)
    return self.__field_type__

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _clearStorageName(self) -> None:
    """
    A box placed at a name must build its storage name from that name,
    though a clone carries the cached name of the box it was made from:
    'BaseDescriptor.clone' copies the dictionary of the box. The cache is
    cleared.
    """
    object.__setattr__(self, '__storage_name__', None)

  def _getStorageName(self, **kwargs) -> str:
    """
    Each instance keeps its value in its own dictionary, under a key no
    other field of the class shares, and that a box of another class at
    the same name, as a 'FixBox', does not share either.

    Implementation
    --------------

    The key joins the field name and the lowercased name of the box class,
    '__x__attribox_field_object__' for an 'AttriBox' at 'x'. It is cached;
    '__set_name__' clears the cache, so a clone placed at another name
    builds its own.

    Returns
    -------

    str
      The key.

    Raises
    ------

    MissingVariable
      The box was never placed in a class.

    TypeException
      The cache holds something other than a 'str'.
    """
    if self.__storage_name__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      if self.getFieldOwner() is None:
        raise MissingVariable(self, '__field_name__', str)
      fieldName = self.getFieldName()
      boxName = type(self).__name__.lower()
      storageName = '__%s__%s_field_object__' % (fieldName, boxName)
      object.__setattr__(self, '__storage_name__', storageName)
      return self._getStorageName(_recursion=True)  # pragma: no mutate
    if isinstance(self.__storage_name__, str):
      return self.__storage_name__
    raise TypeException('__storage_name__', self.__storage_name__, str)

  def _resolve(self, *args, **kwargs) -> T:
    """
    Each instance needs a value of its own, built from the arguments of
    the declaration at its first read.

    Implementation
    --------------

    A lone argument already of the field type, and no placeholder among
    the arguments, is deep-copied; otherwise the constructor of the field
    type is called with the arguments, and whatever it raises reaches the
    read as it is. An 'Object' the box builds is tagged after it is built,
    so its constructor cannot ask for 'self.instance'. A copy that is the
    default
    itself, as the copy of a class, of a function or of an object whose
    class answers a copy with itself is, is returned untagged, since the
    box built nothing.

    Parameters
    ----------

    *args
      The positional arguments of the declaration, placeholders replaced.

    **kwargs
      The keyword arguments of the declaration, placeholders replaced.

    Returns
    -------

    T
      The value.

    Raises
    ------

    TypeError
      A lone argument of the field type cannot be copied.

    TypeException
      The constructor returned something that is not of the field type.
    """
    fieldType = self.getFieldType()
    if len(args) == 1 and not kwargs and not self.hasSentinelArgs():
      if isinstance(args[0], fieldType):
        try:
          argCopy = deepcopy(args[0])
        except (Error, TypeError, ValueError) as exception:
          infoSpec = """The default of '%s.%s' is a '%s' that cannot be
          copied, so each instance cannot have its own. Give the box the
          arguments of the '%s' constructor instead: '%s[%s](...)'."""
          typeName = fieldType.__name__
          info = infoSpec % (
              self.getFieldOwner().__name__, self.getFieldName(), typeName,
              typeName, type(self).__name__, typeName,
          )
          raise TypeError(textFmt(info)) from exception
        else:
          if argCopy is args[0]:
            #  This branch is reached by the following:
            #  - The default is a class or a function, which a copy hands
            #    back as it is
            #  - The class of the default answers a copy with the default
            #    itself, as an enumeration member does
            return argCopy
          #  The rest of this branch is reached by the following:
          #  - The copy of the default is a new object
          return self._applyTags(argCopy)
    fieldObject = fieldType(*args, **kwargs)
    if isinstance(fieldObject, fieldType):
      return self._applyTags(fieldObject)
    raise TypeException(self.getFieldName(), fieldObject, fieldType)

  def _applyTags(self, fieldObject: Any, ) -> T:
    """
    An 'Object' the box builds must be able to ask its box for the
    instance and the owner of the access in progress, through
    'self.instance' and 'self.owner', and code holding only such a value
    must be able to tell where it belongs: the class declaring it, the
    name it is declared at, and the box that built it. The tags mean
    built by, not held by.

    Implementation
    --------------

    The three tags are written with 'object.__setattr__' when the value is
    an 'Object', whose instances always have a '__dict__'. Anything else,
    a plain value, a builtin or a class, is returned as it is, whatever
    field type the box declares, since nothing could read the tags off
    it. An assigned value is never tagged.

    Parameters
    ----------

    fieldObject : Any
      The value the box built.

    Returns
    -------

    T
      The same value.
    """
    #  Only an 'Object' can ask its box for anything; the tags serve that.
    if not isinstance(fieldObject, Object):
      return fieldObject
    object.__setattr__(fieldObject, '__field_name__', self.getFieldName())
    object.__setattr__(fieldObject, '__field_owner__', self.getFieldOwner())
    object.__setattr__(fieldObject, '__field_box__', self)
    return fieldObject

  def _store(self, instance: Any, value: Any) -> None:
    """
    A class guarding its attributes with a '__setattr__' of its own must
    not stand in the way of its boxes, and a class whose instances have no
    '__dict__' must be named in the error.

    Raises
    ------

    MissingVariable
      The box was never placed in a class.

    MissingInstanceDict
      The instance has no '__dict__'.
    """
    pvtName: str = self._getStorageName()
    try:
      object.__setattr__(instance, pvtName, value)
    except AttributeError as attributeError:
      if self.getFieldOwner() is None:
        raise MissingVariable(
            self,
            '__field_name__',
            str
        ) from attributeError
      fieldName = self.getFieldName()
      raise MissingInstanceDict(instance, fieldName) from attributeError

  def __instance_get__(self, instance: Any, owner: type, **kwargs) -> T:
    """
    A read through an instance must give the value of that instance,
    building it at the first read and the same object at every later one.
    A read made by a deletion must report what is stored and build
    nothing.

    Parameters
    ----------

    instance : Any
      The instance read through.

    owner : type
      The class of the instance.

    **kwargs
      '_deleting=True' from 'Object.__delete__'.

    Returns
    -------

    T
      The value, or 'DELETED', which 'Object.__get__' turns into
      'MissingVariable'.
    """
    pvtName = self._getStorageName()
    try:
      value = object.__getattribute__(instance, pvtName)
    except AttributeError as attributeError:
      if kwargs.get('_deleting', False):
        raise attributeError
      if kwargs.get('_recursion', False):
        raise RecursionError from attributeError
      args = self.getPosArgs()
      kwargs = self.getKeyArgs()
      fieldObject = self._resolve(*args, **kwargs)
      self._store(instance, fieldObject)
      return self.__instance_get__(
          instance, owner, _recursion=True)  # pragma: no mutate
    else:
      return value

  def _cast(self, value: Any) -> T:
    """
    An assigned value of another type must be converted where nothing is
    lost, and refused with an error naming the attribute otherwise.

    Implementation
    --------------

    'typeCast' converts; its 'TypeCastException' is raised again as a
    'TypeException' naming the field.

    Parameters
    ----------

    value : Any
      The value assigned.

    Returns
    -------

    T
      The value converted.

    Raises
    ------

    TypeException
      'typeCast' refuses the value.
    """
    fieldType = self.getFieldType()
    try:
      return typeCast(fieldType, value)
    except TypeCastException as typeCastException:
      fieldName = self.getFieldName()
      raise TypeException(fieldName, value, fieldType) from typeCastException

  def __instance_set__(self, instance: Any, value: Any, **kwargs) -> T:
    """
    A write must store a value of the field type, as assigned when it is
    one, converted when it is not.

    Parameters
    ----------

    instance : Any
      The instance written through.

    value : Any
      The value assigned.

    Returns
    -------

    T
      The value as stored, which the 'onSet' callbacks receive.

    Raises
    ------

    TypeException
      The value is not of the field type and does not convert.
    """
    if isinstance(value, self.getFieldType()):
      self._store(instance, value)
      return value
    if kwargs.get('_recursion', False):
      raise RecursionError
    cast = self._cast(value)
    return self.__instance_set__(
        instance, cast, _recursion=True)  # pragma: no mutate

  def __instance_delete__(self, instance: Any, *_, **kwargs) -> None:
    """
    After a deletion the next read must fail, and must not build the
    default again.

    Implementation
    --------------

    'DELETED' is stored. An attribute never read builds nothing on the
    way.
    """
    self._store(instance, DELETED)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  # @formatter:off
  @overload
  def __get__(self, instance: None, owner: type) -> Self: ...
  @overload
  def __get__(self, instance: Any, owner: type) -> T: ...
  # @formatter:on

  def _settleReadsPlainly(self, ) -> None:
    """
    The '_settleReadsPlainly' method settles, once for the box, whether a
    read through it runs no code but that of 'AttriBox': 'hookPreGet',
    'hookOnGet' and '__instance_get__' are looked up on the class of the
    box, and '__reads_plainly__' is True when all three are those of
    'AttriBox', False when a subclass overrides one.
    """
    cls = type(self)
    plain = True
    for name in ('hookPreGet', 'hookOnGet', '__instance_get__'):
      if getattr(cls, name) is not getattr(AttriBox, name):
        plain = False
    object.__setattr__(self, '__reads_plainly__', plain)

  def __get__(self, instance: Any, owner: type) -> Union[Self, T]:
    """
    Read through the class, the box must give itself, for inspection or
    for registering callbacks; read through an instance, the value. By
    far the most reads are of a value already stored, through a box with
    no read callback, and such a read runs no code of the builder: it
    has no use for the frame or for the hook phases, which cost many
    times the read itself, and must not pay for them.

    Implementation
    --------------

    When no read callback is registered and the hooks and the fetch are
    those of 'AttriBox', the stored value is taken from the instance and
    returned, unless it is 'DELETED'. Every other read is the full read
    of 'Object.__get__': the first read of an instance, which builds the
    value, a deleted value, and a storage name that is no name, each of
    which is refused or handled there as before. The callbacks are
    looked at on every read, since one may be registered after reads
    were made.

    Raises
    ------

    MissingVariable
      The box has no field type or no name, as a box installed with
      'setattr' after the class was created.
    """
    if instance is None:
      return super().__get__(instance, owner)
    if self.__field_type__ is None:
      raise MissingVariable(self, '__field_type__', type)
    if not (self.__pre_get_keys__ or self.__on_get_keys__):
      if self.__reads_plainly__ is None:
        self._settleReadsPlainly()
      if self.__reads_plainly__:
        try:
          value = object.__getattribute__(instance, self.__storage_name__)
        except (AttributeError, TypeError):
          #  This branch is reached by the following:
          #  - The first read of an instance, which has no value yet
          #  - A storage name not yet made, or one that is no 'str'
          pass
        else:
          if value is not DELETED:
            return value
    return super().__get__(instance, owner)

  def __copy__(self) -> Self:
    """
    Copying a box gives the box itself; see '__deepcopy__'.
    """
    return self

  def __deepcopy__(self, memo: dict) -> Self:
    """
    A value the box built names the box in '__field_box__', so a deep copy
    of the value, or of the instance holding it, reaches the box. A copy
    of the box would be a descriptor on no class, and the copied value
    must keep naming the box its class declares.

    Implementation
    --------------

    The box itself is returned. A separate box is made by subscripting and
    calling the box class again.
    """
    return self

  def __reduce__(self) -> tuple:
    """
    An instance holding box-built values must survive 'pickle', tags
    included, so an unpickled value must find the very box its class
    declares.

    Implementation
    --------------

    A placed box pickles as 'getattr' of its class and name; an unplaced
    one by its state, spelled out because 'object.__reduce_ex__' would
    call back into this method.
    """
    owner, name = self.__field_owner__, self.__field_name__
    if owner is None or name is None:
      #  The default protocol, spelled out: 'object.__reduce_ex__' would
      #  call back into this method.
      return copyreg.__newobj__, (type(self),), self.__dict__
    return getattr, (owner, name)

  @classmethod
  def __class_getitem__(cls, fieldType: FieldType) -> Self:
    """
    'AttriBox[int]' must give a box, of the class subscripted, so
    'FixBox[int]' gives a 'FixBox'. 'AttriBox[THIS]' must give a box typed
    with the class being defined. A subscript meant for 'typing', as in
    'class Sub(AttriBox[T])', must give a type alias instead, which fails
    if bound in a class body as if it were a box. A class 'isinstance'
    refuses, as 'typing.Any' is from Python 3.11 on and a 'Protocol' that
    is not '@runtime_checkable' is, must be refused at the subscript, since
    no value could ever be checked against it; the overload signatures
    hold their classes to the same rule, and the rule has one place.

    Implementation
    --------------

    A plain class or 'THIS' makes a box once 'TypeSig.validateTypes' has
    checked it, given the subscript as the declaration to name.

    Parameters
    ----------

    fieldType : FieldType
      A 'Union[type, TypeVar]': the class of the values, or a type
      variable for a generic subclass.

    Returns
    -------

    AttriBox or _RootAlias
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
      self = object.__new__(cls)
      object.__setattr__(self, '__field_type__', fieldType)
      return self  # noqa
    try:
      out = super().__class_getitem__(fieldType)
    except Exception as exception:
      name, value = 'fieldType', fieldType
      raise TypeException(name, value, type, TypeVar) from exception
    else:
      return _RootAlias.fromAlias(out)

  def __call__(self: Any, *args, **kwargs) -> Self:
    """
    The parentheses of the declaration hold the arguments of the default,
    kept until the first read. A placed box called again, as 'Holder.n(5)',
    would change the default of every instance not yet read, and is
    refused.

    Parameters
    ----------

    *args
      Positional arguments for the constructor, placeholders allowed.

    **kwargs
      Keyword arguments for the constructor, placeholders allowed.

    Returns
    -------

    AttriBox
      The box itself.

    Raises
    ------

    TypeError
      The box is placed in a class already.
    """
    if self.__field_owner__ is not None:
      infoSpec = """The box at '%s.%s' took the arguments of its default as
      its class was created, and cannot take new ones."""
      ownerName = self.__field_owner__.__name__
      info = infoSpec % (ownerName, self.__field_name__)
      raise TypeError(textFmt(info))
    self.__init__(*args, **kwargs)
    return self

  def __set_name__(self, owner: type, name: str, **kwargs) -> None:
    """
    A wrong declaration must fail on the class statement, not at some later
    read: a box never subscripted, a box declared without parentheses, and
    a class whose instances have no '__dict__' to keep values in.

    Implementation
    --------------

    'THIS' as field type becomes the class, a box that never received its
    arguments is refused, and the cached key is cleared before
    'BaseDescriptor.__set_name__' handles a second name or a second class.
    A box receives its arguments when its parentheses reach
    'Object.__init__', so a subclass whose '__init__' does not hand on to
    'AttriBox.__init__' is refused the same way.

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
      The box never received its arguments.

    SharedDescriptor
      The box is placed on another class already.
    """
    if self.__field_type__ is None:
      raise MissingVariable(self, '__field_type__', type)
    #  '__dictoffset__' is zero iff 'owner' instances have no '__dict__'
    if not type.__getattribute__(owner, '__dictoffset__'):
      raise MissingInstanceDict(owner, name)
    if self.__field_type__ is THIS:
      object.__setattr__(self, '__field_type__', owner)
    if self.__pos_args__ is None:
      infoSpec = """The box at '%s.%s' is declared without parentheses. A
      box takes the arguments of its default in parentheses, as '%s[%s]()'
      for none. A subclass of 'AttriBox' whose '__init__' does not hand on
      to 'AttriBox.__init__' is refused the same way."""
      boxName = type(self).__name__
      typeName = self.__field_type__.__name__
      info = infoSpec % (owner.__name__, name, boxName, typeName)
      raise TypeError(textFmt(info))
    self._clearStorageName()
    super().__set_name__(owner, name, **kwargs)

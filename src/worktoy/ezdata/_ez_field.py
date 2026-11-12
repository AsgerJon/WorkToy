"""
EZField is the declaration of one attribute in an 'EZData' class body.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from copy import deepcopy, Error
from typing import TYPE_CHECKING, TypeVar, Generic

from ..core.sentinels import THIS, SentinelMeta
from ..desc import Field
from ..dispatch import TypeSig
from ..mcls import BaseObject
from ..utilities import maybe, typeCast, hasCastRule, textFmt
from ..waitaminute import MissingVariable, TypeException
from ..waitaminute.dispatch import TypeCastException

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any, Union, Optional, Self, Type

T = TypeVar('T')


class EZField(BaseObject, Generic[T]):
  """
  A dataclass declares its fields in its class body, and one declaration
  must say two things: the class every value of the field is held to, and
  how the default of the field is made. A bare value in the body can say
  neither outright. Its type has to be taken as the type of the field,
  exactly, so that 'x = 0' declares an 'int' field that refuses '0.5',
  and nothing tells the line from a constant of the class. A builder
  needs a declaration that states both, to be recommended for every
  field. The default must be a recipe and not a value, so that no two
  instances share a mutable default. The declaration should read as the
  declaration of a box reads, the type in a subscript and the arguments
  of the default in parentheses, since that is the spelling a builder
  already knows. A declaration missing either half, or one made in a
  class that is no dataclass, is a mistake that must fail where it is
  written.

  Implementation
  --------------

  'EZField[T](...)' is the recommended way to declare a field of an
  'EZData' class: 'x = EZField[float](0)' says in one line that it
  declares a field, of which type and with which default. A bare value
  in the body declares a field as well, of the type of the value;
  'EZHook' wraps it into a field through 'fromValue'.

  'EZField[T]' gives a field of type 'T' through '__class_getitem__', and
  the call that follows keeps the arguments of the default. '_construct'
  builds a default from them, anew at every call. The shapes it takes:

  - 'EZField[T](value)' : type 'T', default a copy of 'value' when it
    already is a 'T', the cast of 'value' when 'T' is a text or a number
    type, and 'T(value)' otherwise, with whatever 'T' makes of the
    value: 'EZField[list]('abc')' defaults to the three letters, as
    'list('abc')' does.
  - 'EZField[T]()' : type 'T', default 'T()'.
  - 'EZField[T](*args, **kwargs)' : type 'T', default
    'T(*args, **kwargs)'.
  - 'EZField.fromValue(v)' : type 'type(v)', default a copy of 'v'.
    'EZHook' wraps a bare class-body value this way.

  Two shapes are refused as the class body binds them, with
  'IncompleteFieldException': 'EZField(value)', which has no type, and
  'EZField[T]', which has no parentheses.

  A subclass of 'EZField' takes options of its own in the same
  parentheses: '__call__' hands them to the '__init__' of the subclass,
  which keeps what is its own and hands the arguments of the default on
  to 'EZField.__init__'. A clone is of the class of the field and holds
  what the field holds; see 'clone_'.

  The field is never placed on its class. 'EZHook' claims it before the
  namespace stores it, so 'Object.__set_name__' never runs for it;
  'EZSpace.registerEZField' gives it its name and 'EZMeta.__init__' its
  owner. Bound in any other class body, it is refused with a 'TypeError'
  saying so; see 'hookSetName'. The placeholders 'THIS', 'OWNER' and
  'DESC' of a box are not resolved in a field recipe: a field keeps no
  access in progress, and the arguments of the recipe reach the field
  type as written.

  Attributes
  ----------

  fieldOwner : type
    The EZData subclass the field is bound to, set by 'EZMeta.__init__'
    after the class is created.

  fieldName : str
    The name the field is declared at, set by 'EZSpace.registerEZField'
    as the class body binds it.

  fieldType : type[T]
    The declared type of the values the field holds.

  posArgs : tuple
    The positional arguments of the default.

  keyArgs : dict
    The keyword arguments of the default.

  defaultValue : T
    A new default, built by the rules of '_construct' at every read, so
    that mutable defaults are not shared between instances.

  Examples
  --------

      class Point2D(EZData):
        x = EZField[float](0.0)
        y = EZField[float](0.0)

      class Bag(EZData):
        items = EZField[list]()        # default to a fresh []
        labels = EZField[dict]()       # default to a fresh {}

      class Person(EZData):
        name = EZField[FullName]('Doe', givenNames='John')
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  STATIC METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @staticmethod
  def _construct(fieldType: type, name: str, args: tuple, kwargs: dict) -> T:
    """
    The default of a field must be built from the arguments of its
    declaration, as a box builds its default from its parentheses, anew for
    every instance, so that instances share nothing. A lone argument is
    meant as a value for the field, not as an argument of a constructor:
    one already of the field type must become each instance's own copy,
    nested state included, and one of another type must be converted as a
    value given to the field later is, or refused. Whatever is built must
    be an instance of the field type, since a field always holds one. A
    refusal must speak of the mistake that was made: a value of a wrong
    type, or a default that could not be built.

    Implementation
    --------------

    A lone argument without keywords that already is an instance of
    'fieldType' is deep-copied by '_copyValue', as the box deep-copies its
    default. Calling the field type on it is no copy for every type, as
    'Point(Point(1, 2))' shows, while the copy gives each instance an
    object of its own, and an enumeration member or an immutable value
    copies to itself. For a field type 'typeCast' decides for, a family
    builtin, a subclass of one or a class declaring '__cast_as__', the lone
    argument is cast or refused by '_castValue', where the box calls the
    constructor. For any other class it is the one argument of the
    constructor. Several arguments, keywords or none call the constructor.

    A result that is no instance of the field type raises 'TypeException'
    naming the field. A constructor raising 'TypeError' or 'ValueError'
    over a lone value raises 'TypeException' too, since that value is of a
    wrong type for the field. Over several arguments, keywords or none, no
    value is of a wrong type: the default could not be built, and
    '_unbuiltDefault' words the 'TypeError'. Both 'defaultValue' and the
    default recipes of the generated '__init__' build their values here.

    Parameters
    ----------

    fieldType : type
      The field type.

    name : str
      The field name, for the refusals.

    args : tuple
      The positional arguments of the declaration.

    kwargs : dict
      The keyword arguments of the declaration.

    Returns
    -------

    T
      The default, an instance of 'fieldType'.

    Raises
    ------

    TypeException
      The cast refuses the lone value, the constructor refuses the lone
      value, or the call returns something that is no instance of
      'fieldType'.

    TypeError
      A lone value of the field type cannot be copied; see '_copyValue'.
      The constructor refuses several arguments, keywords or none; see
      '_unbuiltDefault'.
    """
    if len(args) == 1 and not kwargs:
      value = args[0]
      if isinstance(value, fieldType):
        return EZField._copyValue(fieldType, name, value)
      if hasCastRule(fieldType):
        return EZField._castValue(fieldType, name, value)
    try:
      value = fieldType(*args, **kwargs)
    except (TypeError, ValueError) as exception:
      if len(args) == 1 and not kwargs:
        #  This branch is reached by the following:
        #  - The lone value is the one argument of the constructor, which
        #    refused it
        raise TypeException(name, args[0], fieldType) from exception
      #  The rest of this branch is reached by the following:
      #  - The constructor refused several arguments, keywords or none
      raise EZField._unbuiltDefault(fieldType, name) from exception
    if isinstance(value, fieldType):
      return value
    raise TypeException(name, value, fieldType)

  @staticmethod
  def _unbuiltDefault(fieldType: type, name: str) -> TypeError:
    """
    A field declared with several arguments, with keywords or with empty
    parentheses takes its default from a call of the field type, and a
    field type that takes no empty call is the plain way to declare a
    field with no sensible default. When that call is refused, nobody
    gave the field a value of a wrong type, so the refusal must not read
    as if somebody had: it names the field and the field type, says that
    the default could not be built, and gives both ways out.

    Implementation
    --------------

    The exception is returned, not raised, so that '_construct' raises
    it chained from the refusal of the constructor, which holds the
    constructor's own words.

    Parameters
    ----------

    fieldType : type
      The field type whose constructor refused the call.

    name : str
      The field name.

    Returns
    -------

    TypeError
      The refusal, to be raised.
    """
    infoSpec = """The default of the field '%s' could not be built: '%s'
    refused the call the declaration describes. Declare the field with
    arguments '%s' accepts, as 'EZField[%s](...)', or give the field a
    value when the instance is made."""
    typeName = fieldType.__name__
    info = infoSpec % (name, typeName, typeName, typeName)
    return TypeError(textFmt(info))

  @staticmethod
  def _copyValue(fieldType: type, name: str, value: Any) -> Any:
    """
    A lone default already of the field type must become a value of each
    instance's own, with everything nested in it, as the default of a box
    does: the declaration is a recipe materialized per instance. A value
    that cannot be copied, as a lock, can be no instance's own, and the
    refusal must name the field and the way out.

    Implementation
    --------------

    'copy.deepcopy' makes the copy. Its 'copy.Error', 'TypeError' or
    'ValueError' becomes a 'TypeError' naming the field and pointing at the
    arguments of the constructor, chained from the copy's own error.

    Parameters
    ----------

    fieldType : type
      The field type, for the message.

    name : str
      The field name, for the message.

    value : Any
      The lone default, an instance of 'fieldType'.

    Returns
    -------

    Any
      The copy.

    Raises
    ------

    TypeError
      The value cannot be copied.
    """
    try:
      return deepcopy(value)
    except (Error, TypeError, ValueError) as exception:
      infoSpec = """The default of the field '%s' is a '%s' that cannot
      be copied, so each instance cannot have its own. Give the field the
      arguments of the '%s' constructor instead: 'EZField[%s](...)'."""
      typeName = fieldType.__name__
      info = infoSpec % (name, typeName, typeName, typeName)
      raise TypeError(textFmt(info)) from exception

  @staticmethod
  def _castValue(fieldType: type, name: str, value: Any) -> Any:
    """
    A lone default of a text or a number type, or of a class that says how
    values convert to it, must be converted as a value assigned to the
    field is, and refused in the same words.

    Implementation
    --------------

    'typeCast' converts. Its 'TypeCastException' is raised again as a
    'TypeException' naming the field, chained.

    Parameters
    ----------

    fieldType : type
      The field type.

    name : str
      The field name, for the refusal.

    value : Any
      The lone default.

    Returns
    -------

    Any
      The value as an instance of 'fieldType'.

    Raises
    ------

    TypeException
      'typeCast' refuses the value.
    """
    try:
      return typeCast(fieldType, value)
    except TypeCastException as typeCastException:
      raise TypeException(name, value, fieldType) from typeCastException

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private variables
  __field_owner__: Optional[type] = None
  __field_name__: Optional[str] = None
  __field_type__: Optional[Type[T]] = None
  __pos_args__: Optional[tuple] = None
  __key_args__: Optional[dict] = None

  #  Public Variables
  fieldOwner: Field[type] = Field()
  fieldName: Field[str] = Field()
  fieldType: Field[Type[T]] = Field()
  posArgs: Field[tuple] = Field()
  keyArgs: Field[dict] = Field()
  defaultValue: Field[T] = Field()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @fieldOwner.GET
  def _getFieldOwner(self, ) -> type:
    """
    Code holding a field must be able to ask which dataclass the field
    belongs to, and a field no class has taken yet must say so rather than
    answer 'None'.

    Implementation
    --------------

    'EZMeta.__init__' writes '__field_owner__' once the class exists.

    Returns
    -------

    type
      The EZData subclass holding the field.

    Raises
    ------

    MissingVariable
      No class has taken the field yet.

    TypeException
      '__field_owner__' was set to something that is no class.
    """
    if self.__field_owner__ is None:
      raise MissingVariable(self, '__field_owner__', type)
    if isinstance(self.__field_owner__, type):
      return self.__field_owner__
    raise TypeException('__field_owner__', self.__field_owner__, type)

  @fieldName.GET
  def _getFieldName(self, ) -> str:
    """
    Code holding a field must be able to ask for the name it is declared
    at, and a field not yet registered must say so rather than answer
    'None'.

    Implementation
    --------------

    'EZSpace.registerEZField' writes '__field_name__' as the class body
    binds the field, and 'EZSpace.registerBaseField' for an inherited one.

    Returns
    -------

    str
      The name of the field on its class.

    Raises
    ------

    MissingVariable
      The field is not registered yet.

    TypeException
      '__field_name__' was set to something that is no string.
    """
    if self.__field_name__ is None:
      raise MissingVariable(self, '__field_name__', str)
    if isinstance(self.__field_name__, str):
      return self.__field_name__
    raise TypeException('__field_name__', self.__field_name__, str)

  @fieldType.GET
  def _getFieldType(self, ) -> Type[T]:
    """
    Code holding a field must be able to ask which class its values are
    held to, and a field declared without a subscript must say that it has
    none.

    Implementation
    --------------

    '__class_getitem__' writes '__field_type__' for 'EZField[T]', and
    'fromValue' for a bare class-body value.

    Returns
    -------

    type[T]
      The declared field type.

    Raises
    ------

    MissingVariable
      The field was made without a subscript, as 'EZField(1)'.

    TypeException
      '__field_type__' was set to something that is no class.
    """
    if self.__field_type__ is None:
      raise MissingVariable(self, '__field_type__', type)
    if isinstance(self.__field_type__, type):
      # noinspection PyTypeChecker
      return self.__field_type__
    raise TypeException('__field_type__', self.__field_type__, type)

  @posArgs.GET
  def _getPosArgs(self, ) -> tuple:
    """
    The positional arguments of the default must be readable from the
    field, and a field subscripted and never called, which holds none, must
    say so.

    Implementation
    --------------

    '__init__' writes '__pos_args__', and '__call__' hands the
    parentheses of a subscripted field to '__init__'.

    Returns
    -------

    tuple
      The positional arguments of the declaration.

    Raises
    ------

    MissingVariable
      The field was never called, as 'EZField[T]' without parentheses.

    TypeException
      '__pos_args__' was set to something that is no tuple.
    """
    if self.__pos_args__ is None:
      raise MissingVariable(self, '__pos_args__', tuple)
    if isinstance(self.__pos_args__, tuple):
      return self.__pos_args__
    raise TypeException('__pos_args__', self.__pos_args__, tuple)

  @keyArgs.GET
  def _getKeyArgs(self, ) -> dict:
    """
    The keyword arguments of the default must be readable from the field,
    beside the positional ones, and a field never called must say that it
    holds none.

    Implementation
    --------------

    '__init__' writes '__key_args__', and '__call__' hands the
    parentheses of a subscripted field to '__init__'.

    Returns
    -------

    dict
      The keyword arguments of the declaration.

    Raises
    ------

    MissingVariable
      The field was never called.

    TypeException
      '__key_args__' was set to something that is no dict.
    """
    if self.__key_args__ is None:
      raise MissingVariable(self, '__key_args__', dict)
    if isinstance(self.__key_args__, dict):
      return self.__key_args__
    raise TypeException('__key_args__', self.__key_args__, dict)

  @defaultValue.GET
  def _getDefaultValue(self, ) -> T:
    """
    Code holding a field must be able to ask for a default, and every
    answer must be a value of its own, so that nothing is shared between
    two that asked.

    Implementation
    --------------

    '_construct' builds the value from the field type and the arguments of
    the declaration, naming the field in a refusal, or 'defaultValue' when
    the field has no name yet. A lone default already of the field type is
    deep-copied, so two instances share nothing of a mutable default,
    nested state included. Several arguments reach the constructor as they
    are, so a mutable object among them is whatever the constructor makes
    of it.

    Returns
    -------

    T
      A new default for the field.

    Raises
    ------

    MissingVariable
      The field has no type or was never called; the getters asked here
      raise it.

    TypeException
      The lone default is of a wrong type, or the field type returns
      something that is no instance of it; see '_construct'.

    TypeError
      A lone default of the field type cannot be copied; see '_copyValue'.
      The constructor refuses several arguments, keywords or none; see
      '_unbuiltDefault'.
    """
    name = maybe(self.__field_name__, 'defaultValue')
    return self._construct(self.fieldType, name, self.posArgs, self.keyArgs)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, *args, **kwargs) -> None:
    """
    The parentheses of a declaration hold the arguments of the default,
    which must be kept until an instance needs one. The field type is no
    part of them: it comes from the subscript, or from the value itself for
    a bare class-body value.

    Implementation
    --------------

    The arguments are kept as given, under '__pos_args__' and
    '__key_args__'; see '_construct' for what is made of them. A subclass
    taking options of its own hands on to this method the arguments meant
    for the default.

    Parameters
    ----------

    *args
      The positional arguments of the default.

    **kwargs
      The keyword arguments of the default.
    """
    self.__pos_args__ = args
    self.__key_args__ = kwargs

  @classmethod
  def __class_getitem__(cls, type_: Type[T]) -> EZField:
    """
    'EZField[T]' must give a field of type 'T', ready to take the arguments
    of its default in the parentheses that follow. Every value of the field
    is checked against 'T' with 'isinstance', so a subscript no value could
    be checked against must fail where it is written: something that is no
    class, a class 'isinstance' refuses, and a sentinel, which stands for a
    meaning and is no type of value. 'THIS', which a box resolves to its
    owner, cannot type a field either: a field needs a default, and no
    value of the class being declared exists while its body runs.

    Implementation
    --------------

    The subscript counts as a class when its type is a metaclass, as the
    boxes judge theirs, since 'isinstance(list[int], type)' answers 'True'
    on Python 3.9 and 3.10. A sentinel other than 'THIS' is refused in the
    words of a field type. 'TypeSig.validateTypes', the one check of a
    declared type, the field types of the boxes included, checks the rest
    and names the declaration 'EZField[T]' in its refusal. 'THIS' is
    refused last. The field is made by '__new__' alone, so its arguments
    stay unset until it is called; one bound in a class body uncalled is
    refused by 'EZHook._assertCompleteField' with
    'IncompleteFieldException'.

    Parameters
    ----------

    type_ : type[T]
      The class of the values the field holds.

    Returns
    -------

    EZField
      A new field of that type, to be called with the arguments of its
      default.

    Raises
    ------

    TypeException
      'type_' is no class, such as 'list[int]' or a 'TypeVar'.

    UncheckableType
      'type_' is a class 'isinstance' refuses, as 'typing.Any' is from
      Python 3.11 on and a 'Protocol' that is not '@runtime_checkable' is.

    TypeError
      'type_' is a sentinel, 'THIS' included.
    """
    if not issubclass(type(type_), type):
      raise TypeException('fieldType', type_, type)
    declaration = '%s[%s]' % (cls.__name__, type_.__name__)
    if isinstance(type_, SentinelMeta) and type_ is not THIS:
      infoSpec = """The subscript '%s' names a sentinel as the field
      type. A sentinel stands for a meaning, such as the enclosing class,
      and is no type of value a field could hold; the field type is the
      class of the values the field holds."""
      raise TypeError(textFmt(infoSpec % declaration))
    TypeSig.validateTypes(type_, variadic=False, declaration=declaration)
    if type_ is THIS:
      infoSpec = """The subscript '%s' names 'THIS', the class being
      declared, as the field type. A field needs a default, and no value
      of that class exists while its body runs, so a field cannot be
      typed with it."""
      raise TypeError(textFmt(infoSpec % declaration))
    self = cls.__new__(cls)
    setattr(self, '__field_type__', type_)
    return self

  def __call__(self, *args, **kwargs) -> Self:
    """
    The canonical declaration is one expression, 'EZField[T](...)': the
    subscript gives the field, and the call must give it the arguments of
    its default and hand the same field back. A subclass of 'EZField'
    that carries options of its own, a unit or a line of description,
    must be able to take them in the same parentheses, as a subclass of
    'AttriBox' takes its own.

    Implementation
    --------------

    The arguments go to the '__init__' of the class of the field, and the
    field is returned. 'EZField.__init__' stores them as the arguments of
    the default; the '__init__' of a subclass keeps what is its own and
    hands the rest on to it. Calling a field again runs '__init__' again,
    which replaces what the field held. A subclass whose '__init__' hands
    nothing on leaves the field without arguments, and
    'EZHook._assertCompleteField' refuses it as the class body binds it.

    A field a class holds is refused, as a placed box is. The constructor
    of the class took the recipe of the default as the class was created,
    so new arguments would change what the field says and leave what the
    class does as it was. A clone is bound to no class and takes them.

    Parameters
    ----------

    *args
      The positional arguments of the default.

    **kwargs
      The keyword arguments of the default.

    Returns
    -------

    Self
      The field itself.

    Raises
    ------

    TypeError
      The field belongs to a class already.
    """
    if self.__field_owner__ is not None:
      infoSpec = """The field at '%s.%s' took the arguments of its default
      as its class was created, and cannot take new ones."""
      ownerName = self.__field_owner__.__name__
      info = infoSpec % (ownerName, self.__field_name__)
      raise TypeError(textFmt(info))
    self.__init__(*args, **kwargs)
    return self

  @classmethod
  def fromValue(cls, value: Any) -> Self:
    """
    A bare value in a dataclass body, as 'name = 'Anonymous'', declares a
    field too: its type is the type of the value, and the value is the
    default.

    Implementation
    --------------

    A field is made with the value as its one argument and 'type(value)' as
    its field type. 'EZHook.setItemPhase' wraps bare values this way. A
    bare 'None' never arrives here: the hook refuses it with
    'IncompleteFieldException', since no field type can be taken from it.

    Parameters
    ----------

    value : Any
      The value bound in the class body.

    Returns
    -------

    EZField
      A field of type 'type(value)' with '(value,)' as its positional
      arguments.
    """
    self = cls(value)
    setattr(self, '__field_type__', type(value))
    return self

  @classmethod
  def clone_(cls, self: Self) -> EZField[T]:
    """
    A subclass inherits the fields of its bases, and each class must hold
    field objects of its own, since a field carries the name and the owner
    it is bound to. A field bound to a second name in one body, or in a
    second class, needs an object of its own for the same reason. In
    every other respect the new object must be the same field: what a
    subclass of 'EZField' keeps beside the field type and the arguments
    of the default must come along, and making the copy must not ask for
    the options of that subclass a second time.

    Implementation
    --------------

    A new field of 'cls' is made by '__new__' alone, so no '__init__'
    runs, and takes every entry of the instance dictionary of the given
    field except its name, its owner and the private name 'Object' caches
    from the name, as 'BaseDescriptor.clone' copies a descriptor. The
    entries are the objects the given field holds, not copies of them.
    The name and the owner stay unset until the new field is registered.
    'EZSpace.registerBaseField' and 'EZSpace.registerEZField' clone
    through 'clone', where 'cls' is the class of the field.

    Parameters
    ----------

    self : EZField
      The field to clone.

    Returns
    -------

    EZField
      A field of 'cls' holding what the given field holds, bound to
      nothing.
    """
    other: EZField[T] = cls.__new__(cls)
    skipped = ('__field_owner__', '__field_name__', '__private_name__')
    for key, value in vars(self).items():
      if key not in skipped:
        object.__setattr__(other, key, value)
    return other

  def clone(self, ) -> EZField[T]:
    """Instance-shaped alias for 'clone_(self)'."""
    return self.clone_(self)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  if TYPE_CHECKING:  # pragma: no cover, no mutate
    # @formatter:off
    from typing import overload
    @overload
    def __get__(self, instance: None, owner: type) -> Self: ...
    @overload
    def __get__(self, instance: Any, owner: type) -> T: ...
    def __get__(self, instance: Any, owner: type) -> Union[Self, T]: ...
    # @formatter:on

  def hookSetName(self, owner: type, name: str, **kwargs) -> None:
    """
    A field bound in the body of a class that is no dataclass would sit
    there as every 'Object' does, reading as itself and refusing writes,
    which says nothing about the mistake. The class statement must fail
    instead, saying where a field belongs.

    Implementation
    --------------

    'Object.__set_name__' calls this hook for a field the interpreter
    places, which happens only in the body of a class not built by
    'EZMeta': in an 'EZData' body 'EZHook' claims the field before the
    namespace stores it, so the interpreter never places it. The hook
    always raises. Before Python 3.12 the interpreter hands the error on
    wrapped in 'RuntimeError'.

    Parameters
    ----------

    owner : type
      The class whose body bound the field.

    name : str
      The name it was bound to.

    Raises
    ------

    TypeError
      Always: the field was placed in the body of a class that is no
      'EZData' subclass.
    """
    infoSpec = """An 'EZField' declares a field of a dataclass and
    belongs in the body of an 'EZData' subclass, but '%s' is bound to one
    at '%s' and '%s' is no 'EZData' subclass."""
    info = infoSpec % (owner.__name__, name, owner.__name__)
    raise TypeError(textFmt(info))

  def __str__(self) -> str:
    """
    A field shown in a message or a log should read as the declaration a
    builder would recognise, with the class and the name it belongs to, and
    must not fail for a field that has neither yet.

    Implementation
    --------------

    The text is 'Owner.name: type(args)'. 'EZField', '<unbound>' and
    'object' stand in for an owner, a name and a type not set yet, so an
    unbound field reads 'EZField.<unbound>: object()'.

    Returns
    -------

    str
      The text of the field.
    """
    infoSpec = """%s.%s: %s(%s)"""
    ownerName = maybe(self.__field_owner__, type(self)).__name__
    fieldName = maybe(self.__field_name__, '<unbound>')
    fieldType = maybe(self.__field_type__, object).__name__
    posArgs = maybe(self.__pos_args__, ())
    posStr = ', '.join(repr(a) for a in posArgs)
    keyArgs = maybe(self.__key_args__, {})
    keyStr = ', '.join('%s=%r' % (k, v) for k, v in keyArgs.items())
    if posArgs and keyArgs:
      argStr = str.join(', ', (posStr, keyStr))
    elif posArgs:
      argStr = posStr
    elif keyArgs:
      argStr = keyStr
    else:
      argStr = ''
    return infoSpec % (ownerName, fieldName, fieldType, argStr)

  def __repr__(self) -> str:
    """
    The 'repr' of a field should be the expression that declares it, and
    must not fail for a field that is not complete yet.

    Implementation
    --------------

    The text is 'EZField[type](args)', with 'object' standing in for a type
    not set yet and empty parentheses for arguments not given.

    Returns
    -------

    str
      The declaration of the field.
    """
    infoSpec = """%s[%s](%s)"""
    clsName = type(self).__name__
    typeStr = maybe(self.__field_type__, object).__name__
    posArgs = maybe(self.__pos_args__, ())
    posStr = ', '.join(repr(a) for a in posArgs)
    keyArgs = maybe(self.__key_args__, {})
    keyStr = ', '.join('%s=%r' % (k, v) for k, v in keyArgs.items())
    if posArgs and keyArgs:
      argStr = str.join(', ', (posStr, keyStr))
    elif posArgs:
      argStr = posStr
    elif keyArgs:
      argStr = keyStr
    else:
      argStr = ''
    return infoSpec % (clsName, typeStr, argStr)

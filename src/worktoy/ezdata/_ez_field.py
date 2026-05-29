"""
EZField is the per-field descriptor declared in an 'EZData' class body.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, Generic

from ..desc import Field
from ..mcls import BaseObject
from ..utilities import maybe
from ..waitaminute import MissingVariable, TypeException

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Union, Optional, Self, Type

T = TypeVar('T')


class EZField(BaseObject, Generic[T]):
  """
  EZField is the per-field descriptor used by 'EZData' to declare
  typed attributes with default values. The canonical spelling is
  'EZField[T](*args, **kwargs)', where the subscript sets the
  field type via '__class_getitem__' and the call binds the
  construction arguments. Default values are recipes, not cached
  objects: 'field.defaultValue' constructs a fresh
  'fieldType(*posArgs, **keyArgs)' on every read, so mutable
  defaults are not shared between EZData instances.

  Attributes
  ----------
  fieldOwner : type
    The EZData subclass this field is bound to. Set by
    'EZMeta.__init__' after class creation.
  fieldName : str
    The attribute name this field is bound to on its owner.
    Set by 'EZSpace.registerEZField' at class-body assignment.
  fieldType : type[T]
    The declared type of the values this field holds.
  posArgs : tuple
    The positional arguments used when materializing a default.
  keyArgs : dict
    The keyword arguments used when materializing a default.
  defaultValue : T
    A fresh default value computed as
    'fieldType(*posArgs, **keyArgs)'. Re-evaluated on every
    read so mutable defaults are not shared between instances.

  Construction shapes accepted:

  - 'EZField[T](value)' : type 'T', default 'T(value)'.
  - 'EZField[T]()' : type 'T', default 'T()'.
  - 'EZField[T](*args, **kwargs)' : type 'T', default
    'T(*args, **kwargs)'.
  - 'EZField.fromValue(v)' : type 'type(v)', default 'type(v)(v)'.
    Used internally by 'EZHook' to wrap bare class-body values.

  Shapes rejected at class-body time with 'IncompleteFieldException':

  - 'EZField(value)' (no type subscript)
  - 'EZField[T]' (no trailing parens)

  Examples
  --------
      class Point2D(EZData):
        x = EZField[float](0.0)
        y = EZField[float](0.0)

      class Bag(EZData):
        items = EZField[list]()        # default to a fresh []
        labels = EZField[dict]()       # default to a fresh {}

      class Person(EZData):
        name = EZField[FullName]('Doe', givenName='John')
  """

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
    Return the EZData subclass this field is bound to. Set by
    'EZMeta.__init__' after class construction.

    Returns
    -------
    type
      The EZData subclass that owns this field.

    Raises
    ------
    MissingVariable
      If the field has not yet been bound to a class.
    TypeException
      If '__field_owner__' was set to a non-type value.
    """
    if self.__field_owner__ is None:
      raise MissingVariable(self, '__field_owner__', type)
    if isinstance(self.__field_owner__, type):
      return self.__field_owner__
    raise TypeException('__field_owner__', self.__field_owner__, type)

  @fieldName.GET
  def _getFieldName(self, ) -> str:
    """
    Return the attribute name this field is bound to on its
    owner class. Set by 'EZSpace.registerEZField' at class-body
    assignment time.

    Returns
    -------
    str
      The attribute name.

    Raises
    ------
    MissingVariable
      If the field has not yet been registered.
    TypeException
      If '__field_name__' was set to a non-string value.
    """
    if self.__field_name__ is None:
      raise MissingVariable(self, '__field_name__', str)
    if isinstance(self.__field_name__, str):
      return self.__field_name__
    raise TypeException('__field_name__', self.__field_name__, str)

  @fieldType.GET
  def _getFieldType(self, ) -> Type[T]:
    """
    Return the declared type of this field's values. Set by
    'EZField.__class_getitem__' for the 'EZField[T]' form and by
    'EZField.fromValue' for the bare-value path.

    Returns
    -------
    type[T]
      The declared field type.

    Raises
    ------
    MissingVariable
      If no type-setting construction path has been taken.
    TypeException
      If '__field_type__' was set to a non-type value.
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
    Return the positional arguments stored at construction time.
    Used by 'defaultValue' to materialize a fresh default
    instance per call.

    Returns
    -------
    tuple
      The stored positional arguments.

    Raises
    ------
    MissingVariable
      If the field was created without a call (the 'EZField[T]'
      shape with no trailing parentheses).
    TypeException
      If '__pos_args__' was set to a non-tuple value.
    """
    if self.__pos_args__ is None:
      raise MissingVariable(self, '__pos_args__', tuple)
    if isinstance(self.__pos_args__, tuple):
      return self.__pos_args__
    raise TypeException('__pos_args__', self.__pos_args__, tuple)

  @keyArgs.GET
  def _getKeyArgs(self, ) -> dict:
    """
    Return the keyword arguments stored at construction time,
    paired with 'posArgs' to build the default value.

    Returns
    -------
    dict
      The stored keyword arguments.

    Raises
    ------
    MissingVariable
      If the field was created without a call.
    TypeException
      If '__key_args__' was set to a non-dict value.
    """
    if self.__key_args__ is None:
      raise MissingVariable(self, '__key_args__', dict)
    if isinstance(self.__key_args__, dict):
      return self.__key_args__
    raise TypeException('__key_args__', self.__key_args__, dict)

  @defaultValue.GET
  def _getDefaultValue(self, ) -> T:
    """
    Construct and return a fresh default value by invoking the
    field type with the stored positional and keyword arguments.
    Each call builds a new top-level object, so two instances do
    not share the same mutable container ('list', 'dict', 'set',
    ...). This is a shallow construction, though: a mutable object
    nested inside the stored arguments is shared across instances,
    so mutating that nested object leaks between them.

    Returns
    -------
    T
      A fresh default value for the field.

    Raises
    ------
    MissingVariable
      If the field is missing its type or its construction
      arguments. The Field getters consulted here surface those
      conditions as 'MissingVariable'.
    """
    return self.fieldType(*self.posArgs, **self.keyArgs)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, *args, **kwargs) -> None:
    """
    Store the positional and keyword arguments that will later be
    used to build the field's default value via 'fieldType(*args,
    **kwargs)'. The field type itself is set separately, either
    by '__class_getitem__' (for the 'EZField[T](...)' shape) or
    by 'fromValue' (for the bare-value class-body shape).

    Parameters
    ----------
    *args
      Positional arguments to be forwarded to the field type
      constructor when materializing the default.
    **kwargs
      Keyword arguments to be forwarded to the field type
      constructor when materializing the default.
    """
    self.__pos_args__ = args
    self.__key_args__ = kwargs

  @classmethod
  def __class_getitem__(cls, type_: Type[T]) -> EZField:
    """
    Implements the 'EZField[T]' subscript syntax. Returns a fresh
    EZField with its field type set to 'type_' and its
    construction arguments unset. Callable next to bind the
    construction arguments, as in 'EZField[float](0.0)'.

    Parameters
    ----------
    type_ : type[T]
      The declared type of values held by this field.

    Returns
    -------
    EZField
      A new EZField carrying 'type_' as its field type. The
      returned instance must subsequently be called to bind
      construction arguments before it is used as a class-body
      field; otherwise 'EZSpace.registerEZField' raises
      'IncompleteFieldException' at class-body time.
    """
    self = cls.__new__(cls)
    setattr(self, '__field_type__', type_)
    return self

  def __call__(self, *args, **kwargs) -> Self:
    """
    Bind the construction arguments used to build the field's
    default value. Calling on an already-bound EZField replaces
    its stored arguments.

    Parameters
    ----------
    *args
      New positional arguments for the default-value recipe.
    **kwargs
      New keyword arguments for the default-value recipe.

    Returns
    -------
    Self
      'self', so the canonical 'EZField[T](*args, **kwargs)'
      shape evaluates to a single fully-formed EZField.
    """
    self.__pos_args__ = args
    self.__key_args__ = kwargs
    return self

  @classmethod
  def fromValue(cls, value: Any) -> Self:
    """
    Build an EZField from a bare class-body value, inferring the
    field type from 'type(value)' and using the value itself as
    the single positional construction argument. The bare-value
    path in 'EZHook.setItemPhase' takes this route to wrap
    expressions like 'name = "Anonymous"' inside the class body.

    Parameters
    ----------
    value : Any
      The seed value. Its type becomes the field type; the value
      itself becomes the default.

    Returns
    -------
    EZField
      A new EZField carrying 'type(value)' as its field type and
      '(value,)' as its positional arguments.
    """
    self = cls(value)
    setattr(self, '__field_type__', type(value))
    return self

  @classmethod
  def clone_(cls, self: Self) -> EZField[T]:
    """
    Build an independent EZField that mirrors the given one. The
    new field shares the same field type and the same
    construction arguments, but has its own '__field_name__' and
    '__field_owner__' slots (left unset and bound by the new
    owner class when registration runs). Used by
    'EZSpace.registerBaseField' to copy inherited fields into a
    subclass namespace without mutating the parent's field
    objects.

    Parameters
    ----------
    self : EZField
      The field to clone.

    Returns
    -------
    EZField
      A fresh EZField configured identically to 'self' for
      construction purposes.
    """
    other: EZField[T] = cls(*self.posArgs, **self.keyArgs)
    setattr(other, '__field_type__', self.fieldType)
    return other

  def clone(self, ) -> EZField[T]:
    """Instance-shaped alias for 'clone_(self)'."""
    return self.clone_(self)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  if TYPE_CHECKING:  # pragma: no cover
    # @formatter:off
    from typing import overload
    @overload
    def __get__(self, instance: None, owner: type) -> Self: ...
    @overload
    def __get__(self, instance: Any, owner: type) -> T: ...
    def __get__(self, instance: Any, owner: type) -> Union[Self, T]: ...
    # @formatter:on

  def __str__(self) -> str:
    """
    Render the field as 'Owner.name: type(args)', using fallback
    placeholders when the field has not yet been bound to a
    class. Unbound fields show 'EZField.<unbound>: object()' and
    do not raise, matching the defensive behavior of '__repr__'.

    Returns
    -------
    str
      A human-readable rendering of the field.
    """
    infoSpec = """%s.%s: %s(%s)"""
    ownerName = maybe(self.__field_owner__, type(self)).__name__
    fieldName = maybe(self.__field_name__, '<unbound>')
    fieldType = maybe(self.__field_type__, object).__name__
    posArgs = maybe(self.__pos_args__, ())
    posStr = ', '.join(repr(a) for a in posArgs)
    keyArgs = maybe(self.__key_args__, {})
    keyStr = ', '.join(f"{k}={v!r}" for k, v in keyArgs.items())
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
    Render the field as 'EZField[type](args)', the canonical
    construction expression that would reproduce it. Uses
    fallback placeholders so unbound fields still render rather
    than raising 'MissingVariable'.

    Returns
    -------
    str
      A round-trippable construction expression for the field.
    """
    infoSpec = """%s[%s](%s)"""
    clsName = type(self).__name__
    typeStr = maybe(self.__field_type__, object).__name__
    posArgs = maybe(self.__pos_args__, ())
    posStr = ', '.join(repr(a) for a in posArgs)
    keyArgs = maybe(self.__key_args__, {})
    keyStr = ', '.join(f"{k}={v!r}" for k, v in keyArgs.items())
    if posArgs and keyArgs:
      argStr = str.join(', ', (posStr, keyStr))
    elif posArgs:
      argStr = posStr
    elif keyArgs:
      argStr = keyStr
    else:
      argStr = ''
    return infoSpec % (clsName, typeStr, argStr)

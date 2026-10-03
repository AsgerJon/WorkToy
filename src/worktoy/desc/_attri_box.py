"""
AttriBox is a lazily built, strongly typed attribute descriptor.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from copy import deepcopy
from enum import Enum
from typing import TYPE_CHECKING, TypeVar

from . import _RootAlias, Field, BaseDescriptor
from ..core import Object
from ..core.sentinels import DELETED
from ..utilities import typeCast, castRule, textFmt
from ..waitaminute import TypeException, MissingVariable
from ..waitaminute.dispatch import TypeCastException

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Self, Union, Optional, TypeAlias, Never

  FieldType: TypeAlias = Union[type, TypeVar]

T = TypeVar('T')

#  The builtin containers take one iterable rather than their elements as
#  separate arguments. Text is refused for them rather than iterated, since
#  a 'str' would split into characters and 'bytes' into integers. A field
#  of one of the text types takes a single value through 'resolveText'.
_CONTAINERS = (list, tuple, set, frozenset, dict)
_TEXT_TYPES = (str, bytes, bytearray)
#  The number types, whose constructors round: 'int(2.5)' is '2' and
#  'bool(2)' is 'True'. A field of one of them, or of a subclass keeping its
#  constructor, takes a single value through 'resolveNumber'.
_NUMBER_TYPES = (bool, int, float, complex)


class AttriBox(BaseDescriptor[T]):
  """
  AttriBox is a lazily built, strongly typed attribute descriptor.
  Declare it as 'x = AttriBox[T](*args, **kwargs)': the subscript fixes
  the field type 'T', and the call captures the deferred default. The
  field is built by calling 'T(*args, **kwargs)' the first time it is
  read on an instance, then cached on that instance.

  Sentinels in the deferred default
  ---------------------------------
  The captured arguments may include the contextual sentinels, which
  are substituted when the field is built, using the active '__get__':

  - THIS  -> the instance the attribute is read from.
  - OWNER -> the owner class the attribute is read through.
  - DESC  -> this 'AttriBox' descriptor itself.

  So 'AttriBox[Foo](THIS)' builds a separate 'Foo(instance)' for each
  instance, and 'AttriBox[Foo](OWNER)' builds 'Foo(owner)'. A sentinel
  with no active context (no instance or owner available) is passed
  through unchanged.

  Get and set contract
  --------------------
  Reading the field returns the stored 'T' instance, building the
  deferred default on first read. Reading a deleted field raises
  'MissingVariable'. The field always holds an instance of 'T', though
  not necessarily of exactly 'T': a 'bool' assigned to an
  'AttriBox[int]' stays a 'bool'. A field type whose constructor returns
  something other than an instance of it is refused with
  'TypeException'. Assigning a value:

  - a value already of type 'T' is stored unchanged;
  - if 'T' is a text type, 'str', 'bytes' or 'bytearray', or based on
    one, the value goes to 'resolveText', which defers to 'typeCast':
    text converts between the three as UTF-8, and anything else raises
    'TypeException', since the constructors of the text types accept
    almost anything ('str(None)' is 'None', 'bytes(5)' five zero
    bytes). A single default argument takes the same route;
  - otherwise a lossless 'typeCast(T, value)' is tried with no
    construction; on success the cast result is stored;
  - if 'T' is 'bool', 'int', 'float', or 'complex', or a subclass of
    one that keeps its constructor, the cast is
    authoritative: a refused value raises (the chained
    'OverflowError' when an int is too large for the float,
    otherwise 'TypeException') instead of being forced through
    'T(value)', which would silently round. A single default
    argument, and an assigned tuple of one value, go to
    'resolveNumber', which defers to the same cast. Stupid args,
    stupid prizes;
  - for any other 'T', a failed cast falls back to the field-type
    constructor ('T(value)', or 'T(*value)' when 'value' is a
    tuple; see '_resolve' for the splat rules);
  - a builtin container field type ('list', 'tuple', 'set', 'frozenset'
    or 'dict') refuses a 'str', 'bytes' or 'bytearray' with
    'TypeException' rather than splitting it into characters or
    integers, for the deferred default as for an assignment;
  - if construction also fails, 'TypeException' is raised, chained
    from the cast failure.

  A field type based on a builtin follows 'castRule', as 'typeCast' and
  the overload dispatch do. A subclass that keeps the constructor of its
  builtin is held to the rule of that builtin, and the field holds an
  instance of the subclass built from the cast value. A subclass with a
  constructor of its own, such as an 'IntEnum', is trusted: its
  constructor decides.

  Notes
  -----
  A sentinel captured in the deferred default is rebuilt through the
  field type even when the owning instance is already an instance of
  that type. The convenience case is 'AttriBox[Foo](someFoo)', where a
  lone argument that is already a 'Foo' is deep-copied for each instance
  instead of being rebuilt, so 'AttriBox[list]([1, 2, 3])' gives every
  instance its own list rather than one shared default. A value that
  refuses to be copied is stored unchanged rather than raising. That
  copy is suppressed whenever the captured arguments contain 'THIS',
  'OWNER', or 'DESC', because such an argument becomes an instance of
  the field type only by the accident of the surrounding class
  hierarchy.

  The case to watch is a field type that is also a base of its owner:

    class Parent: ...

    class Child(Parent):
      mom = AttriBox[Parent](THIS)

  Reading 'child.mom' builds 'Parent(child)', not 'child' itself, even
  though 'isinstance(child, Parent)' holds. The corollary is that the
  field type must accept whatever 'THIS' resolves to. A 'Parent' with no
  constructor taking an argument raises 'TypeException' here, chained
  from the 'TypeError' that 'object.__init__' raises, rather than
  silently handing back the owner.

  Each instance stores the value of a field under the private name that
  'Object.getPrivateName' derives from the field name, followed by the
  lower-case name of the box class and '_field_object__', so an
  'AttriBox' named 'fooBar' stores at
  '__foo_bar__attribox_field_object__'. The double underscore inside
  keeps the storage apart from dunders Python uses and from private
  class attributes such as '__foo_bar__'. Names that differ only in how
  their words are joined or capitalised derive the same private name,
  though: 'fooBar' and 'foo_bar' both store at
  '__foo_bar__attribox_field_object__', as do 'X' and 'x' at
  '__x__attribox_field_object__'. Declaring two such fields on one
  class, the same name once in each spelling, leaves them sharing one
  storage, and the behaviour is then undefined.

  An object the box creates, as a default or through the field-type
  constructor on assignment, is tagged with '__field_box__',
  '__field_name__' and '__field_owner__', naming the box that created it.
  An object assigned already of the field type is not. '_applyTags'
  lists the objects left untagged, and a class keeps its instances
  untagged by declaring '__no_box_tag__' as true. A box is its own copy,
  shallow and deep, so a copy of a tagged object, or of the instance
  owning the field, names the same box; see '__deepcopy__'.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private Variables
  __field_type__: Optional[type] = None

  #  Public Variables
  fieldType: Field[type] = Field()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @fieldType.GET
  def getFieldType(self) -> type:
    if self.__field_type__ is None:
      raise MissingVariable(self, '__field_type__', type)
    return self.__field_type__

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _getStorageName(self) -> str:
    """
    The '_getStorageName' method returns the name under which each
    instance stores the value of this field: the private name from
    'getPrivateName', followed by the lower-case name of the box class
    and '_field_object__'. An 'AttriBox' named 'fooBar' stores at
    '__foo_bar__attribox_field_object__' and a 'FixBox' of that name at
    '__foo_bar__fixbox_field_object__', so anyone who meets the name
    can tell what put it there. The double underscore inside sets the
    name apart from every name written in the '__snake_case__' style, so
    the stored value never lands on a dunder Python uses, on the state
    'Object' keeps, or on a private class attribute of the owner, such
    as the '__foo_bar__' of the 'Field' pattern.
    """
    boxName = type(self).__name__.lower()
    return '%s%s_field_object__' % (self.getPrivateName(), boxName)

  def _resolve(self, *args, **kwargs) -> T:
    """
    The '_resolve' method builds a new instance of the field type from
    the given arguments. It does *not* retrieve arguments from 'self',
    but requires them to be passed in, because it is used both when
    setting and getting.

    For a text field type, 'str', 'bytes' or 'bytearray', a single
    argument without keywords goes to 'resolveText' rather than to the
    constructor, and for a number field type, 'bool', 'int', 'float' or
    'complex', to 'resolveNumber'; see there. The rules below apply to
    every other build.

    A lone argument that is already an instance of the field type is
    deep-copied rather than rebuilt, so each instance owns its default
    instead of sharing the single object captured in the class body. A
    value that refuses to be copied is stored unchanged rather than
    raising, since receiving a value of the exact field type must never
    error. This copy is suppressed when the box captured a contextual
    sentinel, since a value that became a field-type instance only
    because 'THIS' resolved to the owner must still go through the
    constructor. So 'AttriBox[Parent](THIS)' read on a 'Child' instance
    builds 'Parent(child)' instead of copying 'child' itself just
    because it happens to be a 'Parent'. The copy likewise yields to
    normal construction when keyword arguments are present, since
    copying the lone argument would silently discard them.

    When '__instance_get__' is unable to retrieve a value from a given
    instance, the 'args' and 'kw' passed to the constructor of the
    'AttriBox' are retrieved from the 'getPosArgs' and 'getKeyArgs'
    methods, and passed to this method.

    The '__instance_set__' method will always receive one object. However,
    if this object is a 'tuple', the intention may be that these should be
    understood as starred arguments. For example:

    class Foo:
      bar = AttriBox[complex](0)

      def __getitem__(self, index: Any) -> Any: ...

    foo = Foo()
    foo.bar = 69, 420

    foo.bar = 69, 420
    #  The descriptor protocol processes the above assignment as:
    AttriBox.__set__(Foo.bar, foo, (69, 420))
    #  Similarly to how:
    foo[69, 420]
    #  is processed as:
    Foo.__getitem__(foo, (69, 420))
    In the above examples, it is *not* possible to pass keyword arguments.
    This is the only difference between function calls and the above. For
    this reason, a received 'tuple' object implies a sequence of
    positional arguments. When passing such on to the field type
    constructor, it is reasonable to infer that a star (*) were
    intended. With a few exceptions, described below. Please note,
    that 'args' in any 'function' object with starred arguments,
    is a 'tuple' of the passed arguments. The tuple spoken off here,
    is when the 'args' object consists only of one 'tuple' object.

    The exceptions referenced above all have to do with builtin collection
    types. These demand receiving a tuple as a single argument, rather
    than an arbitrary number of arguments. For example, the following is
    not valid:
    sus = list(1, 2, 3)
    but the following is:
    meh = list((1, 2, 3))  # no star
    The above is true for: tuple, list, set and frozenset. For dict,
    each element of the tuple must itself be a tuple of length 2, with the
    first element being hashable. For 'set' and 'frozenset', every element
    must be hashable. The final exception is that in the presence of
    keyword arguments, the 'tuple' is not unpacked. A single argument
    for a container is converted as a whole, so 'AttriBox[list](range(3))'
    holds '[0, 1, 2]', except that a 'str', 'bytes' or 'bytearray' is
    refused rather than split into characters or integers.

    Why a tuple splats, and why the builtins are exempt
    ---------------------------------------------------
    Two constructor conventions exist and cannot be told apart from
    the field type alone. Value constructors take their components as
    separate positional arguments, as in 'complex(re, im)' or any
    'Foo(x, y)'. Container constructors take a single iterable, as in
    'list(items)'. Most user types follow the first convention, so a
    received 'tuple' is splatted by default to make 'self.bar = 69,
    420' mirror 'AttriBox[Foo](69, 420)'. The four builtin containers
    and 'dict' follow the second convention and reject splatting, so
    they are hardcoded as the known exceptions. There is no general
    way to detect a user type that follows the second convention, so
    such a type is not granted the same courtesy.

    The corollary is the practical escape hatch: the splat fires on
    'tuple' specifically, not on every iterable. A field type whose
    constructor wants a single iterable should therefore be fed a
    'list', and declaring the field type accordingly documents the
    intent at the call site:

      class Karen:
        def __init__(self, pedantry: list[str]) -> None: ...

      class Owner:
        karen = AttriBox[Karen](['why', 'are', 'you', 'like'])

    The list default builds 'Karen([...])' and 'owner.karen = [...]'
    rebuilds it the same way, because a 'list' is never splatted.
    Only forcing a 'tuple' onto such a type re-triggers the splat.

    One asymmetry survives and is worth stating outright: the
    deferred default and the runtime setter do not treat a 'tuple'
    alike. The arguments captured by 'AttriBox[T](...)' are already
    the positional argument list and are never splatted, whereas a
    'tuple' arriving through '__instance_set__' is. So
    'AttriBox[T]((a, b))' builds 'T((a, b))', but
    'instance.attr = (a, b)' builds 'T(a, b)'. Same value, different
    path, different result. Feeding a 'list' avoids the divergence.

    Parameters
    ----------
    *args : Any
        Positional arguments forwarded to the field-type constructor,
        splatted from a received 'tuple' under the rules above.
    **kwargs : Any
        Keyword arguments forwarded to the field-type constructor.

    Returns
    -------
    T
        The field-type instance, tagged by '_applyTags' with this box,
        its field name and its owner when this box created it.

    Raises
    ------
    TypeException
        If neither the cast nor the field-type constructor accepts the
        arguments, or if the constructor returns something that is not
        an instance of the field type.
    """
    fieldType = self.getFieldType()
    #  A flag rather than 'None' marks a value not built yet, since 'None'
    #  is the very value 'AttriBox[object](None)' copies.
    copied = False
    if not self.hasSentinelArgs() and len(args) == 1 and not kwargs:
      if isinstance(args[0], fieldType):
        copied = True
        #  A lone argument already of the field type is deep-copied so
        #  that each instance owns its default rather than sharing the
        #  single object captured in the class body. Atomic immutables
        #  ('int', 'float', 'str', ...) deep-copy to themselves, so the
        #  common scalar default costs nothing. A value that refuses to
        #  be copied is stored as-is rather than raising: receiving a
        #  value of the exact field type must never error, and an
        #  un-copyable value can only be shared or rejected.
        try:
          fieldObject = deepcopy(args[0])
        except Exception:  # un-copyable: share rather than raise
          fieldObject = args[0]
    if not copied:
      if self._isTextField() and len(args) == 1 and not kwargs:
        fieldObject = self.resolveText(args[0])
      elif self._isLoneNumber(args, kwargs):
        fieldObject = self.resolveNumber(args[0])
      else:
        fieldObject = self._callFieldType(*args, **kwargs)
      if not isinstance(fieldObject, fieldType):
        #  A constructor may return anything at all. Storing what it
        #  returned would break the rule that the field always holds an
        #  instance of its field type.
        raise TypeException(self.getFieldName(), fieldObject, fieldType)
    self._applyTags(fieldObject, *args)
    return fieldObject

  def _isTextField(self) -> bool:
    """
    The '_isTextField' method reports whether the field type is one of
    the text types, 'str', 'bytes' or 'bytearray', or a subclass of one.
    Their constructors accept almost anything, so a single value for such
    a field goes through 'resolveText' instead.
    """
    fieldType = self.getFieldType()
    return True if issubclass(fieldType, _TEXT_TYPES) else False

  def _isNumberField(self) -> bool:
    """
    The '_isNumberField' method reports whether the field type is one of
    the number types, 'bool', 'int', 'float' or 'complex', or a subclass
    keeping the constructor of one, by 'castRule'. Their constructors
    round, so a single value for such a field goes through
    'resolveNumber' instead.
    """
    return True if castRule(self.getFieldType()) in _NUMBER_TYPES else False

  def _isLoneNumber(self, args: tuple, kwargs: dict) -> bool:
    """
    The '_isLoneNumber' method reports whether a build from the given
    arguments is a single value for a number field: one positional
    argument, no keyword, and no contextual sentinel among the captured
    arguments, since a sentinel is rebuilt through the constructor
    whatever it resolved to, as the class docstring says.
    """
    if len(args) != 1 or kwargs or self.hasSentinelArgs():
      return False
    return self._isNumberField()

  def resolveNumber(self, value: Any) -> Any:
    """
    The 'resolveNumber' method turns a single value into the value of a
    number field, one whose field type is 'bool', 'int', 'float' or
    'complex', or a subclass keeping the constructor of one. It defers to
    'typeCast', which converts a number or a numeric string without loss
    and refuses anything else, rather than calling the field type, whose
    constructor rounds: 'int(2.5)' is '2', and 'bool(2)' is 'True'. An
    'int' too large for a 'float' raises the 'OverflowError' of the cast,
    as an assignment does.

    A default given as a single argument without keywords comes here, and
    so does an assigned tuple of one value, as in 'foo.n = (2.5,)', which
    the cast of '__instance_set__' leaves to the build. Several
    arguments, as in 'AttriBox[int]('ff', 16)', and keyword arguments
    still go to the constructor, and so does a contextual sentinel.

    The method exists to be replaced, as 'resolveText' does. A subclass
    of 'AttriBox' that wants its number fields rounded, or converted some
    other way, replaces it, and every number field of that box class
    follows. What it returns must still be an instance of the field type,
    or the box raises 'TypeException'.

    Parameters
    ----------
    value : Any
      The single value to turn into the value of the field.

    Returns
    -------
    Any
      An instance of the field type.

    Raises
    ------
    TypeException
      If 'typeCast' refuses the value, chained from the
      'TypeCastException' it raised.
    OverflowError
      If the value is an 'int' too large for a 'float' field.
    """
    fieldType = self.getFieldType()
    try:
      return typeCast(fieldType, value)
    except TypeCastException as typeCastException:
      cause = typeCastException.__cause__
      if isinstance(cause, OverflowError):
        raise cause
      fieldName = self.getFieldName()
      raise TypeException(fieldName, value, fieldType) from typeCastException

  def resolveText(self, value: Any) -> Any:
    """
    The 'resolveText' method turns a single value into the value of a
    text field, one whose field type is 'str', 'bytes' or 'bytearray'. It
    defers to 'typeCast', which converts between the three text types as
    UTF-8 and refuses anything else, rather than calling the field type,
    whose constructor accepts almost anything: 'str(None)' is 'None', and
    'bytes(5)' is five zero bytes.

    A value assigned to a text field comes here unless it is already of
    the field type, and so does a default given as a single argument
    without keywords. Several arguments, as in 'AttriBox[str](b'ab',
    'latin-1')', still go to the constructor.

    The method exists to be replaced. A subclass of 'AttriBox' that wants
    its text fields more lenient, stricter, or converted some other way
    altogether replaces it, and every text field of that box class
    follows. What it returns must still be an instance of the field type,
    or the box raises 'TypeException'.

    Parameters
    ----------
    value : Any
      The single value to turn into the value of the field.

    Returns
    -------
    Any
      An instance of the field type.

    Raises
    ------
    TypeException
      If 'typeCast' refuses the value, chained from the
      'TypeCastException' it raised.
    """
    fieldType = self.getFieldType()
    try:
      return typeCast(fieldType, value)
    except TypeCastException as typeCastException:
      fieldName = self.getFieldName()
      raise TypeException(fieldName, value, fieldType) from typeCastException

  def _callFieldType(self, *args, **kwargs) -> Any:
    """
    The '_callFieldType' method builds a value by calling the field type
    with the given arguments, under the rules '_resolve' describes for
    the builtin containers: a single argument is converted as a whole,
    several arguments become the elements, and text is refused rather
    than split.
    """
    fieldType = self.getFieldType()
    container = True if fieldType in _CONTAINERS and not kwargs else False
    single = True if len(args) == 1 else False
    if container and single and isinstance(args[0], _TEXT_TYPES):
      raise TypeException('value', args[0], fieldType)
    try:
      if container and single:
        return fieldType(args[0])
      if container:
        return fieldType(args)
      return fieldType(*args, **kwargs)
    except (TypeError, ValueError) as exception:
      name = 'value'
      badValue = args[0] if args else None
      raise TypeException(name, badValue, fieldType) from exception

  def _assignedArgs(self, value: Any) -> tuple:
    """
    The '_assignedArgs' method turns an assigned value into the arguments
    '_resolve' builds from, substituting the contextual sentinels. An
    assigned 'tuple' is the argument list, as '_resolve' explains, except
    for a container field type, which takes the tuple whole as its one
    iterable.
    """
    if isinstance(value, tuple):
      args = (*(self.filterSentinels(arg) for arg in value),)
      if self.getFieldType() in _CONTAINERS:
        return (args,)
      return args
    return (self.filterSentinels(value),)

  def _applyTags(self, fieldObject: Any, *args) -> None:
    """
    The '_applyTags' method writes three tags onto an object this box
    created, so the object can find the box that made it:
    '__field_name__', '__field_owner__' and '__field_box__'. The tags name
    the box that created the object, not a box that holds it: an object
    assigned to the field already of the field type is stored as it is,
    and keeps whatever tags it has. The tags are written with
    'object.__setattr__', past any '__setattr__' of the object's class, so
    a frozen or otherwise guarded object is tagged like any other.

    The objects this box did not create, or cannot tag, are left as they
    are:

    - one of 'args', the arguments the object was built from, handed back
      as it was, such as a default that refuses to be copied or copies to
      itself;
    - a class, whose tags would become class attributes read by all its
      instances and subclasses;
    - an instance of a class declaring '__no_box_tag__' as true, which
      is how the enumeration members of 'KeeNum' and 'KeeFlags' opt out,
      and how any other class may;
    - a member of an 'Enum', a shared singleton of the standard library;
    - an object without an instance dict, such as an instance of a class
      with '__slots__' only, or of a builtin such as 'int'.
    """
    if any(fieldObject is arg for arg in args):
      return
    if isinstance(fieldObject, type):
      return
    if getattr(type(fieldObject), '__no_box_tag__', False):
      return
    if isinstance(fieldObject, Enum):
      return
    try:
      object.__getattribute__(fieldObject, '__dict__')
    except AttributeError:
      return
    object.__setattr__(fieldObject, '__field_name__', self.getFieldName())
    object.__setattr__(fieldObject, '__field_owner__', self.getFieldOwner())
    object.__setattr__(fieldObject, '__field_box__', self)

  def __instance_get__(self, instance: Any, owner: type, **kwargs) -> T:
    """
    The '__instance_get__' method returns the stored field value for the
    given instance, building the deferred default with a fresh
    field-type instance on the first read and caching it under the
    private name. A read passing '_deleting=True', which 'Object.__delete__'
    makes to report the old value, answers from the storage alone and
    raises 'AttributeError' for an unset field instead of building.
    """
    pvtName = self._getStorageName()
    try:
      #  Not 'getattr', whose miss an owner's '__getattr__' could answer.
      value = object.__getattribute__(instance, pvtName)
    except AttributeError as attributeError:
      if kwargs.get('_deleting', False):
        raise attributeError
      if kwargs.get('_recursion', False):
        raise RecursionError from attributeError
      args = self.getPosArgs()
      kwargs = self.getKeyArgs()
      fieldObject = self._resolve(*args, **kwargs)
      #  Not 'setattr', which an owner's '__setattr__' could refuse.
      object.__setattr__(instance, pvtName, fieldObject)
      return self.__instance_get__(instance, owner, _recursion=True)
    else:
      return value

  def __instance_set__(self, instance: Any, value: Any, **kwargs) -> T:
    """
    The '__instance_set__' method stores 'value' for the given instance.
    A value already of the field type is stored unchanged; otherwise a
    lossless 'typeCast' is tried, and only failing that does the field
    type constructor run. See the class docstring for the full coercion
    contract. It returns the value stored, which the 'onSet' callbacks
    receive.
    """
    fieldType = self.getFieldType()
    pvtName = self._getStorageName()
    if isinstance(value, fieldType):
      object.__setattr__(instance, pvtName, value)
      return value
    #  Catch recursion
    if kwargs.get('_recursion', False):
      raise RecursionError
    if self._isTextField():
      #  Text skips the cast below, so that 'resolveText' alone decides.
      fieldObject = self._resolve(*self._assignedArgs(value), **kwargs)
      return self.__instance_set__(instance, fieldObject, _recursion=True)
    #  Attempt to 'typeCast' without instantiation
    try:
      cast = typeCast(fieldType, value, allowInstantiation=False)
    except TypeCastException as typeCastExc:
      cause = typeCastExc.__cause__
      if isinstance(cause, OverflowError):
        raise cause
      if self._isNumberField():
        if not isinstance(value, tuple):
          raise TypeException('value', value, fieldType) from typeCastExc
      try:
        fieldObject = self._resolve(*self._assignedArgs(value), **kwargs)
      except Exception as exception:
        raise exception from typeCastExc
      else:
        return self.__instance_set__(instance, fieldObject, _recursion=True)
    else:
      return self.__instance_set__(instance, cast, _recursion=True)

  def __instance_delete__(self, instance: Any, *_, **kwargs) -> None:
    """
    The '__instance_delete__' method deletes the field for the given
    instance by storing the 'DELETED' sentinel under the private
    attribute name, which a later read translates into 'MissingVariable'.
    """
    pvtName = self._getStorageName()
    object.__setattr__(instance, pvtName, DELETED)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __get__(self, instance: Any, owner: type) -> Any:
    """
    The '__get__' method confirms that a field type was captured before
    handing the access to the 'Object' descriptor protocol.

    The class-body route is already closed by '__set_name__', so a box
    that reaches here without a field type was installed on a finished
    class by 'setattr', where no name was ever assigned and no hook ever
    ran. Failing here names the descriptor at the access itself, rather
    than several frames deeper once '_resolve' asks for the field type
    and 'getFieldType' raises the identical exception from there.

    Class-level access is unaffected: a box read through its owning class
    still returns the descriptor, so it stays available for
    introspection.
    """
    if instance is not None:
      if self.__field_type__ is None:
        raise MissingVariable(self, '__field_type__', type)
    return super().__get__(instance, owner)

  def __copy__(self) -> Self:
    """
    The '__copy__' method returns the box itself, so 'copy.copy' of a box
    is the box. See '__deepcopy__' for the reason, which applies to both.
    """
    return self

  def __deepcopy__(self, memo: dict) -> Self:
    """
    The '__deepcopy__' method returns the box itself, so 'copy.deepcopy'
    of a box is the box, whether the box is copied directly or reached
    while copying another object. It replaces the copying 'NoPickle'
    provides, which would build a new box holding deep copies of every
    attribute, the captured default arguments included.

    A box is part of the class it is declared on, as a method or a
    property is, and is shared by every instance of that class. A copy of
    it would be a descriptor installed on no class. Copying reaches a box
    mostly through the tags of '_applyTags': an object this box created
    refers to it through '__field_box__', so a deep copy of that object,
    or of an object holding it, such as the instance owning the field,
    reaches the box through the tag. Returning the box itself keeps the
    '__field_box__' of the copy naming the box declared on the class, as
    the original does, and leaves the captured default arguments of the
    box uncopied. The copy of the object itself is made as before.

    'FixBox', 'Kee' and 'KeeBox' inherit this. A separate box is made by
    subscripting and calling the box class again, and a separate 'Kee'
    with 'Kee.clone'. 'FastBox' creates no tags and keeps the copying of
    'NoPickle'.
    """
    return self

  @classmethod
  def __class_getitem__(cls, fieldType: FieldType) -> Self:
    """
    The '__class_getitem__' method captures the field type from the
    'AttriBox[T]' subscript. A plain class produces a fresh 'AttriBox'
    parametrized with it. Anything else, a 'TypeVar' or a parametrized
    generic such as 'list[int]', is forwarded to the generic machinery,
    and a class body binding the resulting alias raises 'PhantomBoxError'.

    Parameters
    ----------
    fieldType : type or TypeVar
        The field type fixed by the subscript.

    Returns
    -------
    Self
        A new instance of the box class the subscript was written
        against, carrying 'fieldType' and ready for the deferred
        '__call__'. Subclasses such as 'FixBox' and 'Kee' therefore get
        an instance of themselves rather than of 'AttriBox'.

    Raises
    ------
    TypeException
        If 'fieldType' is not a 'type' or 'TypeVar'.

    """
    #  'isinstance(fieldType, type)' reads '__class__', which a builtin
    #  parametrized generic such as 'list[int]' forwards to its origin on
    #  Python 3.9 and 3.10, answering 'True'. The type of the subscript is
    #  a metaclass exactly when the subscript is a plain class, on every
    #  version, without an attribute lookup a class-level hook could answer.
    if issubclass(type(fieldType), type):
      self = object.__new__(cls)
      self.__field_type__ = fieldType
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
    The '__call__' method captures constructor arguments for deferred
    field construction. The 'AttriBox[T](*args, **kw)' idiom is a
    two-step decoration: '__class_getitem__' produces a fresh 'AttriBox'
    parametrized with the field type 'T', and this '__call__' captures
    the positional and keyword arguments forwarded to 'T(...)' when the
    field is first accessed on an instance. The arguments are stashed via
    'Object.__init__' (which routes them through 'getPosArgs' /
    'getKeyArgs'); the field type is not instantiated here.

    A box already placed on a class refuses the call with 'TypeError'.
    Read through its class, as in 'Holder.n', a box gives itself, and the
    call would replace the default of every instance yet to read the
    field.

    Returns
    -------
    Self
        'self', so the call site can chain straight into a class-body
        assignment, for example 'x = AttriBox[int](42)'.
    """
    if self.__field_owner__ is not None:
      infoSpec = """The box at '%s.%s' took the arguments of its default as
      its class was created, and cannot take new ones."""
      ownerName = self.__field_owner__.__name__
      info = infoSpec % (ownerName, self.__field_name__)
      raise TypeError(textFmt(info))
    Object.__init__(self, *args, **kwargs)
    return self

  def __set_name__(self, owner: type, name: str, **kwargs) -> None:
    """
    This implementation settles what an incomplete declaration meant, at
    the moment the class is created.

    Two incomplete spellings reach here, and they are treated
    differently because only one of them leaves anything to work with. A
    box that never captured a field type has nothing to build from, and
    no later chance to learn one, since '__class_getitem__' is the only
    place a field type is ever assigned. That one is refused outright. A
    box whose subscript did name a type, but whose trailing call was
    left off, is missing only the deferred argument list, and an absent
    list reads naturally as an empty one. That one has the capture run
    on its behalf, which leaves it indistinguishable from a box written
    as 'AttriBox[T]()'.

    Refusing at class creation rather than at first read is what
    '_RootAlias.__set_name__' does for the alias case, and for the same
    reason. This is the earliest moment the mistake is unambiguous, and
    the class body is where the offending line actually sits.

    The normalisation has to happen before the inherited implementation
    runs, since that is what records the owner and the name and fires
    'hookSetName'. Skipping the delegation would leave every box without
    a field name, which the private-name lookup needs on the first read.

    Note that Python 3.7 through 3.11 re-raise anything from
    '__set_name__' wrapped in a 'RuntimeError', with the original left
    on '__cause__'. From 3.12 onward it propagates unchanged.
    """
    if self.__field_type__ is None:
      raise MissingVariable(self, '__field_type__', type)
    if self.__pos_args__ is None:
      BaseDescriptor.__init__(self)
    super().__set_name__(owner, name, **kwargs)

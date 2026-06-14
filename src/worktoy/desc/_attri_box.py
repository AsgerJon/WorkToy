"""
AttriBox is a lazily built, strongly typed attribute descriptor.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from copy import deepcopy
from typing import TYPE_CHECKING, TypeVar

from . import Field, BaseDescriptor
from ..core import Object
from ..core.sentinels import DELETED
from ..utilities import textFmt, typeCast
from ..waitaminute import TypeException, MissingVariable
from ..waitaminute.dispatch import TypeCastException

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Self, Union, Optional

T = TypeVar('T')


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
  'MissingVariable'. Assigning a value:

  - a value already of type 'T' is stored unchanged;
  - otherwise a lossless 'typeCast(T, value)' is tried with no
    construction; on success the cast result is stored;
  - if 'T' is 'bool', 'int', 'float', or 'complex', the cast is
    authoritative: a refused non-tuple value raises (the chained
    'OverflowError' when an int is too large for the float,
    otherwise 'TypeException') instead of being forced through
    'T(value)', which would silently round. Stupid args, stupid
    prizes;
  - for any other 'T', a failed cast falls back to the field-type
    constructor ('T(value)', or 'T(*value)' when 'value' is a
    tuple; see '_resolve' for the splat rules);
  - if construction also fails, 'TypeException' is raised, chained
    from the cast failure.

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

  def _resolve(self, *args, **kwargs) -> T:
    """
    The '_resolve' method builds a new instance of the field type from
    the given arguments. It does *not* retrieve arguments from 'self',
    but requires them to be passed in, because it is used both when
    setting and getting.

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
    keyword arguments, the 'tuple' is not unpacked.

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
        The freshly built field-type instance, tagged with its field
        name, owner, and owning box.

    Raises
    ------
    TypeException
        If neither the cast nor the field-type constructor accepts the
        arguments.
    """
    fieldType = self.getFieldType()
    fieldObject = None
    if not self.hasSentinelArgs() and len(args) == 1 and not kwargs:
      if isinstance(args[0], fieldType):
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
    if fieldObject is None:
      try:
        if fieldType in (list, set, frozenset, dict, tuple) and not kwargs:
          fieldObject = fieldType(args)
        else:
          fieldObject = fieldType(*args, **kwargs)
      except (TypeError, ValueError) as exception:
        name = 'value'
        badValue = args[0] if args else None
        raise TypeException(name, badValue, fieldType) from exception
    try:
      setattr(fieldObject, '__field_name__', self.getFieldName())
      setattr(fieldObject, '__field_owner__', self.getFieldOwner())
      setattr(fieldObject, '__field_box__', self)
    except AttributeError:
      pass
    return fieldObject

  def __instance_get__(self, instance: Any, owner: type, **kwargs) -> Any:
    """
    The '__instance_get__' method returns the stored field value for the
    given instance, building the deferred default with a fresh
    field-type instance on the first read and caching it under the
    private name.
    """
    pvtName = self.getPrivateName()
    try:
      value = getattr(instance, pvtName)
    except AttributeError as attributeError:
      if kwargs.get('_recursion', False):
        raise RecursionError from attributeError
      args = self.getPosArgs()
      kwargs = self.getKeyArgs()
      fieldObject = self._resolve(*args, **kwargs)
      setattr(instance, pvtName, fieldObject)
      return self.__instance_get__(instance, owner, _recursion=True)
    else:
      return value

  def __instance_set__(self, instance: Any, value: Any, **kwargs) -> None:
    """
    The '__instance_set__' method stores 'value' for the given instance.
    A value already of the field type is stored unchanged; otherwise a
    lossless 'typeCast' is tried, and only failing that does the field
    type constructor run. See the class docstring for the full coercion
    contract.
    """
    fieldType = self.getFieldType()
    pvtName = self.getPrivateName()
    if isinstance(value, fieldType) or kwargs.get('_root', False):
      return setattr(instance, pvtName, value)
    #  Catch recursion
    if kwargs.get('_recursion', False):
      raise RecursionError
    #  Attempt to 'typeCast' without instantiation
    try:
      cast = typeCast(fieldType, value, allowInstantiation=False)
    except TypeCastException as typeCastException:
      cause = typeCastException.__cause__
      if isinstance(cause, OverflowError):
        raise cause
      if fieldType in (bool, int, float, complex):
        if not isinstance(value, tuple):
          raise TypeException(
            'value', value, fieldType) from typeCastException
      if isinstance(value, tuple):
        args = (*(self.filterSentinels(arg) for arg in value),)
      else:
        args = (self.filterSentinels(value),)
      try:
        fieldObject = self._resolve(*args, **kwargs)
      except Exception as exception:
        raise exception from typeCastException
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
    pvtName = self.getPrivateName()
    setattr(instance, pvtName, DELETED)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def __class_getitem__(cls, fieldType: Union[type, TypeVar]) -> Self:
    """
    The '__class_getitem__' method captures the field type from the
    'AttriBox[T]' subscript. A 'TypeVar' is forwarded to the generic
    machinery; a concrete type produces a fresh 'AttriBox' parametrized
    with it.

    Parameters
    ----------
    fieldType : type or TypeVar
        The field type fixed by the subscript.

    Returns
    -------
    Self
        A new 'AttriBox' carrying 'fieldType', ready for the deferred
        '__call__'.

    Raises
    ------
    ValueError
        If 'fieldType' is 'NoneType', whose field could only ever
        hold 'None' and whose deferred construction would fail on
        the first read.
    """
    if isinstance(fieldType, TypeVar):
      return super().__class_getitem__(fieldType)  # noqa
    if fieldType is type(None):
      infoSpec = """'%s' cannot use 'NoneType' as its field type! A
      field of this type could only ever hold 'None'."""
      raise ValueError(textFmt(infoSpec % cls.__name__))
    self = object.__new__(cls)
    self.__field_type__ = fieldType
    return self  # noqa

  def __call__(self, *args, **kwargs) -> Any:
    """
    The '__call__' method captures constructor arguments for deferred
    field construction. The 'AttriBox[T](*args, **kw)' idiom is a
    two-step decoration: '__class_getitem__' produces a fresh 'AttriBox'
    parametrized with the field type 'T', and this '__call__' captures
    the positional and keyword arguments forwarded to 'T(...)' when the
    field is first accessed on an instance. The arguments are stashed via
    'Object.__init__' (which routes them through 'getPosArgs' /
    'getKeyArgs'); the field type is not instantiated here.

    Returns
    -------
    Any
        'self', so the call site can chain straight into a class-body
        assignment, for example 'x = AttriBox[int](42)'.
    """
    Object.__init__(self, *args, **kwargs)
    return self

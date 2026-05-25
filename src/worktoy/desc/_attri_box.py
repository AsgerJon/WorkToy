"""
AttriBox implements a lazily instantiated and strongly typed descriptor
class.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from . import Field, BaseDescriptor
from ..core import Object
from ..core.sentinels import DELETED
from ..utilities import typeCast
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
  - if the cast fails, the value is passed to the field-type
    constructor ('T(value)', or 'T(*value)' when 'value' is a
    tuple; see '_resolve' for the splat rules);
  - if construction also fails, 'TypeException' is raised, chained
    from the cast failure.
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
    Creates a new instance of the field type from the given arguments.
    Please note, that this method does *not* retrieve arguments from
    'self', but requires them to be passed in as arguments. This is because
    this method is used both when setting and getting.

    When '__instance_get__' is unable to retrieve a value from a given
    instance. The 'args' and 'kw' passed to the constructor of the
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
    """
    fieldType = self.getFieldType()
    fieldObject = None
    if len(args) == 1:
      if isinstance(args[0], fieldType):
        fieldObject = args[0]
    if fieldObject is None:
      try:
        if fieldType in (list, set, frozenset, dict, tuple):
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
    Returns the value of the field for the given instance. If the value is
    not set, it initializes it with a new instance of the field type.
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
    Sets the value of the field for the given instance. If the value is
    not set, it initializes it with a new instance of the field type.
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
    Deletes the value of the field for the given instance by storing
    the 'DELETED' sentinel under the private attribute name.
    """
    pvtName = self.getPrivateName()
    setattr(instance, pvtName, DELETED)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def __class_getitem__(cls, fieldType: Union[type, TypeVar]) -> Self:
    """
    Allows the AttriBox to be used as a generic type with a specified
    field type.
    """
    if isinstance(fieldType, TypeVar):
      return super().__class_getitem__(fieldType)  # noqa
    self = object.__new__(cls)
    self.__field_type__ = fieldType
    return self  # noqa

  def __call__(self, *args, **kwargs) -> Any:
    """Bind constructor arguments for deferred field construction.

    The 'AttriBox[T](*args, **kw)' idiom is a two-step
    decoration: '__class_getitem__' produces a fresh 'AttriBox'
    parametrized with the field type 'T', and this '__call__'
    captures the positional and keyword arguments that should be
    forwarded to 'T(...)' when the field is first accessed on an
    instance. The arguments are stashed via 'Object.__init__'
    (which routes them through 'getPosArgs' / 'getKeyArgs'); the
    field type is not instantiated here.

    Returns 'self' so the call site can chain straight into a
    class-body assignment, e.g. 'x = AttriBox[int](42)'.
    """
    Object.__init__(self, *args, **kwargs)
    return self

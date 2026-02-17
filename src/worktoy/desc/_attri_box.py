"""
AttriBox implements a lazily instantiated and strongly typed descriptor
class.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from . import Field
from ..core import Object
from ..core.sentinels import DELETED
from ..utilities import typeCast
from ..waitaminute import TypeException
from ..waitaminute.dispatch import TypeCastException

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Self


class AttriBox(Object):
  """
  AttriBox implements a lazily instantiated and strongly typed descriptor
  class.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Private Variables
  __field_type__ = None  # The type of the objects stored in the box.

  #  Public Variables
  fieldType = Field()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @fieldType.GET
  def getFieldType(self) -> type:
    return self.__field_type__

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _resolve(self, *args, **kwargs) -> Self:
    """
    Creates a new instance of the field type from the given arguments.
    Please note, that this method does *not* retrieve arguments from
    'self', but requires them to be passed in as arguments. This is because
    this method is used both when setting and getting.

    When '__instance_get__' is unable to retrieve a value from a given
    instance. The 'args' and 'kwargs' passed to the constructor of the
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
    """
    fieldType = self.getFieldType()
    try:
      if fieldType in (list, set, frozenset, dict, tuple):
        fieldObject = fieldType(args)
      else:
        fieldObject = fieldType(*args, **kwargs)
    except (TypeError, ValueError) as exception:
      name = 'value'
      raise TypeException(name, args[0], fieldType) from exception

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

  def __instance_delete__(
      self,
      instance: Any,
      old: Any = None,
      **kwargs,
      ) -> None:
    """
    Deletes the value of the field for the given instance. If the value is
    not set, it does nothing.
    """
    pvtName = self.getPrivateName()
    setattr(instance, pvtName, DELETED)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def __class_getitem__(cls, fieldType: type) -> Self:
    """
    Allows the AttriBox to be used as a generic type with a specified
    field type.
    """
    self = object.__new__(cls)
    self.__field_type__ = fieldType
    return self  # noqa

  def __call__(self, *args: Any, **kwargs: Any) -> Any:
    """
    Allows the AttriBox to be called like a function, returning a new
    instance of the field type.
    """
    Object.__init__(self, *args, **kwargs)
    return self

  def __delete__(self, instance: Any, **kwargs) -> None:
    try:
      Object.__delete__(self, instance, **kwargs)
    except AttributeError as attributeError:
      fieldName = self.getFieldName()
      raise AttributeError(fieldName) from attributeError

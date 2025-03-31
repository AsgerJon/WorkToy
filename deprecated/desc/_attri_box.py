"""AttriBox provides a feature complete implementation of the descriptor
protocol with lazy instantiation. With it, the owning class need only set
one attribute on one line to access the full functionality of the
descriptor. The syntactic sugar is as follows:


class Info:
  # This class provides an attribute class of the Owner class below

  __owning_instance__ = None

  def __init__(self, instance: object) -> None:
    self.__owning_instance__ = instance


class Owner:
  # This class owns attributes through the AttriBox class

  x = AttriBox[float]()
  info = AttriBox[Info](THIS)  # THIS is replaced by the owning instance.


The class of the attribute is placed in the brackets and the parentheses
are given the arguments used to instantiate the attribute. It is possible
to pass special placeholders here which are replaced when the attribute
object is created. The placeholders are:

THIS: The owning instance
TYPE: The owning class
BOX: The AttriBox instance
ATTR: The attribute class or its subclass

The lifecycle of the AttriBox instance is as follows:

1. The AttriBox class itself is created
2. The AttriBox instance is created during the class body execution of a
class that is being created.
3. When the class creation process completes, the '__set_name__' method is
invoked. This class is inherited from the 'CoreDescriptor' class.
4. When this AttriBox instance is accessed through the owning class,
not an instance of it, the AttriBox instance itself returns.
5. When the access is through an instance of the owning class,
the AttriBox instance first attempts to find an existing value in the
namespace of the instance at its private name. This value is returned if
it exists.
6. Otherwise, an instance of the wrapping class 'Bag' is created and an
instance of the inner class is created and stored in the 'Bag' instance.
It is the 'Bag' instance that is stored in the namespace of the owning
class and during calls to __get__, the wrapped object is returned from
inside the Bag instance.
7. By default, the setter method expects the value received to be of the
same type as the existing object in the Bag instance.
8. By default, the deleter method is disabled and will raise an exception.
This is because calls on the form: 'del instance.attribute' must then
cause 'instance.attribute' to result in Attribute error. This is not
really practical as it is insufficient to remove the value as the
descriptor is on the owning class not the instance. This means that no
functionality is present to distinguish between the __delete__ having been
called, and then inner object not having been created yet."""
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

try:
  from typing import Self, Callable
except ImportError:
  Self = object
  Callable = object

try:
  from typing import Never
except ImportError:
  Never = object

try:
  from typing import TYPE_CHECKING
except ImportError:
  TYPE_CHECKING = False

from typing import Any
from depr.desc import NotifyBox, Bag
from worktoy.static import maybe, typeCast, THIS
from worktoy.text import typeMsg, monoSpace


class AttriBox(NotifyBox):
  """AttriBox class improves the AttriBox class!"""

  __is_attribox__ = True

  __default_object__ = None
  __field_class__ = None
  __pos_args__ = None
  __key_args__ = None

  @staticmethod
  def getThisFilter(instance: object) -> Callable:
    """Getter-function for the 'THIS' filter."""

    def thisFilter(obj: object) -> object:
      """Filter for the 'THIS' placeholder."""
      if obj is THIS:
        return instance
      return obj

    return thisFilter

  @classmethod
  def __class_getitem__(cls, fieldClass: type) -> AttriBox:
    """Class method for creating a AttriBox instance."""
    return cls(fieldClass)

  def __init__(self, *args) -> None:
    NotifyBox.__init__(self)
    for arg in args:
      if isinstance(arg, type):
        fieldClass = arg
        break
    else:
      e = """AttriBox constructor requires the fieldClass type!"""
      raise ValueError(e)
    if isinstance(fieldClass, type):
      self.__field_class__ = fieldClass
    else:
      e = """AttriBox constructor requires the fieldClass type!"""
      e2 = typeMsg('fieldClass', fieldClass, type)
      raise TypeError(monoSpace('%s\n%s' % (e, e2)))
    self.__field_class__ = fieldClass

  def __call__(self, *args, **kwargs) -> Self:
    self.__pos_args__ = [*args, ]
    self.__key_args__ = {**kwargs, }
    return self

  def getFieldClass(self, ) -> type:
    """Getter-function for the field class."""
    if self.__field_class__ is None:
      e = """The field class of the AttriBox instance has not been set!"""
      raise AttributeError(e)
    if isinstance(self.__field_class__, type):
      return self.__field_class__
    e = typeMsg('__field_class__', self.__field_class__, type)
    raise TypeError(e)

  def getArgs(self, instance: object, **kwargs) -> list[Any]:
    """Getter-function for positional arguments"""
    if kwargs.get('_root', False):
      return maybe(self.__pos_args__, [])
    thisFilter = self.getThisFilter(instance)
    return [thisFilter(arg) for arg in maybe(self.__pos_args__, [])]

  def getKwargs(self, instance: object, **kwargs) -> dict[str, Any]:
    """Getter-function for keyword arguments"""
    if kwargs.get('_root', False):
      return maybe(self.__key_args__, {})
    thisFilter = self.getThisFilter(instance)
    kw = maybe(self.__key_args__, {})
    return {k: thisFilter(v) for (k, v) in kw.items()}

  def getDefaultFactory(self) -> Any:
    """Getter-function for function creating the default value. """
    keyArgs = self.getKwargs(None, _root=True)
    posArgs = self.getArgs(None, _root=True)
    fieldClass = self.getFieldClass()

    def callMeMaybe(instance: object) -> Any:
      """This function creates the default value."""
      thisFilter = self.getThisFilter(instance)
      newArgs = [thisFilter(arg) for arg in posArgs]
      newKeys = {k: thisFilter(v) for (k, v) in keyArgs.items()}

      if fieldClass is bool:
        innerObject = True if [*newArgs, None][0] else False
      else:
        if newArgs and newKeys:
          innerObject = fieldClass(*newArgs, **newKeys)
        elif newArgs:
          innerObject = fieldClass(*newArgs)
        elif newKeys:
          innerObject = fieldClass(**newKeys)
        else:
          innerObject = fieldClass()
      if TYPE_CHECKING:
        return Bag(None, innerObject)
      return innerObject

    return callMeMaybe

  def createFieldObject(self, instance: object, ) -> Bag:
    """Create the field object. If the default object is set, it is used."""
    factory = self.getDefaultFactory()
    return Bag(instance, factory(instance))

  def __instance_reset__(self, instance: object) -> None:
    """Reset-function for the instance."""
    pvtName = self._getPrivateName()
    delattr(instance, pvtName)

  def __instance_get__(self, instance: object, **kwargs) -> Any:
    """Getter-function for the instance. Please note, that if the call is
    the notifier asking what the previous value was, the functionality in
    the AbstractDescriptor expects and handles the exception. """
    pvtName = self._getPrivateName()
    bag = getattr(instance, pvtName, None)
    if bag is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      innerObject = self.createFieldObject(instance)
      setattr(instance, pvtName, innerObject)
      return self.__instance_get__(instance, _recursion=True)
    if not isinstance(bag, Bag):
      e = typeMsg('bag', bag, Bag)
      raise TypeError(e)
    innerObject = bag.getInnerObject()
    fieldClass = self.getFieldClass()
    if isinstance(innerObject, fieldClass):
      return innerObject
    e = typeMsg('innerObject', innerObject, fieldClass)
    raise TypeError(e)

  def __instance_set__(self, instance: Any, value: Any, **kwargs) -> None:
    """Setter-function for the instance."""
    pvtName = self._getPrivateName()
    fieldCls = self.getFieldClass()
    value = typeCast(value, fieldCls)
    if value is None:
      e = """The '%s' object received a 'None' value in the setter. This 
      object has field name: '%s', field class: '%s' and owner name: '%s'!"""
      boxName = type(self).__name__
      fieldName = self.getFieldName()
      fieldCls = self.getFieldClass().__name__
      ownerName = type(instance).__name__
      e2 = monoSpace(e % (boxName, fieldName, fieldCls, ownerName))
      raise ValueError(e2)
    bag = getattr(instance, pvtName, None)
    if bag is None:
      return setattr(instance, pvtName, Bag(instance, value))
    bag.setInnerObject(value)
    return setattr(instance, pvtName, bag)

  if TYPE_CHECKING:
    from typing import NoReturn as Never

  def __instance_del__(self, instance: object) -> Never:
    """Deleter-function for the instance."""
    e = """Deleter-function is not implemented by the AttriBox class."""
    raise TypeError(e)

  def __str__(self, ) -> str:
    """String representation"""
    posArgs = self.getArgs(None, _root=True)
    keyArgs = self.getKwargs(None, _root=True)
    posStr = ', '.join([str(arg) for arg in posArgs])
    keyStr = ', '.join([f'{k}={v}' for (k, v) in keyArgs.items()])
    argStr = ', '.join([arg for arg in [posStr, keyStr] if arg])
    clsName = self.getFieldClass().__name__
    return """AttriBox[%s](%s)""" % (clsName, argStr)

  def __repr__(self, ) -> str:
    """String representation"""
    return str(self)

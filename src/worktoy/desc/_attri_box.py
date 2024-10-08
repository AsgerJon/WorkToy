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
called, and then inner object not having been created yet.

"""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

try:
  from typing import Self
except ImportError:
  Self = object

try:
  from typing import Never
except ImportError:
  Never = object

try:
  from typing import TYPE_CHECKING
except ImportError:
  TYPE_CHECKING = False

from typing import Any

from worktoy.desc import Bag, THIS, TYPE, AbstractDescriptor, BOX, \
  ATTR, DEFAULT, NODEF
from worktoy.parse import maybe
from worktoy.text import typeMsg, monoSpace


class AttriBox(AbstractDescriptor):
  """AttriBox class improves the AttriBox class!"""

  __default_object__ = None
  __field_class__ = None
  __pos_args__ = None
  __key_args__ = None

  @staticmethod
  def _castNumberTo(value: object, target: type) -> Any:
    """This method handles the cringe cases of ints being rejected as
    floats. """
    if isinstance(value, int):
      if target is int:
        return value
      if target is float:
        return float(value)
      if target is complex:
        return float(value) + 0j
    if isinstance(value, float):
      if target is int:
        if value.is_integer():
          return int(value)
        e = typeMsg('value', value, int)
        raise TypeError(e)
      if target is float:
        return value
      if target is complex:
        return value + 0j
    if isinstance(value, complex):
      if target is int:
        if value.real.is_integer() and not value.imag:
          return int(value.real)
        e = typeMsg('value', value, int)
        raise TypeError(e)
      if target is float:
        if not value.imag:
          return float(value.real)
        e = typeMsg('value', value, float)
        raise TypeError(e)
      if target is complex:
        return value

  @staticmethod
  def _unpackValueToArgsKwargs(value: Any) -> tuple[tuple, dict]:
    """This method unpacks the value into positional and keyword
    arguments."""
    if not value:
      return (), {}
    if not isinstance(value, (list, tuple)):
      return (value,), {}
    if len(value) == 1:
      return (value[0],), {}
    if len(value) == 2:
      if isinstance(value[0], (list, tuple)):
        if isinstance(value[1], dict):
          return (*value[0],), {**value[1], }
    return (*value,), {}

  @classmethod
  def __class_getitem__(cls, fieldClass: type) -> AttriBox:
    """Class method for creating a AttriBox instance."""
    return cls(fieldClass)

  def __init__(self, *args) -> None:
    AbstractDescriptor.__init__(self)
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
    for arg in args:
      if arg is DEFAULT:
        self.__default_object__ = DEFAULT.getDefaultObject()
        if not isinstance(self.__default_object__, self.getFieldClass()):
          e = """The default object is not of the correct type!"""
          e2 = typeMsg('defaultObject', self.__default_object__,
                       self.getFieldClass())
          raise TypeError(monoSpace('%s\n%s' % (e, e2)))
        break
      if arg is NODEF:
        if len(args) - 1 or kwargs:
          e = """The NODEF flag must be the only argument!"""
          raise ValueError(e)
        self.__default_object__ = NODEF
        break
    else:
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
    args = []
    for arg in maybe(self.__pos_args__, []):
      if arg is THIS:
        args.append(instance)
      elif arg is TYPE:
        args.append(self.getFieldOwner())
      elif arg is BOX:
        args.append(self)
      elif arg is ATTR:
        args.append(type(self))
      else:
        args.append(arg)
    return args

  def getKwargs(self, instance: object, **kwargs) -> dict[str, Any]:
    """Getter-function for keyword arguments"""
    if kwargs.get('_root', False):
      return maybe(self.__key_args__, {})
    keyArgs = {}
    for (key, val) in maybe(self.__key_args__, {}).items():
      if val is THIS:
        keyArgs[key] = instance
      elif val is TYPE:
        keyArgs[key] = self.getFieldOwner()
      elif val is BOX:
        keyArgs[key] = self
      elif val is ATTR:
        keyArgs[key] = type(self)
      else:
        keyArgs[key] = val
    return keyArgs

  def getDefaultFactory(self) -> Any:
    """Getter-function for function creating the default value. """
    keyArgs = self.getKwargs(None, _root=True)
    posArgs = self.getArgs(None, _root=True)
    fieldClass = self.getFieldClass()

    zerotons = [BOX, ATTR]
    for zero in zerotons:
      if zero in [*posArgs, *keyArgs.values()]:
        e = """The 'getDefaultFactory' does not BOX and ATTR, 
        but received: %s""" % zero
        raise ValueError(monoSpace(e))

    def callMeMaybe(instance: object) -> Any:
      """This function creates the default value."""
      newKeys = {}
      for (key, val) in keyArgs.items():
        if val is THIS:
          newKeys[key] = instance
        elif val is TYPE:
          newKeys[key] = type(instance)
        else:
          newKeys[key] = val
      newArgs = []
      for arg in posArgs:
        if arg is THIS:
          newArgs.append(instance)
        elif arg is TYPE:
          newArgs.append(type(instance))
        else:
          newArgs.append(arg)
      if fieldClass is bool:
        innerObject = True if [*newArgs, None][0] else False
      else:
        innerObject = fieldClass(*newArgs, **newKeys)
      if TYPE_CHECKING:
        return Bag(None, innerObject)
      return innerObject

    return callMeMaybe

  def createFieldObject(self, instance: object, ) -> Bag:
    """Create the field object. If the default object is set, it is used."""
    if self.__default_object__ is not None:
      return Bag(instance, self.__default_object__)
    if self.__field_class__ is None:
      e = """AttriBox instance has not been initialized!"""
      raise AttributeError(e)
    if self.__pos_args__ is None or self.__key_args__ is None:
      e = """AttriBox instance has not been called!"""
      raise AttributeError(e)
    keyArgs = self.getKwargs(instance, )
    posArgs = self.getArgs(instance, )
    fieldClass = self.getFieldClass()
    if fieldClass is bool:
      innerObject = True if [*posArgs, None][0] else False
    else:
      innerObject = fieldClass(*posArgs, **keyArgs)
    return Bag(instance, innerObject)

  def __instance_reset__(self, instance: object) -> None:
    """Reset-function for the instance."""
    pvtName = self._getPrivateName()
    delattr(instance, pvtName)

  def __instance_get__(self, instance: object, **kwargs) -> Any:
    """Getter-function for the instance. Please note, that if the call is
    the notifier asking what the previous value was, the functionality in
    the AbstractDescriptor expects and handles the exception. """
    pvtName = self._getPrivateName()
    if getattr(instance, pvtName, None) is None:
      if self.__default_object__ is NODEF:
        e = """This instance of %s has the NODEF flag set, and the 
        required explicitly set value is missing! NODEF requires that an 
        explicit value be set for the attribute.""" % self.getFieldName()
        raise TypeError(monoSpace(e))
      if kwargs.get('_recursion', False):
        raise RecursionError
      setattr(instance, pvtName, self.createFieldObject(instance))
      return self.__instance_get__(instance, _recursion=True)
    bag = getattr(instance, pvtName)
    if not isinstance(bag, Bag):
      e = typeMsg('bag', bag, Bag)
      raise TypeError(e)
    innerObject = bag.getInnerObject()
    fieldClass = self.getFieldClass()
    if isinstance(innerObject, fieldClass):
      return innerObject
    e = typeMsg('innerObject', innerObject, fieldClass)
    raise TypeError(e)

  def __instance_set__(self,
                       instance: object,
                       value: object,
                       **kwargs) -> None:
    """Setter-function for the instance."""
    pvtName = self._getPrivateName()
    fieldCls = self.getFieldClass()
    if isinstance(value, fieldCls):
      bag = getattr(instance, pvtName, None)
      if bag is None:
        return setattr(instance, pvtName, Bag(instance, value))
      bag.setInnerObject(value)
      return setattr(instance, pvtName, bag)
    if fieldCls in [int, float, complex]:
      if kwargs.get('_recursion2', False):
        e = typeMsg('value', value, fieldCls)
        raise TypeError(e)
      return self.__instance_set__(instance,
                                   self._castNumberTo(value, fieldCls),
                                   _recursion2=True)
    if not isinstance(value, (tuple, list)):
      if kwargs.get('_recursion3', False):
        raise RecursionError
      return self.__instance_set__(instance, (value,), _recursion3=True)
    if kwargs.get('_recursion', False):
      e = typeMsg('value', value, fieldCls)
      raise TypeError(e)
    newValue = None
    try:
      args, kwargs2 = self._unpackValueToArgsKwargs(value)
      newValue = fieldCls(*args, **kwargs2)
    except ValueError as valueError:
      if 'could not convert' in str(valueError):
        e = """Could not convert the value to the field class!"""
        e2 = typeMsg('value', value, fieldCls)
        raise TypeError(monoSpace('%s\n%s' % (e, e2)))
    return self.__instance_set__(instance, newValue, _recursion=True)

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

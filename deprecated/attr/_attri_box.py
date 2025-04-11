"""AttriBox subclasses the AbstractBox and implements support for object
creation based on a given field class and a set of arguments. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from re import compile

from worktoy.attr import AbstractBox
from worktoy.static import thisFilterFactory, typeCast
from worktoy.text import monoSpace, typeMsg
from worktoy.waitaminute import EmptyBox

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Self, Any, Callable


class AttriBox(AbstractBox):
  """AttriBox subclasses the AbstractBox and implements support for object
  creation based on a given field class and a set of arguments. """

  #  Utility methods

  #  Private variables

  __field_class__ = None
  __pos_args__ = None
  __key_args__ = None

  #  Instantiation methods

  def __class_getitem__(cls, fieldClass: type) -> Self:
    """Class method for creating a AttriBox instance."""
    return cls(fieldClass, _root=True)

  def __init__(self, fieldClass: Any, **kwargs) -> None:
    if not kwargs.get('_root', False):
      e = """AttriBox instances should use the special syntax:
      AttriBox[FieldClass](*args, **kwargs)!"""
      raise ValueError(monoSpace(e))
    if not isinstance(fieldClass, type):
      e = typeMsg('fieldClass', fieldClass, type)
      raise TypeError(monoSpace(e))
    self.__field_class__ = fieldClass

  def __call__(self, *args, **kwargs) -> Self:
    """Set the arguments for the object creation."""
    if self.__pos_args__ is not None:
      e = """The positional arguments have already been set!"""
      raise AttributeError(monoSpace(e))
    if self.__key_args__ is not None:
      e = """The keyword arguments have already been set!"""
      raise AttributeError(monoSpace(e))
    self.__pos_args__ = [*args, ]
    self.__key_args__ = {**kwargs, }
    return self

  #  Getter methods

  def getFieldClass(self, ) -> type:
    """Getter-function for the field class."""
    if self.__field_class__ is None:
      e = """The field class of the AttriBox instance has not been set!"""
      raise AttributeError(monoSpace(e))
    if isinstance(self.__field_class__, type):
      return self.__field_class__
    e = typeMsg('__field_class__', self.__field_class__, type)
    raise TypeError(monoSpace(e))

  def getArgs(self, instance: object = None) -> list:
    """Getter-function for arguments. If the instance is provided, and the
    special 'THIS' object is found in the arguments, it is replaced with the
    instance. If the instance is not provided, the 'THIS' object is left
    untouched."""
    if self.__pos_args__ is None:
      e = """The positional arguments of the AttriBox instance have not been
      set!"""
      raise AttributeError(monoSpace(e))
    if instance is None:
      return self.__pos_args__
    return thisFilterFactory(instance)(self.getArgs())

  def getKwargs(self, instance: object = None) -> dict:
    """Getter-function for keyword arguments. If the instance is provided,
    and the special 'THIS' object is found in the arguments,
    it is replaced with the instance. If the instance is not provided,
    the 'THIS' object is left untouched."""
    if self.__key_args__ is None:
      e = """The keyword arguments of the AttriBox instance have not been
      set!"""
      raise AttributeError(monoSpace(e))
    if instance is None:
      return self.__key_args__
    return thisFilterFactory(instance)(self.getKwargs())

  def getDefaultFactory(self) -> Callable:
    """Getter-function for the default factory function."""
    fieldClass = self.getFieldClass()
    args = self.getArgs()
    kwargs = self.getKwargs()

    if fieldClass is bool:
      def callMeMaybe(instance, ) -> Any:
        """Function for creating the default value."""
        return True if [args, None][0] else False

      return callMeMaybe

    def callMeMaybe(instance, ) -> Any:
      """Function for creating the default value."""
      thisFilter = thisFilterFactory(instance)
      newArgs = thisFilter(*args)
      newKwargs = thisFilter(**kwargs)
      if newArgs and newKwargs:
        return fieldClass(*newArgs, **newKwargs)
      if newArgs:
        return fieldClass(*newArgs)
      if newKwargs:
        return fieldClass(**newKwargs)
      return fieldClass()

    return callMeMaybe

  def getPrivateName(self, ) -> str:
    """Getter-function for the private name of the field."""
    fieldName = self.getFieldName()
    pattern = compile(r'(?<!^)(?=[A-Z])')
    return '__%s__' % pattern.sub('_', fieldName).lower()

  #  Creation of the field object for a given instance

  def __get_existing__(self, instance: object, ) -> Any:
    """Getter-method for the existing field object."""
    privateName = self.getPrivateName()
    fieldObject = getattr(instance, privateName, None)
    if fieldObject is None:
      raise EmptyBox(self, instance)
    return fieldObject

  def __get_new__(self, instance: object, ) -> Any:
    """Getter-method for the new field object."""
    factory = self.getDefaultFactory()
    fieldObject = factory(instance)
    privateName = self.getPrivateName()
    setattr(instance, privateName, fieldObject)
    return fieldObject

  def __instance_set__(self, instance: object, value: Any) -> None:
    """Setter-method for the field object."""
    pvtName = self.getPrivateName()
    fieldCls = self.getFieldClass()
    setattr(instance, pvtName, typeCast(value, fieldCls))

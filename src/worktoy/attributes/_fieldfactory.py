"""WorkToy - Attributes - FieldFactory
Alternative to descriptors. Setting an instance of Field factory in a
class body creates the necessary variables and methods on the target
class."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.attributes import StrAttribute
from worktoy.core import DefaultClass


class FieldFactory(DefaultClass):
  """WorkToy - Attributes - FieldFactory
  Alternative to descriptors. Setting an instance of Field factory in a
  class body creates the necessary variables and methods on the target
  class."""

  __field_name__ = StrAttribute()
  __private_name__ = StrAttribute()
  __getter_name__ = StrAttribute()
  __setter_name__ = StrAttribute()
  __deleter_name__ = StrAttribute()

  def __init__(self, *args, **kwargs) -> None:
    DefaultClass.__init__(self, *args, **kwargs)
    self.sourceClass = None
    self.targetClass = None
    self._fieldName = None

  def __set_name__(self, target: type, name: str) -> None:
    self.setFieldName(name)
    self.setTargetClass(target)

  def setFieldName(self, name: str) -> None:
    """Setter-function for the name of this FieldFactory instance as it in
    the class body of the target class."""
    self._fieldName = name
    firstLetterUpper = name[0].upper()
    firstLetterLower = name[0].lower()
    nameLetters = name[1:]
    self.__field_name__ = self._fieldName
    self.__private_name__ = '_%s%s' % (firstLetterLower, nameLetters)
    self.__getter_name__ = '_get%s%s' % (firstLetterUpper, nameLetters)
    self.__setter_name__ = '_set%s%s' % (firstLetterUpper, nameLetters)
    self.__deleter_name__ = '_del%s%s' % (firstLetterUpper, nameLetters)

  def setterFactory(self, targetClass: type) -> type:
    """Creates the setter function. Please note that this method is set on
    the class, but is called on the instance. When it is set on the class,
    it becomes an instance method. This means that after retrieving the
    method with:
      'setter = getattr(cls, __setter_name__)'
      'setter(obj, newValue)'
    The setter does not receive the instance variable. This is because
    the setter is retrieved from the class. Alternatively:
      'setter = getattr(obj, __setter_name__)'
      'setter(newValue)'
    """

    def setterFunction(instance: object, newValue: object) -> None:
      """Setter function"""
      setattr(instance, self.__private_name__, newValue)

    setattr(targetClass, self.__setter_name__, setterFunction)

    return targetClass

  def getterFactory(self, targetClass: type) -> type:
    """Creates the getter function. """

    def getterFunction(instance: object, ) -> object:
      """Getter function"""
      out = getattr(instance, self.__private_name__, None)
      if out is None:
        pass

      return out

    setattr(targetClass, self.__getter_name__, getterFunction)

    return targetClass

  def creatorFactory(self, targetClass: type) -> type:
    """Creator function"""

    def creatorFunction(instance: object) -> None:
      """Creates an instance of the source class exposed by the field."""
      newInstance = self.sourceInstanceCreator()
      setter = getattr(targetClass, self.__setter_name__, None)
      if setter is None:
        raise self.createUnexpectedStateError()
      setattr(targetClass, self.__private_name__, newInstance)

  def setTargetClass(self, targetClass: type) -> type:
    """Setter-function for target class."""

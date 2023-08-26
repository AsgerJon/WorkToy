"""WorkToy - Attributes - VariableAttribute
Expands the attribute class to support immutable types requiring setters.
"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.attributes import ConstantAttribute


class VariableAttribute(ConstantAttribute):
  """WorkToy - Attributes - VariableAttribute
  Expands the attribute class to support immutable types requiring setters.
  """

  def __init__(self, value: object,
               type_: type = None, *args, **kwargs) -> None:
    ConstantAttribute.__init__(self, value, type_, *args, **kwargs)

  def getSetterFunctionName(self) -> str:
    """Name of the getter function"""
    startLetter = self.getFieldName()[0].upper()
    remaining = self.getFieldName()[1:]
    return '_set%s%s' % (startLetter, remaining)

  def setterFunctionFactory(self, targetClass: type) -> type:
    """Creates a setter function for target class"""
    setterFunctionName = self.getSetterFunctionName()
    privateFieldName = self.getPrivateVariableName()

    def setterFunction(cls: type, instance: object, val: object) -> None:
      """Setter-function"""
      setattr(instance, privateFieldName, val)

    setattr(targetClass, setterFunctionName, classmethod(setterFunction))
    return targetClass

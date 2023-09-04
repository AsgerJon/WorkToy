"""WorkToy - Fields - AbstractView
Views are pseudo fields that act like fields, but where the getter is not
actually 'getting' the value of an underlying valuable, but instead 'gets'
the function value on the instance. """
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from worktoy.core import Function
from worktoy.fields import AbstractField
from worktoy.guards import TypeGuard, SomeGuard, NoneGuard


class AbstractView(AbstractField):
  """WorkToy - Fields - AbstractView
  Views are pseudo fields that act like fields, but where the getter is not
  actually 'getting' the value of an underlying valuable, but instead 'gets'
  the function value on the instance. """

  functionGuard = TypeGuard(Function)
  someGuard = SomeGuard()
  noneGuard = NoneGuard()

  def __init__(self, *args, **kwargs) -> None:
    AbstractField.__init__(self, None, *args, **kwargs)
    self.__inner_function__ = None

  def __call__(self, func: Function) -> Function:
    """Setter-function for the method obtaining the value. Use as a
    decorator in the class body. For example:

    from worktoy.fields import IntField
    class Rectangle:
      #  Sample class representing a rectangle
      width = IntField(1)
      height = IntField(1)
      areaView = AbstractView()

      @areaView
      def area(self) -> int:
        #  Returns the area of the rectangle
        return self.height * self.width

    rect = Rectangle(3, 4)
    rect.width  # output: 3
    rect.height  # output: 4
    """

    if isinstance(self.__inner_function__, Function):
      raise NotImplementedError
    self.__inner_function__ = getattr(func, '__func__', func)

  def _getInnerFunction(self) -> Function:
    """Getter-function for the inner function. This function is
    responsible for raising an error if the inner function is not
    available. """
    return self.functionGuard(self.__inner_function__)

  def explicitGetter(self, obj: object, cls: type) -> Any:
    """Returned by invoking the inner function"""
    func = self._getInnerFunction()
    return func(obj, cls)

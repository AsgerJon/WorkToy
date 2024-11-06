"""The 'ExplicitBox' class is a subclass of the 'AttriBox' class that
allows the user to explicitly set the default value of the field."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

try:
  from typing import Callable, Any, Self
except ImportError:
  Callable = object
  Any = object
  Self = object

from worktoy.desc import AttriBox
from worktoy.parse import typeCast


class ExplicitBox(AttriBox):
  """The '_ExplicitBox' class is a subclass of the 'AttriBox' class that
  allows the user to explicitly set the default value of the field."""

  __explicit_default__ = None

  def getExplicitDefault(self) -> Any:
    """This method returns the explicit default value of the field."""
    if self.__explicit_default__ is None:
      e = """The default value of the field is not explicitly set!"""
      raise ValueError(e)
    fieldCls = self.getFieldClass()
    return typeCast(self.__explicit_default__, fieldCls)

  def setExplicitDefault(self, value: Any) -> None:
    """This method sets the explicit default value of the field."""
    if self.__explicit_default__ is not None:
      e = """The default value of the field is already explicitly set!"""
      raise ValueError(e)
    fieldCls = self.getFieldClass()
    self.__explicit_default__ = typeCast(value, fieldCls)

  def __call__(self, *args, **kwargs) -> Self:
    """This method sets the default value of the field."""
    if kwargs:
      e = """The '%s' class dose not allow keyword arguments!"""
      raise TypeError(e % self.__class__.__name__)
    if not args:
      e = """The '%s' class requires one positional argument!"""
      raise TypeError(e % self.__class__.__name__)
    if len(args) - 1:
      e = """The '%s' class requires only one positional argument!"""
      raise TypeError(e % self.__class__.__name__)
    self.setExplicitDefault(args[0])
    return self

  def getDefaultFactory(self) -> Callable:
    """This method returns the default factory function."""
    explicitDefault = self.getExplicitDefault()

    def callMeMaybe(instance: object) -> Any:
      """This function returns the default value of the field."""
      return explicitDefault

    return callMeMaybe

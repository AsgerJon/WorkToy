"""The 'ExplicitBox' class is a subclass of the 'AttriBox' class that
allows the user to explicitly set the default value of the field."""
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from depr.meta import CallMeMaybe

try:
  from typing import Any, Self
except ImportError:
  Any = object
  Self = object

from depr.desc import AttriBox
from worktoy.static import typeCast


class ExplicitBox(AttriBox):
  """The '_ExplicitBox' class is a subclass of the 'AttriBox' class that
  allows the user to explicitly set the default value of the field."""

  __explicit_default__ = None

  def setExplicitDefault(self, value: Any) -> None:
    """This method sets the explicit default value of the field."""
    if self.__explicit_default__ is not None:
      e = """The default value of the field is already explicitly set!"""
      raise ValueError(e)
    fieldCls = self.getFieldClass()
    self.__explicit_default__ = typeCast(value, fieldCls)

  def getExplicitDefault(self) -> Any:
    """This method returns the explicit default value of the field."""
    if self.__explicit_default__ is None:
      e = """The default value of the field is not explicitly set!"""
      raise ValueError(e)
    fieldCls = self.getFieldClass()
    return typeCast(self.__explicit_default__, fieldCls)

  def hasExplicitDefault(self) -> bool:
    """This method returns True if the field has an explicit default
    value."""
    return False if self.__explicit_default__ is None else True

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

  def getDefaultFactory(self) -> CallMeMaybe:
    """This method returns the default factory function."""
    if self.hasExplicitDefault():
      explicitDefault = self.getExplicitDefault()

      def callMeMaybe(instance: object) -> Any:
        """This function returns the default value of the field."""
        return explicitDefault
    else:
      fieldCls = self.getFieldClass()

      def callMeMaybe(instance: object) -> Any:
        """This function returns the default value of the field."""
        return fieldCls()

    return callMeMaybe

"""ExplicitBox subclasses AttriBox and allows an explicit default value to
be used instead of invoking the default factory function. """
#  AGPL-3.0 license
#  Copyright (c) 2024-2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.attr import AttriBox

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any, Callable


class ExplicitBox(AttriBox):
  """ExplicitBox subclasses AttriBox and allows an explicit default value to
  be used instead of invoking the default factory function. """

  __explicit_default__ = None

  def __init__(self, *args, **kwargs) -> None:
    """This method initializes the field."""
    if kwargs.get('_root', False):
      AttriBox.__init__(self, *args, **kwargs)
    else:
      self.__explicit_default__ = args[0]
      AttriBox.__init__(self, type(args[0]), _root=True)
      self()

  def hasExplicitDefault(self) -> bool:
    """This method returns True if the field has an explicit default
    value."""
    return False if self.__explicit_default__ is None else True

  def getExplicitDefault(self) -> Any:
    """This method returns the explicit default value of the field."""
    if self.__explicit_default__ is None:
      e = """The default value of the field is not explicitly set!"""
      raise ValueError(e)
    return self.__explicit_default__

  def getDefaultFactory(self) -> Callable:
    """This method returns the default factory function."""
    explicitDefault = self.getExplicitDefault()

    def callMeMaybe(instance: object) -> Any:
      """This function returns the default value of the field."""
      return explicitDefault

    return callMeMaybe

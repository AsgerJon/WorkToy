"""WorkToy - Guards - TypeGuard
This class checks against None and a type given in the constructor. """
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any, Never, TYPE_CHECKING

from worktoy.guards import AbstractGuard

if TYPE_CHECKING:
  pass


class TypeGuard(AbstractGuard):
  """WorkToy - Guards - TypeGuard
  This class checks against None and a type given in the constructor. """

  def __init__(self, type_: type, *args, **kwargs) -> None:
    self._type = type_
    AbstractGuard.__init__(self, *args, **kwargs)

  def __call__(self, argument: Any, name: str) -> Any:
    """Calling the guard instance returns the argument back if it passes
    the check."""
    index = self.argumentCheck(argument)
    if not index:
      return argument
    return self.exceptionFactory(index, argument, name)

  def getType(self) -> type:
    """Getter-function for the allowed type."""
    return self._type

  def argumentCheck(self, argument: Any) -> int:
    if argument is None:
      return 1
    if isinstance(argument, self.getType()):
      return 0
    return 2

  def exceptionFactory(self, index: int, argument: Any, name: str,
                       *args, **kwargs) -> Never:
    """Raises one error if the argument is None, but a different one if
    the argument is of a different type that the allowable one. """
    if index == 1:
      from worktoy.waitaminute import UnexpectedStateError
      raise UnexpectedStateError(name)
    if index == 2:
      from worktoy.waitaminute import TypeSupportError
      expectedType = self.getType()
      actualValue = argument
      argName = name
      raise TypeSupportError(expectedType, actualValue, argName)
    raise TypeError

  def repairer(self, argument: Any) -> Any:
    """Not implemented."""
    raise NotImplementedError

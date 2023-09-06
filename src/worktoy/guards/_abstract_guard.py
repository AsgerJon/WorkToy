"""WorkToy - Guards - AbstractGuard
This package provides custom handling of exceptions."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
from typing import Any, TYPE_CHECKING, Never

from worktoy.base import DefaultClass

if TYPE_CHECKING:
  pass


class AbstractGuard(DefaultClass):
  """WorkToy - Guards - AbstractGuard
  Raises a relevant error if a variable is of the wrong type. Raises a
  different error if the variable is None. """

  def __init__(self, *args, **kwargs) -> None:
    DefaultClass.__init__(self, *args, **kwargs)

  @abstractmethod
  def argumentCheck(self, argument: Any) -> int:
    """Subclasses must implement this method to determine if an argument is
    acceptable. The return value is expected to be an integer where 0
    indicates that the argument is accepted. Other values should then
    indicate a reason why the argument is rejected. """

  @abstractmethod
  def exceptionFactory(self, *args, **kwargs) -> Never:
    """For each possible rejection mode defined on the argument check,
    this method must raise an appropriate exception. Subclass should
    implement this to handle each, but are allowed to have a final
    catch-all exception."""

  @abstractmethod
  def repairer(self, argument: Any) -> Any:
    """Besides raising the correct error message, subclasses may provide
    attempts at converting rejected arguments. The return value from this
    method is passed back to the beginning of the checks."""

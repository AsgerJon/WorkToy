"""ComplexCast converts from str, int, bool and float to complex."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

try:
  from typing import Self, TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import Self
  except ImportError:
    Self = object
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

from worktoy.waitaminute import CastMismatch
from worktoy.static import AbstractCast, IntCast, FloatCast


class ComplexCast(AbstractCast):
  """ComplexCast converts from str, int, bool and float to complex."""

  intCast = IntCast()
  floatCast = FloatCast()

  def getTargetType(self, **kwargs) -> type:
    """Get the target type of the cast. Subclasses must implement this
    method to return the target type."""
    return complex

  def _cast(self, *args, **kwargs) -> complex:
    """Cast the arguments to the target type."""
    if TYPE_CHECKING:
      assert callable(self.intCast)
      assert callable(self.floatCast)
    if len(args) - 1:
      e = """%s expects exactly one argument, but received %d: \n%s"""
      clsName = type(self).__name__
      nArgs = len(args)
      fmt = lambda arg: '  %s of type: %s' % (str(arg), type(arg).__name__)
      listArgs = '\n'.join([fmt(arg) for arg in args])
      raise TypeError(e % (clsName, nArgs, listArgs))
    arg = args[0]
    if isinstance(arg, complex):
      return arg
    if isinstance(arg, bool):
      return (1.0 if arg else 0.0) + 0j
    if isinstance(arg, int):
      return self.floatCast(arg) + 0j
    if isinstance(arg, float):
      return arg + 0j
    if isinstance(arg, str):
      try:
        return complex(arg)
      except Exception as exception:
        e = """Parsing strings to complex numbers is not yet implemented!"""
        raise NotImplementedError(e) from exception
    try:
      return complex(arg)
    except Exception as exception:
      raise CastMismatch(complex, arg) from exception

  def __get__(self, instance: object, owner: type) -> Self:
    """Get the ComplexCast object."""
    return self

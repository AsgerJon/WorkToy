"""IntCast class converts from str, float, bool and complex to int. """
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

try:
  from typing import Self
except ImportError:
  try:
    from typing_extensions import Self
  except ImportError:
    Self = object

from worktoy.static import AbstractCast
from worktoy.waitaminute import CastMismatch


class IntCast(AbstractCast):
  """IntCast class converts from str, float, bool and complex to int. """

  def getTargetType(self, **kwargs) -> type:
    """Get the target type of the cast. Subclasses must implement this
    method to return the target type."""
    return int

  def _cast(self, *args, **kwargs) -> int:
    """Cast the arguments to the target type."""
    if len(args) - 1:
      e = """%s expects exactly one argument, but received %d: \n%s"""
      clsName = type(self).__name__
      nArgs = len(args)
      fmt = lambda arg: '  %s of type: %s' % (str(arg), type(arg).__name__)
      listArgs = '\n'.join([fmt(arg) for arg in args])
      raise TypeError(e % (clsName, nArgs, listArgs))
    arg = args[0]
    if isinstance(arg, int):
      return arg
    if isinstance(arg, bool):
      return 1 if arg else 0
    if isinstance(arg, float):
      if arg.is_integer():
        return int(arg)
      raise CastMismatch(int, arg)
    if isinstance(arg, complex):
      if arg.imag:
        raise CastMismatch(int, arg)
      try:
        return self._cast(arg.real)
      except CastMismatch:
        raise CastMismatch(int, arg)
    if isinstance(arg, str):
      try:
        return int(arg)
      except ValueError:
        raise CastMismatch(int, arg)
    try:
      return int(arg)
    except Exception as exception:
      raise CastMismatch(int, arg) from exception

  def __get__(self, instance: object, owner: type) -> Self:
    """Get the IntCast object."""
    return self

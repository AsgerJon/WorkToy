"""WorkToy - Wait A Minute! - ArgumentError
Raised when a function, particularly a constructor, is missing a required
argument.

When an argument has defaulted to None because of a missing input value,
it is common to see TypeError as the error message. This is correct in
that 'NoneType' is in fact an unexpected type. Nevertheless, the real
problem in such a case is a missing argument, not a type related problem.
For this reason, the ArgumentError should be raised instead.

This error should not be raised """
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.waitaminute import MetaXcept


class ArgumentError(MetaXcept):
  """WorkToy - Wait A Minute! - ArgumentError
  Raised when a function, particularly a constructor, is missing a required
  argument."""

  def __init__(self, argName: str, argType: type, *args, **kwargs) -> None:
    MetaXcept.__init__(self, argName, argType, *args, **kwargs)
    self._argName = self.pretty(argName)
    self._argType = self.pretty(argType)

  def __str__(self) -> str:
    header = MetaXcept.__str__(self)
    func = self.getSourceFunctionName()
    name, type_ = self._argName, self._argType
    msg = """Function '%s' is missing required argument '%s: %s'."""
    body = msg % (func, name, type_)
    return self.monoSpace('<br>'.join([header, body]))

"""WorkToy - Wait A Minute! - MissingAnnotationsError
Raised when a function is lacking annotations."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core import Function
from worktoy.waitaminute import MetaXcept


class MissingAnnotationsError(MetaXcept):
  """WorkToy - Wait A Minute! - MissingAnnotationsError
  Raised when a function is lacking annotations."""

  def __init__(self, func: Function, *args, **kwargs) -> None:
    MetaXcept.__init__(self, func, *args, **kwargs)
    self._func = func

  def __str__(self, ) -> str:
    header = MetaXcept.__str__(self)

    body = """Typehints are required for function overloading in the 
    WorkToy MetaClass system, but are missing from the function: '%s'!"""

    msg = body % self._func

    return '%s\n%s' % (header, self.justify(msg))

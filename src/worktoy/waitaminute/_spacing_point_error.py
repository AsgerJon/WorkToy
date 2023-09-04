"""WorkToy - Wait A Minute! - SpacingPointError
Raised when a sampling function receives n less than 2."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.waitaminute import MetaXcept


class SpacingPointError(MetaXcept):
  """WorkToy - Wait A Minute! - SpacingPointError
  Raised when a sampling function receives n less than 2."""

  def __init__(self, n: int, *args, **kwargs) -> None:
    MetaXcept.__init__(self, n, *args, **kwargs)
    self._n = n

  def __str__(self) -> str:
    header = MetaXcept.__str__(self)
    msg = """Sample function %s requires at least 2 points, but received 
    n=%d""" % (self.getSourceFunctionName(), self._n)
    return '%s\n%s' % (header, self.justify(msg))

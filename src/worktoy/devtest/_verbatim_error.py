"""WorkToy - Wait A Minute! - VerbatimError
Temporary placeholder error."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.waitaminute import MetaXcept


class VerbatimError(MetaXcept):
  """WorkToy - Wait A Minute! - VerbatimError
  Temporary placeholder error."""

  def __init__(self, *args, **kwargs) -> None:
    MetaXcept.__init__(self, *args, **kwargs)
    self._msg = None
    for arg in args:
      if isinstance(arg, str) and self._msg is None:
        self._msg = arg
        break

  def __str__(self) -> str:
    return self._msg

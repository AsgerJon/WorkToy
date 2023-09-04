"""WorkToy - Wait A Minute! - NameSpaceError
General exception relating to namespaces in metaclass implementations."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.waitaminute import MetaXcept


class NameSpaceError(MetaXcept):
  """WorkToy - Wait A Minute! - NameSpaceError
  General exception relating to namespaces in metaclass implementations."""

  def __init__(self, msg: str, *args, **kwargs) -> None:
    MetaXcept.__init__(self, msg, *args, **kwargs)
    self._msg = msg

  def __str__(self) -> str:
    return self._msg

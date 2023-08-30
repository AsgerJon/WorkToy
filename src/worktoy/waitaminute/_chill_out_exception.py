"""WorkToy - Wait A Minute! - ChillOutException
This exception should be raised to control behaviour with exceptions."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.waitaminute import MetaXcept


class ChillOutException(MetaXcept):
  """WorkToy - Wait A Minute! - ChillOutException
  This exception should be raised to control behaviour with exceptions."""

  def __init__(self, *args, **kwargs) -> None:
    MetaXcept.__init__(self, *args, **kwargs)
    self._msg = None

    for arg in args:
      if isinstance(arg, str) and self._msg is None:
        self._msg = arg
    self.msg = 'Just chill out :)' if self._msg is None else self._msg

  def __str__(self) -> str:
    return self._msg

  def handle(self, *args, **kwargs) -> None:
    """No need to raise anything."""
    pass

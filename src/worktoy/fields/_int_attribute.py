"""WorkToy - Fields - IntAttribute
Integer valued attribute."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.fields import AbstractField


class IntAttribute(AbstractField):
  """WorkToy - Fields - IntAttribute
  Integer valued attribute."""

  def __init__(self, *args, **kwargs) -> None:
    AbstractField.__init__(self, *args, **kwargs)
    self._defaultValue = self.maybe(int, *args, 0)

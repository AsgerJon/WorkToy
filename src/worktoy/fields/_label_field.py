"""WorkToy - Fields - LabelField
The Label class implements descriptors to allow for string variables. """
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from icecream import ic

from worktoy.fields import AbstractField


class LabelField(AbstractField):
  """WorkToy - Fields - LabelField
  The Label class implements descriptors to allow for string variables. """

  def __init__(self, text: str = None, *args, **kwargs) -> None:
    AbstractField.__init__(self, *args, **kwargs)
    self.setDefaultValue(text)

  def getFieldSource(self) -> type:
    """Forces source to be string."""
    return str

  def setFieldSource(self, source: type) -> None:
    """Disabled source type setter."""
    raise TypeError

  def __str__(self, ) -> str:
    """Possibly, the default value returned here replaces the inner value."""
    out = super().__str__()
    ic(out)
    return out

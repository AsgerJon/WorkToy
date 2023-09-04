"""WorkSide - Style - FontSizeField
Subclass of IntField."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any, TYPE_CHECKING

from PySide6.QtGui import QFont

from workside.style import FontSize
from worktoy.fields import IntField
from worktoy.waitaminute import TypeSupportError


class FontSizeField(IntField):
  """WorkSide - Style - FontSizeField
  Subclass of IntField."""

  def __init__(self, defVal: Any, *args, **kwargs) -> None:
    if not isinstance(defVal, int):
      try:
        defVal = int(defVal)
      except Exception:
        raise TypeSupportError(int, defVal, 'defVal') from Exception
    IntField.__init__(self, defVal, *args, **kwargs)

  def explicitGetter(self, obj: object, cls: type) -> object:
    return FontSize(IntField.explicitGetter(self, obj, cls))

  def explicitSetter(self, obj: object, val: Any) -> None:
    newValue = val if isinstance(val, int) else int(val)
    IntField.explicitSetter(self, obj, newValue)

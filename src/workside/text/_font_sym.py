"""WorkSide - Style - Font - FONT
The FONT class, capitalised to avoid collision with the PySide6 namespace,
provides text related functionality."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from workside.style import FontFamilyField, FontWeightField, FontSizeField
from worktoy.base import DefaultClass


class FontSym(DefaultClass):
  """WorkSide - Style - Font
  Implementing descriptor access to text values."""

  family = FontFamilyField()
  ptSide = FontSizeField()
  weight = FontWeightField()

  def __init__(self, *args, **kwargs) -> None:
    DefaultClass.__init__(self, *args, **kwargs)

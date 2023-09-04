"""WorkSide - Style - AlignmentSymField
Symbolic field for alignment values."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from workside.style import AlignmentSym
from worktoy.fields import SymField, IntField

if TYPE_CHECKING:
  from worktoy.sym import SyMeta


class AlignmentSymField(SymField):
  """WorkSide - Style - AlignmentSymField
  Symbolic field for alignment values."""

  def __init__(self, *args, **kwargs) -> None:
    IntField.__init__(self, 0, *args, **kwargs)

  def getSymClass(self) -> SyMeta:
    """Getter-function for the symbolic class."""
    return AlignmentSym

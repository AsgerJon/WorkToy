"""WorkToy - Wait A Minute! - SymbolicConversionError
Raised when conversion between symbolic value and integer value fails."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any, TYPE_CHECKING

from worktoy.waitaminute import MetaXcept

if TYPE_CHECKING:
  from worktoy.sym import SyMeta


class SymbolicConversionError(MetaXcept):
  """WorkToy - Wait A Minute! - SymbolicConversionError
  Raised when conversion between symbolic value and integer value fails."""

  def __init__(self, sym: SyMeta, sourceValue: Any, *args,
               **kwargs) -> None:
    MetaXcept.__init__(self, sym, sourceValue, *args, **kwargs)
    self._sym = sym
    self._sourceValue = sourceValue

  def _conversionMessage(self, ) -> str:
    if isinstance(self._sourceValue, int):
      msg = """Failed to convert integer %d to a member of symbolic class 
      %s!"""
      return msg % (self._sourceValue, self._sym)
    if not isinstance(self._sourceValue, int):
      msg = """Failed to convert member %s of symbolic class %s to 
      integer value!"""
      return msg % (self._sym, self._sourceValue)

  def __str__(self) -> str:
    header = MetaXcept.__str__(self)
    msg = self._conversionMessage()
    return '%s\n%s' % (header, self.justify(msg))

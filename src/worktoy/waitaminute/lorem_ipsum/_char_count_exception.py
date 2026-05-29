"""
CharCountException is raised when a text generator receives a
'charCount' below the minimum its type allows.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ...utilities import textFmt

if TYPE_CHECKING:  # pragma: no cover
  pass


class CharCountException(ValueError):
  """
  Raised when a 'BaseGenerator' subclass receives a 'charCount' below
  the minimum the generator type allows. A target that small leaves no
  room to lay out even one unit of text, so the generator would
  otherwise divide by zero or loop without end.
  """

  __slots__ = ('generator', 'charCount', 'minCount')

  def __init__(self, *args) -> None:
    generator, charCount, minCount, *_ = [*args, None, None, None]
    self.generator = generator
    self.charCount = charCount
    self.minCount = minCount
    ValueError.__init__(self, )

  def __str__(self) -> str:
    infoSpec = """Generator '%s' requires a 'charCount' of at least %d
    characters, but received: %d!"""
    name = getattr(self.generator, '__name__', str(self.generator))
    info = infoSpec % (name, self.minCount, self.charCount)
    return textFmt(info, )

  __repr__ = __str__

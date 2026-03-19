"""
LoremChapterChild subclasses 'LoremChapter' and adds more inline components.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.markwork import InlineLorem

from ._lorem_chapter import LoremChapter, LoremSubSection, LoremSection

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Optional, Union


class LoremChapterChild(LoremChapter):
  """
  LoremChapterChild subclasses 'LoremChapter' and adds more inline
  components.
  """

  i4 = InlineLorem()
  i5 = InlineLorem()

  sub4 = LoremSubSection('You')
  sub5 = LoremSubSection('Up')

  sec3 = LoremSection('and')
  sec4 = LoremSection('never')

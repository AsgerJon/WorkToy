"""
LoremChapter subclasses 'Chapter' from the 'worktoy.markwork' module and
provides an example subclass with random contents.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.markwork import Chapter, InlineLorem
from . import LoremSection, LoremSubSection

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Optional, Union


class LoremChapter(Chapter):
  """
  LoremChapter subclasses 'Chapter' from the 'worktoy.markwork' module and
  provides an example subclass with random contents.
  """

  i1 = InlineLorem()
  i2 = InlineLorem()
  i3 = InlineLorem()

  sub1 = LoremSubSection('Never')
  sub2 = LoremSubSection('Gonna')
  sub3 = LoremSubSection('Give')

  sec1 = LoremSection('Together')
  sec2 = LoremSection('Forever')

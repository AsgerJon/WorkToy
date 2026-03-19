"""
LoremSubSection subclasses 'SubSection' and provides an example wit inline
instances of 'InlineLorem'.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.markwork import SubSection, InlineLorem

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Optional, Union


class LoremSubSection(SubSection):
  """
  LoremSubSection subclasses 'SubSection' and provides an example wit inline
  instances of 'InlineLorem'.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Public Variables
  i1 = InlineLorem()
  i2 = InlineLorem()
  i3 = InlineLorem()

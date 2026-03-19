"""
LoremSection subclasses 'Section' and provides an example with both inline
components of type 'InlineLorem' and block components of type
'LoremSubSection'.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from tests.test_markwork.examples import LoremSubSection
from worktoy.markwork import Section, InlineLorem

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Optional, Union


class LoremSection(Section):
  """
  LoremSection subclasses 'Section' and provides an example with both inline
  components of type 'InlineLorem' and block components of type
  'LoremSubSection'.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Public Variables
  i1 = InlineLorem()
  i2 = InlineLorem()
  i3 = InlineLorem()

  b1 = LoremSubSection('Never')
  b2 = LoremSubSection('Gonna')
  b3 = LoremSubSection('Give')

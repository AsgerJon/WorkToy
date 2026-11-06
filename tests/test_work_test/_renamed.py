"""
Renamed is an 'IntSampler' declaring the column count under one new name.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.work_test.samplers import IntSampler

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import TypeAlias

  KeyGroups: TypeAlias = dict[str, tuple[str, ...]]


class Renamed(IntSampler):
  """
  A subclass may redeclare the synonyms of a setting it inherits, and
  the nearest class answers for the setting. 'Renamed' declares the
  column count under 'cols' alone, so 'width' and 'size' are no longer
  keywords of it, while the bounds and the rest keep theirs.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  __key_groups__: KeyGroups = dict(colCount=('cols',))

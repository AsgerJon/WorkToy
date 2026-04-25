"""
TestPermIndexed subclasses 'UtilitiesTest' and tests the 'permIndexed'
function from the 'worktoy.utilities' package.

Written on April 25, 2026 after wasting three hours on copilot code
completion refusing to respond without any failure indication, with no
documentation or anything. By deleting the project locally and cloning it
again, somehow the issue was resolved.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.utilities import permTraced

from . import UtilitiesTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Union, Optional, Tuple, Iterator, Any


class TestPermIndexed(UtilitiesTest):
  """
  TestPermIndexed subclasses 'UtilitiesTest' and tests the 'permIndexed'
  function from the 'worktoy.utilities' package.

  Written on April 25, 2026 after wasting three hours on copilot code
  completion refusing to respond without any failure indication, with no
  documentation or anything. By deleting the project locally and cloning it
  again, somehow the issue was resolved.
  """

  @classmethod
  def factorial(cls, n: int) -> int:
    if n in [0, 1]:
      return 1
    return n * cls.factorial(n - 1)

  @classmethod
  def itemCounts(cls, *items) -> Iterator[tuple[Any, int]]:
    seen = []
    for item in items:
      if item not in seen:
        seen.append(item)
        yield (item, items.count(item))

  @classmethod
  def multinomialCoefficient(cls, *items) -> int:
    out = cls.factorial(len(items))
    for _, count in cls.itemCounts(*items):
      out //= cls.factorial(count)
    return out

  def test_sanity(self, ) -> None:
    """
    This method verifies that the 'permIndexed' finds the expected number
    of permutations.
    """
    
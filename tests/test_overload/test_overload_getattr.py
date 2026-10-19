"""
TestOverloadGetattr tests that 'overload.__getattr__' correctly falls back
to loaded function wherever possible.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.core.sentinels import ARGS
from worktoy.dispatch import overload
from . import OverloadTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Self


class TestOverloadGetattr(OverloadTest):
  """
  TestOverloadGetattr tests that 'overload.__getattr__' correctly falls back
  to loaded function wherever possible.
  """

  def test_overload_getattr(self) -> None:
    """Tests that 'overload.__getattr__' correctly falls back to loaded
    function."""

    def func() -> None:
      """
      Tracable docstring for the function.
      """
      pass

    actual = getattr(func, '__name__')
    loadOver = overload(int)
    loadFunc = loadOver(func)
    expected = getattr(loadFunc, '__name__')
    self.assertEqual(actual, expected)

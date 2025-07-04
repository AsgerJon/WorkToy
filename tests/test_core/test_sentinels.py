"""
TestSentinels performs edge case focused testing of the 'Sentinel' classes
provided by the 'worktoy.core.sentinels' module.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from typing import TYPE_CHECKING

from worktoy.core.sentinels._sentinel import _Sentinel  # NOQA

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Self


class TestSentinels(TestCase):
  """
  TestSentinels performs edge case focused testing of the 'Sentinel' classes
  provided by the 'worktoy.core.sentinels' module.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def tearDownClass(cls) -> None:
    import sys
    import gc
    sys.modules.pop(__name__, None)
    gc.collect()

  def test_recursion(self, ) -> None:
    """
    Tests the recursion protection
    """

    with self.assertRaises(KeyError) as context:
      _ = _Sentinel.__new__(_Sentinel, 'breh', (), {}, _recursion=True)
    e = context.exception
    self.assertEqual(str(e), str(KeyError('breh')))

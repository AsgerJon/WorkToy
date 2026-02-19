"""
TestSentinels performs edge case focused testing of the 'Sentinel' classes
provided by the 'worktoy.core.sentinels' module.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from . import CoreTest
from worktoy.core.sentinels import DESC, THIS, OWNER, METACALL, WILDCARD
from worktoy.core.sentinels import DELETED
from worktoy.core.sentinels._sentinel import _Sentinel  # NOQA

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestSentinels(CoreTest):
  """
  TestSentinels performs edge case focused testing of the 'Sentinel' classes
  provided by the 'worktoy.core.sentinels' module.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def setUp(self) -> None:
    self.sentinels = [
        THIS, OWNER, DESC, METACALL, WILDCARD, DELETED
    ]

  def test_recursion(self, ) -> None:
    """
    Tests the recursion protection
    """

    with self.assertRaises(KeyError) as context:
      _ = _Sentinel.__new__(_Sentinel, 'breh', (), {}, _recursion=True)
    e = context.exception
    self.assertEqual(str(e), str(KeyError('breh')))

  def test_str_repr(self) -> None:
    """
    Tests the string representation of a Sentinel
    """
    for sentinel in self.sentinels:
      self.assertEqual(str(sentinel), repr(sentinel))
      self.assertIsInstance(sentinel, _Sentinel)

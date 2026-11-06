"""
TestMarkers tests the five bare sentinels of 'worktoy.core.sentinels'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core.sentinels import Sentinel, SentinelMeta
from worktoy.core.sentinels import DELETED, OWNER, THIS, DESC, METACALL
from . import CoreTest


class TestMarkers(CoreTest):
  """
  'DELETED', 'OWNER', 'THIS', 'DESC' and 'METACALL' are the bare markers
  of the library, each a sentinel with a docstring and nothing else. The
  tests pin that each is a distinct sentinel of its own name, that no
  two are equal, and that each reads as a sentinel.
  """

  markers = (DELETED, OWNER, THIS, DESC, METACALL)

  def test_each_is_a_sentinel(self) -> None:
    for marker in self.markers:
      with self.subTest(marker=marker.__name__):
        self.assertIsInstance(marker, SentinelMeta)
        self.assertIsSubclass(marker, Sentinel)
        self.assertEqual(str(marker), "<Sentinel: '%s'>" % marker.__name__)

  def test_all_distinct(self) -> None:
    self.assertEqual(len(set(self.markers)), 5)
    for first in self.markers:
      for second in self.markers:
        with self.subTest(first=first.__name__, second=second.__name__):
          self.assertEqual(first == second, first is second)

  def test_names(self) -> None:
    names = [marker.__name__ for marker in self.markers]
    self.assertEqual(names, ['DELETED', 'OWNER', 'THIS', 'DESC', 'METACALL'])

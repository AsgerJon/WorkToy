"""
The 'TestMaybe' class provides unit tests for the 'worktoy.parse.maybe'
function.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from random import shuffle, random
from typing import TYPE_CHECKING

from . import UtilitiesTest
from worktoy.utilities import maybe

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias

  Bases: TypeAlias = tuple[type, ...]


class TestMaybe(UtilitiesTest):
  """
  TestMaybe tests the 'maybe' function from the 'worktoy.parse' module.
  """

  def setUp(self) -> None:
    """
    Sets up a list of falsy objects on an instance variable 'falsies'.
    """
    self.falsies = [
        False,
        0,
        0.0,
        0j,
        '',
        [],
        {},
        set(),
        frozenset(),
    ]
    self.typeFalsies = {
        bool     : False,
        int      : 0,
        float    : 0.0,
        complex  : 0j,
        str      : '',
        list     : [],
        dict     : {},
        set      : set(),
        frozenset: frozenset(),
    }
    self.typeTruthies = {
        bool     : True,
        int      : 1,
        float    : 0.1337,
        complex  : 0.80085j,
        str      : 'a',
        list     : [1],
        dict     : {'a': 1},
        set      : {1},
        frozenset: frozenset({1}),
    }

  @staticmethod
  def weave(a: list, b: list) -> list:
    """
    Weaves two lists of any length.
    """
    out = []
    a, b = [*reversed(a), ], [*reversed(b), ]
    while a or b:
      if not a:
        out.append(b.pop())
        continue
      if not b:
        out.append(a.pop())
        continue
      if random() < len(a) / (len(a) + len(b)):
        out.append(a.pop())
      else:
        out.append(b.pop())
    return [*out, ]

  def testMaybe(self, ) -> None:
    """
    Tests the 'maybe' function with various falsy objects.
    """
    for _ in range(100):
      falsies = [*self.falsies, ]
      shuffle(falsies)
      expected = falsies[0]
      testValues = self.weave(falsies, [None for _ in range(69)])
      self.assertIs(expected, maybe(*testValues), )

  def testEmpty(self) -> None:
    """
    Tests the 'maybe' function with an empty list.
    """
    self.assertIsNone(maybe(), )

  def testOnlyNone(self) -> None:
    """
    Tests the 'maybe' function with only None values.
    """
    self.assertIsNone(maybe(None, None, None), )

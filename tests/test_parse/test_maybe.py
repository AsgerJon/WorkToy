"""
The 'TestMaybe' class provides unit tests for the 'worktoy.parse.maybe'
function.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase
from random import shuffle, random
from typing import TYPE_CHECKING

from worktoy.mcls import AbstractMetaclass
from worktoy.mcls.space_hooks import ReservedNames
from worktoy.waitaminute import ReservedName, ReadOnlyError, ProtectedError
from worktoy.parse import maybe, maybeType, maybeTypes

from worktoy.waitaminute import _Attribute  # NOQA

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias

  Bases: TypeAlias = tuple[type, ...]


class TestMaybe(TestCase):
  """
  TestMaybe tests the 'maybe' function from the 'worktoy.parse' module.
  """

  @classmethod
  def tearDownClass(cls) -> None:
    import sys
    import gc
    sys.modules.pop(__name__, None)
    gc.collect()

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

  def testMaybeType(self) -> None:
    """
    Tests the 'maybeType' function with various falsy objects.
    """
    for _ in range(100):
      some = [*self.typeTruthies.values(), *self.typeFalsies.values(), ]
      shuffle(some)
      expected = some[0]
      testValues = self.weave(some, [None for _ in range(420)])
      expType = type(expected)
      if expected:
        expValue = self.typeTruthies.get(expType, )
      else:
        expValue = self.typeFalsies.get(expType, )
      actual = maybeType(expType, *testValues)
      self.assertEqual(expected, actual, )
      self.assertIsInstance(actual, expType, )

  def testMaybeTypes(self) -> None:
    """
    Tests the 'maybeTypes' function with various falsy objects.
    """
    for _ in range(2):
      some = []
      for _ in range(69):
        some.extend(self.typeTruthies.values())
        some.extend(self.typeFalsies.values())
      shuffle(some)
      testValues = self.weave(some, [None for _ in range(420)])
      for type_ in self.typeTruthies.keys():
        if type_ in [int, float, complex] and False:
          continue
        count = [1 if i else 0 for i in maybeTypes(type_, *testValues)]
        self.assertEqual(sum(count), 69 * (2 if type_ is int else 1))
        #  Cause bool is a subclass of int, so int has double the count

  def testEmpty(self) -> None:
    """
    Tests the 'maybe' function with an empty list.
    """
    self.assertIsNone(maybe(), )
    self.assertIsNone(maybeType(int), )
    self.assertIsNotNone(maybeTypes(int, ))  # cause empty list is not None

  def testOnlyNone(self) -> None:
    """
    Tests the 'maybe' function with only None values.
    """
    self.assertIsNone(maybe(None, None, None), )
    self.assertIsNone(maybeType(int, None, None), )
    self.assertFalse(maybeTypes(int, None, None), )

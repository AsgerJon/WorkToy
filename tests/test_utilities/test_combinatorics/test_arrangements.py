"""
TestArrangements provides tests for the 'Arrangements' class from
'worktoy.utilities.combinatorics'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from . import CombinatoricsTest
from worktoy.utilities.combinatorics import Arrangement, Arrangements

if TYPE_CHECKING:  # pragma: no cover
  # @formatter:off
  from typing import Any, Iterator, Optional

  class Arrangements:  # noqa
    __is_hashable__: Optional[bool]
    items: tuple[Any, ...]
    permutations: tuple[Arrangement, ...]
    def __init__(self, *items: Any) -> None: ...
    def __len__(self) -> int: ...
    def __iter__(self) -> Iterator[Arrangement]: ...
    def __getitem__(self, index: int) -> Arrangement: ...
    def __contains__(self, item: Any) -> bool: ...
    def isHashable(self, _recursion: bool = False) -> bool: ...
  # @formatter:on


class TestArrangements(CombinatoricsTest):
  """Tests for Arrangements(*items) - the deduplicated collection of
  unique value-orderings of a ground tuple."""

  #  ================================================================
  #  |
  #  |                         CONSTRUCTION
  #  ================================================================

  #  ________________________________________________________________
  #  Good construction
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_init_empty(self) -> None:
    """Arrangements() - zero items still admits exactly one
    arrangement (the empty one, by convention 0! = 1)."""
    a = Arrangements()
    self.assertEqual(a.items, ())
    self.assertEqual(len(a), 1)

  def test_init_single_item(self) -> None:
    a = Arrangements('A')
    self.assertEqual(a.items, ('A',))
    self.assertEqual(len(a), 1)

  def test_init_distinct_two(self) -> None:
    a = Arrangements('A', 'B')
    self.assertEqual(a.items, ('A', 'B'))
    self.assertEqual(len(a), 2)

  def test_init_distinct_three(self) -> None:
    a = Arrangements('A', 'B', 'C')
    self.assertEqual(a.items, ('A', 'B', 'C'))
    self.assertEqual(len(a), 6)

  def test_init_with_repeats(self) -> None:
    """Docstring promise: Arrangements('A','A','B') yields three
    arrangements, not six."""
    a = Arrangements('A', 'A', 'B')
    self.assertEqual(len(a), 3)

  def test_init_all_identical(self) -> None:
    a = Arrangements('A', 'A', 'A')
    self.assertEqual(len(a), 1)

  #  ================================================================
  #  |
  #  |                          PYTHON API
  #  ================================================================

  #  ________________________________________________________________
  #  Length
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_len_distinct_items_is_factorial(self) -> None:
    """For n distinct items, cardinality is n!."""
    for n in range(7):
      with self.subTest(n=n):
        a = Arrangements(*range(n))
        self.assertEqual(len(a), self.factorial(n))

  #  ________________________________________________________________
  #  Iteration
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_iter_yields_arrangement_instances(self) -> None:
    a = Arrangements('A', 'B', 'C')
    for x in a:
      self.assertIsInstance(x, Arrangement)

  def test_iter_count_matches_len(self) -> None:
    a = Arrangements('A', 'B', 'C', 'D')
    self.assertEqual(sum(1 for _ in a), len(a))

  #  ________________________________________________________________
  #  Indexing - good
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_getitem_returns_arrangement(self) -> None:
    a = Arrangements('A', 'B', 'C')
    self.assertIsInstance(a[0], Arrangement)

  def test_getitem_negative_index_resolves_from_end(self) -> None:
    a = Arrangements('A', 'B', 'C')
    self.assertIs(a[-1], a[len(a) - 1])

  #  ________________________________________________________________
  #  Indexing - out of range
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_getitem_out_of_range_raises(self) -> None:
    a = Arrangements('A', 'B', 'C')
    with self.assertRaises(IndexError):
      _ = a[len(a)]

  #  ________________________________________________________________
  #  Membership - good
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_contains_arrangement_with_matching_values(self) -> None:
    a = Arrangements('A', 'B', 'C')
    probe = Arrangement(('A', 'B', 'C'), (2, 0, 1))  # values = ('C','A','B')
    self.assertIn(probe, a)

  def test_contains_tuple_with_matching_values(self) -> None:
    a = Arrangements('A', 'B', 'C')
    self.assertIn(('C', 'A', 'B'), a)

  #  ________________________________________________________________
  #  Membership - non-matches
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_contains_arrangement_with_non_matching_values(self) -> None:
    a = Arrangements('A', 'B', 'C')
    probe = Arrangement(('x', 'y', 'Z'), (0, 1, 2))
    self.assertNotIn(probe, a)

  def test_contains_tuple_with_non_matching_values(self) -> None:
    a = Arrangements('A', 'B', 'C')
    self.assertNotIn(('x', 'y', 'Z'), a)

  def test_contains_unrelated_type_is_false(self) -> None:
    """Unlike Arrangement.__eq__, __contains__ returns plain False
    rather than NotImplemented for unrelated types."""
    a = Arrangements('A', 'B', 'C')
    self.assertFalse(a.__contains__(42))
    self.assertFalse(a.__contains__('AB'))
    self.assertFalse(a.__contains__(None))

  #  ================================================================
  #  |
  #  |                           GETTERS
  #  ================================================================

  #  ________________________________________________________________
  #  isHashable - detection
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_isHashable_true_when_all_items_hashable(self) -> None:
    """All items hashable, _createIsHashable's loop completes
    without break, falling into the for/else and assigning True."""
    a = Arrangements('A', 'B', 'C')
    self.assertTrue(a.isHashable())

  def test_isHashable_false_when_any_item_unhashable(self) -> None:
    """One unhashable item is enough, the break fires on the first
    such item, the for/else does not execute, and the method
    falls through to assigning False."""
    a = Arrangements('A', [1], 'C')
    self.assertFalse(a.isHashable())

  def test_isHashable_false_when_all_items_unhashable(self) -> None:
    a = Arrangements([1], [2], [3])
    self.assertFalse(a.isHashable())

  #  ________________________________________________________________
  #  isHashable - caching
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_isHashable_populates_cache_lazily(self) -> None:
    """isHashable() with __is_hashable__=None triggers detection
    and caches the result. The lazy-init branch normally fires
    during __init__; reset and re-call to pin it explicitly."""
    a = Arrangements('A', 'B')
    a.__is_hashable__ = None
    a.isHashable()
    self.assertIsNotNone(a.__is_hashable__)

  def test_isHashable_returns_cached_value_without_recomputing(self) -> None:
    """Items are genuinely hashable, but the cache is poisoned with
    False. isHashable() must trust the cache and return False,
    proving it short-circuits without re-running detection."""
    a = Arrangements('A', 'B')
    a.__is_hashable__ = False
    self.assertFalse(a.isHashable())

  #  ________________________________________________________________
  #  isHashable - peek API
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_isHashable_raises_recursion_error_with_unset_cache(self) -> None:
    """The recursion guard is load-bearing for the peek API:
    'try: x.isHashable(_recursion=True) except RecursionError:'
    lets a caller observe whether detection has run, without
    forcing it. This pins the RecursionError contract that the
    peek pattern depends on."""
    a = Arrangements('A', 'B')
    a.__is_hashable__ = None
    with self.assertRaises(RecursionError):
      a.isHashable(_recursion=True)

  def test_isHashable_peek_returns_cached_value_when_set(self) -> None:
    """Peek with a populated cache: '_recursion=True' is ignored
    because the first 'if' falls through. Pins the other arm of
    the peek API."""
    a = Arrangements('A', 'B')  # __init__ populates the cache
    self.assertTrue(a.isHashable(_recursion=True))

  #  ================================================================
  #  |
  #  |                        FUNCTIONALITY
  #  |              ( the actual point of the class )
  #  ================================================================

  #  ________________________________________________________________
  #  Multiset cardinality
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_multiset_AABB_matches_multinomial(self) -> None:
    """('A','A','B','B') has 4! / (2! · 2!) = 6 unique arrangements."""
    a = Arrangements('A', 'A', 'B', 'B')
    expected = self.factorial(4) // (self.factorial(2) * self.factorial(2))
    self.assertEqual(len(a), expected)

  def test_multiset_AAABB_matches_multinomial(self) -> None:
    """('A','A','A','B','B') has 5! / (3! · 2!) = 10 unique arrangements."""
    a = Arrangements('A', 'A', 'A', 'B', 'B')
    expected = self.factorial(5) // (self.factorial(3) * self.factorial(2))
    self.assertEqual(len(a), expected)

  def test_AAB_yields_exactly_the_three_expected_orderings(self) -> None:
    """Pin the docstring example exactly."""
    a = Arrangements('A', 'A', 'B')
    actual = {tuple(x.values) for x in a}
    expected = {('A', 'A', 'B'), ('A', 'B', 'A'), ('B', 'A', 'A')}
    self.assertEqual(actual, expected)

  #  ________________________________________________________________
  #  Uniqueness of arranged values
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_no_two_arrangements_share_a_values_tuple(self) -> None:
    """The dedup contract: every cached arrangement has a unique
    values tuple, regardless of repeats in the ground items."""
    cases = [
      ('A', 'B', 'C', 'D'),
      ('A', 'A', 'B', 'C'),
      ('A', 'A', 'B', 'B'),
      ('x',) * 4
    ]
    for items in cases:
      with self.subTest(items=items):
        a = Arrangements(*items)
        seen = [x.values for x in a]
        self.assertEqual(len(seen), len(set(seen)))

  #  ________________________________________________________________
  #  Unhashable items - equality-list fallback
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_unhashable_distinct_yields_factorial(self) -> None:
    """Distinct unhashable items: every arrangement routes through
    'TypeError → seen_eq miss → append'. Exercises branch D in
    isolation (no skips)."""
    a = Arrangements([1], [2], [3])
    self.assertEqual(len(a), self.factorial(3))

  def test_unhashable_with_duplicates_dedup(self) -> None:
    """Two equal lists in the ground tuple collapse to multiset
    cardinality. Exercises both unhashable branches: branch D
    ('TypeError → seen_eq miss → append', firing 3 times) and
    branch C ('TypeError → seen_eq hit → skip', firing 3 times)."""
    a = Arrangements([1], [1], [2])
    self.assertEqual(len(a), 3)

  def test_unhashable_specific_values_pinned(self) -> None:
    """Pin the value tuples produced for unhashable duplicates.
    Mirrors the AAB hashable case to make the parallel obvious."""
    a = Arrangements([1], [1], [2])
    produced = [x.values for x in a]
    self.assertEqual(len(produced), 3)
    for expected in [
      ([1], [1], [2]),
      ([1], [2], [1]),
      ([2], [1], [1])
    ]:
      self.assertIn(expected, produced)

  #  ________________________________________________________________
  #  Wrapped Arrangements preserve the ground items
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_each_arrangement_carries_ground_items(self) -> None:
    a = Arrangements('A', 'B', 'C')
    for x in a:
      self.assertEqual(x.items, ('A', 'B', 'C'))

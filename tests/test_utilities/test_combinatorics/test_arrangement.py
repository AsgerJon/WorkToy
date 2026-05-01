"""
TestArrangement provides tests for the 'Arrangement' class from
'worktoy.utilities.combinatorics'.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING
from unittest import TestCase

from worktoy.utilities.combinatorics import Arrangement

if TYPE_CHECKING:  # pragma: no cover
  # @formatter:off
  from typing import Any

  class Arrangement:  # noqa
    items: tuple[Any, ...]
    forward: tuple[int, ...]
    inverse: tuple[int, ...]
    values: tuple[Any, ...]
    def __init__(
        self, items: tuple[Any, ...], forward: tuple[int, ...]
    ) -> None: ...
    def applyTo(self, *values: Any) -> tuple[Any, ...]: ...
    def restoreFrom(self, *values: Any) -> tuple[Any, ...]: ...
    def __len__(self) -> int: ...
    def __eq__(self, other: Any) -> bool: ...
    def __hash__(self) -> int: ...
  # @formatter:on


class TestArrangement(TestCase):
  """Tests for Arrangement(items, forward) — one permutation of a
  ground tuple, with a forward/inverse index pair."""

  #  ================================================================
  #  |
  #  |                         CONSTRUCTION
  #  ================================================================

  #  ________________________________________________________________
  #  Good construction
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_init_basic(self) -> None:
    a = Arrangement(('A', 'B', 'C'), (2, 0, 1))
    self.assertEqual(a.items, ('A', 'B', 'C'))
    self.assertEqual(a.forward, (2, 0, 1))
    self.assertEqual(a.values, ('C', 'A', 'B'))

  def test_init_inverse_on_three_cycle(self) -> None:
    """A 3-cycle is the smallest non-involution and the canonical case
    where confusing forward with inverse fails. Pin both recipes."""
    a = Arrangement(('A', 'B', 'C'), (1, 2, 0))
    self.assertEqual(a.forward, (1, 2, 0))
    self.assertEqual(a.inverse, (2, 0, 1))

  def test_init_satisfies_forward_contract(self) -> None:
    """Class docstring: 'self.values[k] is self.items[self.forward[k]]'."""
    a = Arrangement(('A', 'B', 'C', 'D'), (3, 1, 0, 2))
    for k in range(len(a)):
      self.assertIs(a.values[k], a.items[a.forward[k]])

  def test_init_satisfies_inverse_contract(self) -> None:
    """Class docstring: 'self.values[self.inverse[k]] is self.items[k]'."""
    a = Arrangement(('A', 'B', 'C', 'D'), (3, 1, 0, 2))
    for k in range(len(a)):
      self.assertIs(a.values[a.inverse[k]], a.items[k])

  def test_init_identity(self) -> None:
    a = Arrangement(('A', 'B', 'C'), (0, 1, 2))
    self.assertEqual(a.values, a.items)
    self.assertEqual(a.forward, a.inverse)

  def test_init_empty(self) -> None:
    a = Arrangement((), ())
    self.assertEqual(a.items, ())
    self.assertEqual(a.forward, ())
    self.assertEqual(a.inverse, ())
    self.assertEqual(a.values, ())

  def test_init_singleton(self) -> None:
    a = Arrangement(('A',), (0,))
    self.assertEqual(a.values, ('A',))
    self.assertEqual(a.inverse, (0,))

  #  ________________________________________________________________
  #  Bad construction — length mismatch
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_init_rejects_forward_too_long(self) -> None:
    with self.assertRaises(ValueError):
      Arrangement(('A', 'B'), (0, 1, 2))

  def test_init_rejects_forward_too_short(self) -> None:
    with self.assertRaises(ValueError):
      Arrangement(('A', 'B', 'C'), (0, 1))

  def test_init_rejects_empty_forward_with_nonempty_items(self) -> None:
    with self.assertRaises(ValueError):
      Arrangement(('A', 'B'), ())

  #  ================================================================
  #  |
  #  |                          PYTHON API
  #  ================================================================

  #  ________________________________________________________________
  #  Length and iteration
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_len(self) -> None:
    a = Arrangement(('A', 'B', 'C'), (2, 0, 1))
    self.assertEqual(len(a), 3)

  def test_len_empty(self) -> None:
    self.assertEqual(len(Arrangement((), ())), 0)

  def test_iter_yields_values_not_items(self) -> None:
    a = Arrangement(('A', 'B', 'C'), (2, 0, 1))
    self.assertEqual(tuple(a), ('C', 'A', 'B'))

  def test_iter_empty(self) -> None:
    self.assertEqual(list(Arrangement((), ())), [])

  #  ________________________________________________________________
  #  Equality — good
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_eq_arrangement_same_values(self) -> None:
    a = Arrangement(('A', 'B', 'C'), (2, 0, 1))
    b = Arrangement(('A', 'B', 'C'), (2, 0, 1))
    self.assertEqual(a, b)

  def test_eq_arrangement_same_values_different_construction(self) -> None:
    """Equality is by values; the items/forward pair is incidental."""
    a = Arrangement(('A', 'B'), (1, 0))  # values = ('B', 'A')
    b = Arrangement(('B', 'A'), (0, 1))  # values = ('B', 'A')
    self.assertEqual(a, b)

  def test_eq_with_tuple(self) -> None:
    a = Arrangement(('A', 'B', 'C'), (2, 0, 1))
    self.assertEqual(a, ('C', 'A', 'B'))

  def test_neq_different_values(self) -> None:
    a = Arrangement(('A', 'B', 'C'), (2, 0, 1))
    b = Arrangement(('A', 'B', 'C'), (1, 2, 0))
    self.assertNotEqual(a, b)

  #  ________________________________________________________________
  #  Equality — verifying 'NotImplemented' return value
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_eq_returns_not_implemented_for_unrelated_types(self) -> None:
    a = Arrangement(('A', 'B'), (0, 1))
    self.assertIs(a.__eq__(42), NotImplemented)
    self.assertIs(a.__eq__('AB'), NotImplemented)
    self.assertIs(a.__eq__(None), NotImplemented)

  #  ________________________________________________________________
  #  Hashing
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_hash_equal_arrangements_hash_equally(self) -> None:
    a = Arrangement(('A', 'B', 'C'), (2, 0, 1))
    b = Arrangement(('A', 'B', 'C'), (2, 0, 1))
    self.assertEqual(hash(a), hash(b))

  def test_hash_set_dedupes_by_values(self) -> None:
    a = Arrangement(('A', 'B', 'C'), (2, 0, 1))
    b = Arrangement(('A', 'B', 'C'), (2, 0, 1))  # equal to a
    c = Arrangement(('A', 'B', 'C'), (1, 2, 0))  # different values
    self.assertEqual(len({a, b, c}), 2)

  #  ________________________________________________________________
  #  String representation
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_str_shows_values(self) -> None:
    a = Arrangement(('A', 'B', 'C'), (2, 0, 1))
    self.assertEqual(str(a), '<Arrangement: C, A, B>')

  def test_repr_shows_items_and_forward(self) -> None:
    a = Arrangement(('A', 'B', 'C'), (2, 0, 1))
    self.assertEqual(repr(a), 'Arrangement(A, B, C, 2, 0, 1)')

  #  ================================================================
  #  |
  #  |                        FUNCTIONALITY
  #  |              ( the actual point of the class )
  #  ================================================================

  #  ________________________________________________________________
  #  applyTo — canonical to arranged
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_apply_to_identity(self) -> None:
    a = Arrangement(('A', 'B', 'C'), (0, 1, 2))
    self.assertEqual(a.applyTo('a', 'b', 'c'), ('a', 'b', 'c'))

  def test_apply_to_three_cycle(self) -> None:
    """A 3-cycle round-trip is the regression guard from the class
    docstring: forward/inverse swaps are silent on involutions."""
    a = Arrangement(('A', 'B', 'C'), (1, 2, 0))  # values = ('B','C','A')
    #  Caller passes parallel data in items order; expects values order.
    self.assertEqual(a.applyTo('a', 'b', 'c'), ('b', 'c', 'a'))

  def test_apply_to_rejects_too_few_values(self) -> None:
    a = Arrangement(('A', 'B', 'C'), (2, 0, 1))
    with self.assertRaises(ValueError):
      a.applyTo('a', 'b')

  def test_apply_to_rejects_too_many_values(self) -> None:
    a = Arrangement(('A', 'B', 'C'), (2, 0, 1))
    with self.assertRaises(ValueError):
      a.applyTo('a', 'b', 'c', 'd')

  #  ________________________________________________________________
  #  restoreFrom — arranged to canonical
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_restore_from_identity(self) -> None:
    a = Arrangement(('A', 'B', 'C'), (0, 1, 2))
    self.assertEqual(a.restoreFrom('a', 'b', 'c'), ('a', 'b', 'c'))

  def test_restore_from_three_cycle(self) -> None:
    a = Arrangement(('A', 'B', 'C'), (1, 2, 0))  # values = ('B','C','A')
    #  Caller passes parallel data in values order; expects items order.
    self.assertEqual(a.restoreFrom('b', 'c', 'a'), ('a', 'b', 'c'))

  def test_restore_from_rejects_wrong_arity(self) -> None:
    a = Arrangement(('A', 'B', 'C'), (2, 0, 1))
    with self.assertRaises(ValueError):
      a.restoreFrom('a', 'b')

  #  ________________________________________________________________
  #  Round-trip — applyTo and restoreFrom are inverses
  #  ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨

  def test_round_trip_apply_then_restore(self) -> None:
    """For every forward, restoreFrom(*applyTo(*v)) == v."""
    forwards = [(0, 1, 2), (1, 0, 2), (2, 1, 0),  # involutions
                (1, 2, 0), (2, 0, 1)]  # 3-cycles
    for forward in forwards:
      with self.subTest(forward=forward):
        a = Arrangement(('A', 'B', 'C'), forward)
        self.assertEqual(
          a.restoreFrom(*a.applyTo('a', 'b', 'c')),
          ('a', 'b', 'c'),
        )

  def test_round_trip_restore_then_apply(self) -> None:
    forwards = [(0, 1, 2), (1, 0, 2), (2, 1, 0),
                (1, 2, 0), (2, 0, 1)]
    for forward in forwards:
      with self.subTest(forward=forward):
        a = Arrangement(('A', 'B', 'C'), forward)
        self.assertEqual(
          a.applyTo(*a.restoreFrom('a', 'b', 'c')),
          ('a', 'b', 'c'),
        )

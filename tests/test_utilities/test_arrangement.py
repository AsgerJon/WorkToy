"""
TestArrangement tests 'Arrangement' from 'worktoy.utilities.combinatorics'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.utilities.combinatorics import Arrangement
from worktoy.work_test.samplers import IntSampler
from . import UtilitiesTest


class TestArrangement(UtilitiesTest):
  """
  'Arrangement' is one ordering of a ground tuple, holding the recipe
  that produces it and the recipe that undoes it, with 'applyTo' and
  'restoreFrom' so that a caller never has to pick between the two.
  The tests pin the two invariants of the recipes on a 3-cycle, where
  the two recipes differ, the round trip of the two methods, the
  refusals of the constructor and the methods, and the Python API.
  """

  @staticmethod
  def _cycle() -> Arrangement:
    """The 3-cycle whose forward and inverse recipes differ."""
    return Arrangement(('a', 'b', 'c'), (2, 0, 1))

  def test_values_and_recipes(self) -> None:
    arrangement = self._cycle()
    self.assertEqual(arrangement.items, ('a', 'b', 'c'))
    self.assertEqual(arrangement.forward, (2, 0, 1))
    self.assertEqual(arrangement.inverse, (1, 2, 0))
    self.assertEqual(arrangement.values, ('c', 'a', 'b'))

  def test_recipe_invariants(self) -> None:
    arrangement = self._cycle()
    for k in range(3):
      with self.subTest(k=k):
        self.assertIs(arrangement.values[k],
                      arrangement.items[arrangement.forward[k]])
        self.assertIs(arrangement.values[arrangement.inverse[k]],
                      arrangement.items[k])

  def test_apply_and_restore(self) -> None:
    arrangement = self._cycle()
    self.assertEqual(arrangement.applyTo(1, 2, 3), (3, 1, 2))
    self.assertEqual(arrangement.restoreFrom(3, 1, 2), (1, 2, 3))
    applied = arrangement.applyTo('x', 'y', 'z')
    self.assertEqual(arrangement.restoreFrom(*applied), ('x', 'y', 'z'))
    self.assertEqual(arrangement.applyTo(*arrangement.items),
                     arrangement.values)

  def test_apply_and_restore_refuse_wrong_count(self) -> None:
    arrangement = self._cycle()
    for count in (2, 4):
      values = (*range(count),)
      with self.subTest(count=count):
        with self.assertRaises(ValueError) as context:
          arrangement.applyTo(*values)
        self.assertIn("'applyTo' received '%d' values" % count,
                      str(context.exception))
        with self.assertRaises(ValueError) as context:
          arrangement.restoreFrom(*values)
        self.assertIn("'restoreFrom' received '%d' values" % count,
                      str(context.exception))

  def test_length_mismatch_refused(self) -> None:
    with self.assertRaises(ValueError) as context:
      Arrangement(('a', 'b'), (0, 1, 2))
    self.assertIn("length '3' does not match", str(context.exception))
    self.assertIn("length '2'", str(context.exception))
    with self.assertRaises(ValueError) as context:
      Arrangement(('a', 'b', 'c'), (0, 1))
    self.assertIn("length '2' does not match", str(context.exception))
    self.assertIn("length '3'", str(context.exception))

  def test_not_a_permutation_refused(self) -> None:
    with self.assertRaises(ValueError) as context:
      Arrangement(('a', 'b', 'c'), (0, 0, 1))
    self.assertIn('(0, 0, 1) is not a permutation', str(context.exception))
    self.assertIn('positions 0 to 2', str(context.exception))
    with self.assertRaises(ValueError) as context:
      Arrangement(('a', 'b'), (1, 2))
    self.assertIn('positions 0 to 1', str(context.exception))

  def test_empty(self) -> None:
    arrangement = Arrangement((), ())
    self.assertEqual(len(arrangement), 0)
    self.assertEqual(arrangement.values, ())
    self.assertEqual(arrangement.applyTo(), ())

  def test_len_and_iter(self) -> None:
    arrangement = self._cycle()
    self.assertEqual(len(arrangement), 3)
    self.assertEqual([*arrangement], ['c', 'a', 'b'])

  def test_equality(self) -> None:
    arrangement = self._cycle()
    self.assertEqual(arrangement, Arrangement(('a', 'b', 'c'), (2, 0, 1)))
    self.assertEqual(arrangement, Arrangement(('c', 'a', 'b'), (0, 1, 2)))
    self.assertNotEqual(arrangement, Arrangement(('a', 'b', 'c'), (0, 1, 2)))
    self.assertNotEqual(Arrangement(('a', 'b', 'c'), (0, 1, 2)), arrangement)
    self.assertEqual(arrangement, ('c', 'a', 'b'))
    self.assertNotEqual(arrangement, ('a', 'b', 'c'))
    self.assertNotEqual(arrangement, ('d', 'a', 'b'))
    self.assertIs(arrangement.__eq__(['c', 'a', 'b']), NotImplemented)
    self.assertFalse(arrangement == ['c', 'a', 'b'])
    self.assertTrue(arrangement != 5)

  def test_hash_follows_values(self) -> None:
    arrangement = self._cycle()
    self.assertEqual(hash(arrangement), hash(('c', 'a', 'b')))
    self.assertEqual(hash(arrangement),
                     hash(Arrangement(('c', 'a', 'b'), (0, 1, 2))))
    self.assertEqual(len({arrangement, self._cycle()}), 1)

  def test_str(self) -> None:
    self.assertEqual(str(self._cycle()), '<Arrangement: c, a, b>')
    self.assertEqual(str(Arrangement((1, 2), (1, 0))), '<Arrangement: 2, 1>')

  def test_repr_is_the_constructing_call(self) -> None:
    arrangement = self._cycle()
    self.assertEqual(repr(arrangement),
                     "Arrangement(('a', 'b', 'c'), (2, 0, 1))")
    rebuilt = Arrangement(('a', 'b', 'c'), (2, 0, 1))
    self.assertEqual(rebuilt.items, arrangement.items)
    self.assertEqual(rebuilt.forward, arrangement.forward)
    self.assertEqual(repr(rebuilt), repr(arrangement))

  def test_random_recipes(self) -> None:
    self.randomInteger = IntSampler(0, 99, seed=17)
    for n in range(2, 7):
      forward = [*range(n)]
      self.randomInteger.random.shuffle(forward)
      items = (*('item%d' % i for i in range(n)),)
      arrangement = Arrangement(items, (*forward,))
      self.randomInteger.size = n
      values = self.randomInteger.row
      with self.subTest(n=n, forward=forward):
        self.assertEqual(sorted(arrangement.inverse), [*range(n)])
        applied = arrangement.applyTo(*values)
        restored = arrangement.restoreFrom(*values)
        self.assertEqual(arrangement.restoreFrom(*applied), values)
        self.assertEqual(arrangement.applyTo(*restored), values)
        for k in range(n):
          self.assertIs(arrangement.values[k], items[arrangement.forward[k]])
          self.assertIs(arrangement.values[arrangement.inverse[k]], items[k])

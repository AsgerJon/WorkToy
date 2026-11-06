"""
TestPermuter tests 'Permuter' from 'worktoy.dispatch'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from types import FunctionType

from worktoy.dispatch import Permuter
from worktoy.utilities.combinatorics import Arrangement
from worktoy.waitaminute import TypeException, MissingVariable
from worktoy.waitaminute.desc import WriteOnceError
from . import DispatchTest


def _triple(a: str, b: str, c: str) -> tuple:
  return a, b, c


class TestPermuter(DispatchTest):
  """
  A flexible overload accepts its arguments in any order, so each order
  needs a callable that puts them back in the declared order before the
  call. 'Permuter' holds a function and an 'Arrangement' for that. The
  tests pin the reordering, the constructor in every shape it accepts and
  its refusals, the write-once arrangement, and the three operators.
  """

  @staticmethod
  def _cycle() -> Arrangement:
    """The caller gives c, a, b; the function wants a, b, c."""
    return Arrangement(('a', 'b', 'c'), (2, 0, 1))

  def test_reorders(self) -> None:
    permuter = Permuter(_triple, self._cycle())
    self.assertEqual(permuter('C', 'A', 'B'), ('A', 'B', 'C'))
    self.assertIs(permuter.__wrapped__, _triple)
    self.assertEqual(permuter.arrangement, self._cycle())

  def test_keywords_pass(self) -> None:
    def labelled(a: str, b: str, c: str, **kw) -> tuple:
      return (a, b, c, kw)

    permuter = Permuter(labelled, self._cycle())
    self.assertEqual(permuter('C', 'A', 'B', k=1), ('A', 'B', 'C', {'k': 1}))

  def test_wrong_count_refused(self) -> None:
    permuter = Permuter(_triple, self._cycle())
    with self.assertRaises(ValueError) as context:
      permuter('A', 'B')
    self.assertIn("'restoreFrom' received '2' values",
                  str(context.exception))

  def test_constructor_shapes(self) -> None:
    arrangement = self._cycle()
    self.assertIsNone(Permuter().__function_case__)
    self.assertIs(Permuter(_triple).__wrapped__, _triple)
    self.assertIs(Permuter(arrangement).arrangement, arrangement)
    both = Permuter(_triple, arrangement)
    self.assertIs(both.arrangement, arrangement)
    swapped = Permuter(arrangement, _triple)
    self.assertIs(swapped.__wrapped__, _triple)
    self.assertIs(swapped.arrangement, arrangement)

  def test_constructor_refusals(self) -> None:
    arrangement = self._cycle()
    with self.assertRaises(ValueError) as context:
      Permuter(_triple, arrangement, _triple)
    self.assertIn("at most two positional arguments, but received '3'",
                  str(context.exception))
    with self.assertRaises(ValueError) as context:
      Permuter(arrangement, arrangement)
    self.assertIn("at most one 'Arrangement'", str(context.exception))
    with self.assertRaises(ValueError) as context:
      Permuter(_triple, _triple)
    self.assertIn("at most one 'FunctionType'", str(context.exception))
    with self.assertRaises(TypeException) as context:
      Permuter(5)
    self.assertEqual(context.exception.varName, 'arg')
    self.assertEqual(context.exception.actualObject, 5)
    self.assertIs(context.exception.actualType, int)
    self.assertEqual(context.exception.expectedTypes,
                     (Arrangement, FunctionType))
    self.assertIn("'Arrangement' or 'function'", str(context.exception))

  def test_missing_pieces(self) -> None:
    with self.assertRaises(MissingVariable) as context:
      Permuter(_triple)('A', 'B', 'C')
    self.assertEqual(context.exception.varName, '__arg_arrangement__')
    self.assertIsInstance(context.exception.instance, Permuter)
    self.assertEqual(context.exception.expectedTypes, (Arrangement,))
    self.assertIn("'Permuter.__arg_arrangement__: Arrangement'",
                  str(context.exception))
    with self.assertRaises(MissingVariable) as context:
      Permuter(self._cycle())('A', 'B', 'C')
    self.assertEqual(context.exception.varName, '__function_case__')
    self.assertIsInstance(context.exception.instance, Permuter)
    self.assertIn("'Permuter.__function_case__", str(context.exception))

  def test_arrangement_set_once(self) -> None:
    permuter = Permuter(_triple)
    with self.assertRaises(TypeException) as context:
      permuter.setArrangement(5)
    self.assertEqual(context.exception.varName, 'arrangement')
    self.assertEqual(context.exception.actualObject, 5)
    self.assertIs(context.exception.actualType, int)
    self.assertEqual(context.exception.expectedTypes, (Arrangement,))
    self.assertIn("'arrangement'", str(context.exception))
    permuter.setArrangement(self._cycle())
    with self.assertRaises(WriteOnceError) as context:
      permuter.setArrangement(self._cycle())
    self.assertIs(context.exception.desc, permuter)
    self.assertEqual(context.exception.oldValue, self._cycle())
    self.assertEqual(context.exception.newValue, self._cycle())
    self.assertIn('write-once', str(context.exception))

  def test_operators(self) -> None:
    arrangement = self._cycle()
    bare = Permuter(_triple)
    shifted = bare << arrangement
    self.assertIsInstance(shifted, Permuter)
    self.assertIsNot(shifted, bare)
    self.assertIs(shifted.__wrapped__, _triple)
    self.assertIs(shifted.arrangement, arrangement)
    self.assertIsNone(bare.__arg_arrangement__)
    rshifted = arrangement >> bare
    self.assertIs(rshifted.arrangement, arrangement)
    self.assertIsNot(rshifted, bare)
    inplace = bare
    inplace <<= arrangement
    self.assertIs(inplace, bare)
    self.assertIs(bare.arrangement, arrangement)
    self.assertIs(bare.__lshift__(5), NotImplemented)
    self.assertIs(bare.__ilshift__(5), NotImplemented)
    with self.assertRaises(TypeError):
      _ = bare << 5

  def test_new_arrangement_keeps_class(self) -> None:
    class Sub(Permuter):
      pass

    original = Sub(_triple)
    renewed = Sub.newArrangement(original, self._cycle())
    self.assertIsInstance(renewed, Sub)
    self.assertEqual(renewed('C', 'A', 'B'), ('A', 'B', 'C'))

  def test_random_orders(self) -> None:
    for n in range(2, 5):
      forward = [*range(n)]
      self.randomInteger.random.shuffle(forward)
      arrangement = Arrangement((*range(n),), (*forward,))
      self.randomWord.size = n
      words = self.randomWord.row
      permuter = Permuter(lambda *a: a, arrangement)
      with self.subTest(forward=forward):
        self.assertEqual(permuter(*arrangement.applyTo(*words)), words)

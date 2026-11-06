"""
TestFlexCall tests 'flexCall' and 'isFlex' from 'worktoy.dispatch'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from types import FunctionType

from worktoy.dispatch import flexCall, isFlex
from worktoy.dispatch._flex_call import _missingNames
from worktoy.waitaminute import TypeException
from . import DispatchTest


def _pair(a: int, b: int, c: int = 3) -> tuple:
  """Three parameters, the last with a default."""
  return a, b, c


class TestFlexCall(DispatchTest):
  """
  A callback receives the same arguments however few it declares, so
  'flexCall' wraps a function to drop surplus positional arguments while
  still failing clearly for a missing required one. The tests pin the
  wrapper's cut, its refusal naming the missing parameters, a required
  parameter given by keyword, the functions left as they are, the
  refusal of anything that is no plain function, and that the wrapper
  looks like the function.
  """

  def test_is_flex(self) -> None:
    class Answering:
      def __getattr__(self, key: str) -> None:
        """Answers every name with 'None' rather than refusing it."""

    self.assertFalse(isFlex(_pair))
    self.assertTrue(isFlex(flexCall(_pair)))
    self.assertFalse(isFlex(Answering()))

  def test_not_a_function_refused(self) -> None:
    for value in (print, self.test_is_flex, staticmethod(_pair), 5):
      with self.subTest(value=value):
        with self.assertRaises(TypeException) as context:
          flexCall(value)
        self.assertEqual(context.exception.varName, 'func')
        self.assertIs(context.exception.actualObject, value)
        self.assertIs(context.exception.actualType, type(value))
        self.assertEqual(context.exception.expectedTypes, (FunctionType,))
        self.assertIn("'function'", str(context.exception))

  def test_wrapping_twice_gives_same_wrapper(self) -> None:
    wrapper = flexCall(_pair)
    self.assertIs(flexCall(wrapper), wrapper)

  def test_varargs_function_untouched(self) -> None:
    def gather(*args: int) -> tuple:
      return args

    self.assertIs(flexCall(gather), gather)
    self.assertEqual(gather(1, 2), (1, 2))

  def test_dunder_untouched(self) -> None:
    def __call__(self) -> None:
      """A dunder the interpreter calls with fixed arguments."""

    self.assertIs(flexCall(__call__), __call__)

  def test_surplus_cut(self) -> None:
    wrapper = flexCall(_pair)
    self.assertEqual(wrapper(1, 2, 3, 4, 5), (1, 2, 3))
    self.assertEqual(wrapper(1, 2), (1, 2, 3))

  def test_missing_required_refused(self) -> None:
    wrapper = flexCall(_pair)
    with self.assertRaises(TypeError) as context:
      wrapper(1)
    message = str(context.exception)
    self.assertIn("'_pair' requires at least '2'", message)
    self.assertIn("received only '1'", message)
    self.assertIn('(b)', message)
    with self.assertRaises(TypeError) as context:
      wrapper()
    self.assertIn('(a and b)', str(context.exception))

  def test_required_given_by_keyword(self) -> None:
    wrapper = flexCall(_pair)
    self.assertEqual(wrapper(1, b=2), (1, 2, 3))
    self.assertEqual(wrapper(a=1, b=2, c=4), (1, 2, 4))

  def test_keywords_pass(self) -> None:
    self.assertEqual(flexCall(_pair)(1, 2, c=9), (1, 2, 9))

  def test_wrapper_looks_like_function(self) -> None:
    wrapper = flexCall(_pair)
    self.assertEqual(wrapper.__name__, '_pair')
    self.assertEqual(wrapper.__doc__, _pair.__doc__)
    self.assertIs(wrapper.__wrapped__, _pair)
    self.assertIsInstance(wrapper, FunctionType)

  def test_missing_names(self) -> None:
    self.assertEqual(_missingNames(('a', 'b', 'c'), 1, {'c': 1}), ('b',))
    self.assertEqual(_missingNames(('a', 'b'), 0, {}), ('a', 'b'))
    self.assertEqual(_missingNames(('a', 'b'), 2, {}), ())

  def test_random_surplus(self) -> None:
    wrapper = flexCall(_pair)
    self.randomInteger.size = 6
    for _ in range(5):
      row = self.randomInteger.row
      with self.subTest(row=row):
        self.assertEqual(wrapper(*row), row[:3])

  def test_private_names_still_wrapped(self) -> None:
    def __private(a: int, b: int) -> tuple:
      return a, b

    def trailing__(a: int) -> int:
      return a

    self.assertTrue(isFlex(flexCall(__private)))
    self.assertEqual(flexCall(__private)(1, 2, 3), (1, 2))
    self.assertTrue(isFlex(flexCall(trailing__)))
    self.assertEqual(flexCall(trailing__)(5, 6), 5)

  def test_one_default(self) -> None:
    def one(a: int, b: int = 2) -> tuple:
      return a, b

    wrapper = flexCall(one)
    self.assertEqual(wrapper(1), (1, 2))
    self.assertEqual(wrapper(1, 3, 4), (1, 3))
    with self.assertRaises(TypeError) as context:
      wrapper()
    self.assertIn("'one' requires at least '1'", str(context.exception))

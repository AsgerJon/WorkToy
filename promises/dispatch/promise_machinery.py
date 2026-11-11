"""
PromiseMachinery promises the building blocks of 'worktoy.dispatch' a
project may use on their own: 'flexCall', 'isFlex', 'TypeSig',
'CallMeMaybe', 'Permuter' and 'Dispatcher'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.dispatch import flexCall, isFlex, TypeSig, CallMeMaybe
from worktoy.dispatch import Permuter, Dispatcher, overload
from worktoy.mcls import BaseObject
from worktoy.utilities.combinatorics import Arrangement
from worktoy.waitaminute import TypeException


class PromiseMachinery(TestCase):
  """
  'flexCall(func)' wraps a plain function so it drops surplus positional
  arguments, still raising 'TypeError' for a missing required one, and
  still carrying the name and '__wrapped__' of the function; 'isFlex'
  tells a wrapper from a plain function, and anything but a plain
  function raises 'TypeException'. A 'TypeSig' is the classes of a call
  in order: equal and hashing alike for the same classes, different for
  another order, with 'len', iteration and 'in', and 'TypeSig.fromArgs'
  gives the signature of some arguments. A 'CallMeMaybe' holds a function
  and calls it, reading its name off the function and giving it back as
  '__wrapped__'. A 'Permuter' calls a function with the arguments put
  back in the order an 'Arrangement' restores. Read through the class,
  an overloaded name gives a callable, and the class dictionary holds
  its 'Dispatcher'. Source: the docstrings of these names.
  """

  def test_flex_call(self) -> None:
    def add(a: int, b: int) -> int:
      return a + b

    wrapped = flexCall(add)
    self.assertEqual(wrapped(1, 2, 3), 3)
    self.assertTrue(isFlex(wrapped))
    self.assertFalse(isFlex(add))
    self.assertEqual(wrapped.__name__, 'add')
    self.assertIs(wrapped.__wrapped__, add)
    with self.assertRaises(TypeError):
      wrapped(1)
    with self.assertRaises(TypeException) as context:
      flexCall(len)
    self.assertEqual(context.exception.varName, 'func')
    self.assertIs(context.exception.actualObject, len)

  def test_type_sig(self) -> None:
    self.assertEqual(TypeSig(int, str), TypeSig(int, str))
    self.assertEqual(hash(TypeSig(int, str)), hash(TypeSig(int, str)))
    self.assertNotEqual(TypeSig(int, str), TypeSig(str, int))
    self.assertEqual(len(TypeSig(int, str)), 2)
    self.assertEqual(list(TypeSig(int, str)), [int, str])
    self.assertIn(int, TypeSig(int, str))
    self.assertEqual(TypeSig.fromArgs(1, 'a'), TypeSig(int, str))
    self.assertEqual(TypeSig.fromArgs(True), TypeSig(bool))
    self.assertNotEqual(TypeSig(int, str), (int, str))
    self.assertFalse(isFlex(3))

  def test_call_me_maybe(self) -> None:
    def add(a: int, b: int) -> int:
      return a + b

    held = CallMeMaybe(add)
    self.assertEqual(held(1, 2), 3)
    self.assertEqual(held.__name__, 'add')
    self.assertIs(held.__wrapped__, add)

  def test_permuter(self) -> None:
    def subtract(a: int, b: int) -> int:
      return a - b

    swapped = Permuter(subtract, Arrangement(('a', 'b'), (1, 0)))
    self.assertEqual(swapped(3, 10), 7)

  def test_dispatcher_on_the_class(self) -> None:
    class Greeter(BaseObject):
      @overload(str)
      def greet(self, name: str) -> str:
        return name

    self.assertIsInstance(vars(Greeter)['greet'], Dispatcher)
    self.assertTrue(callable(Greeter.greet))
    self.assertEqual(Greeter().greet('ada'), 'ada')

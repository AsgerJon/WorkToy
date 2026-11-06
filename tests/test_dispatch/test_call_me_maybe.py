"""
TestCallMeMaybe tests 'CallMeMaybe' from 'worktoy.dispatch'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from collections.abc import Callable

from worktoy.dispatch import CallMeMaybe
from worktoy.dispatch._call_me_maybe import _Wrapped
from worktoy.waitaminute import MissingVariable, TypeException
from . import DispatchTest


def _echo(*args, **kwargs) -> tuple:
  """Returns what it was called with."""
  return args, kwargs


class TestCallMeMaybe(DispatchTest):
  """
  The dispatch machinery holds functions in holders that call like the
  function, read names off it, and are never bound as methods. The tests
  pin the forwarding, the pass-through of names, the refusal of a place
  in a class body, the empty holder, the setter, and the descriptor
  behind '__wrapped__' with its refusals.
  """

  def test_call_forwards(self) -> None:
    holder = CallMeMaybe(_echo)
    self.assertEqual(holder(1, 2, k=3), ((1, 2), {'k': 3}))
    self.assertEqual(holder(1, func='x'), ((1,), {'func': 'x'}))
    self.assertIs(holder.__wrapped__, _echo)

  def test_invoke_default(self) -> None:
    holder = CallMeMaybe()
    self.assertEqual(holder.invoke(_echo, 1, k=2), ((1,), {'k': 2}))

  def test_names_read_off_function(self) -> None:
    holder = CallMeMaybe(_echo)
    self.assertEqual(holder.__name__, '_echo')
    self.assertEqual(holder.__qualname__, '_echo')
    self.assertEqual(holder.__doc__, CallMeMaybe.__doc__)
    with self.assertRaises(AttributeError):
      _ = holder.nothing

  def test_never_bound_as_method(self) -> None:
    class Owner:
      pass

    Owner.held = CallMeMaybe(_echo)
    self.assertEqual(Owner().held(1), ((1,), {}))

  def test_place_in_class_body_refused(self) -> None:
    holder = CallMeMaybe(_echo)
    with self.assertRaises(TypeError) as context:
      holder.__set_name__(int, 'held')
    self.assertIn("'CallMeMaybe' does not support the descriptor protocol",
                  str(context.exception))

  def test_not_callable_refused(self) -> None:
    with self.assertRaises(TypeException) as context:
      CallMeMaybe(5)
    self.assertEqual(context.exception.varName, 'func')
    self.assertEqual(context.exception.actualObject, 5)
    self.assertIs(context.exception.actualType, int)
    self.assertEqual(context.exception.expectedTypes, (Callable,))
    self.assertIn("'func'", str(context.exception))
    self.assertIn("'Callable'", str(context.exception))

  def test_empty_holder(self) -> None:
    holder = CallMeMaybe()
    with self.assertRaises(MissingVariable) as context:
      holder()
    self.assertEqual(context.exception.varName, '__function_case__')
    self.assertIs(context.exception.instance, holder)
    self.assertEqual(context.exception.expectedTypes, (tuple,))
    self.assertIn("'CallMeMaybe.__function_case__: tuple'",
                  str(context.exception))
    with self.assertRaises(MissingVariable) as context:
      _ = holder.__wrapped__
    self.assertEqual(context.exception.varName, '__function_case__')
    self.assertIs(context.exception.instance, holder)
    self.assertEqual(context.exception.expectedTypes, (tuple,))
    with self.assertRaises(AttributeError):
      _ = holder.__name__

  def test_set_function(self) -> None:
    holder = CallMeMaybe()
    holder.setFunction(_echo)
    self.assertEqual(holder(7), ((7,), {}))
    holder.setFunction(len)
    self.assertEqual(holder('abc'), 3)
    holder.setFunction(5)
    with self.assertRaises(TypeError):
      holder()

  def test_wrapped_descriptor(self) -> None:
    self.assertIsInstance(CallMeMaybe.__wrapped__, _Wrapped)
    blank = _Wrapped.__new__(_Wrapped)
    with self.assertRaises(MissingVariable) as context:
      blank.__get__(CallMeMaybe(_echo), CallMeMaybe)
    self.assertEqual(context.exception.varName, '__private_key__')
    self.assertIs(context.exception.instance, blank)
    self.assertIn("'_Wrapped.__private_key__", str(context.exception))
    wrong = _Wrapped('__function_case__')
    object.__setattr__(wrong, '__private_key__', 42)
    with self.assertRaises(TypeException) as context:
      wrong.__get__(CallMeMaybe(_echo), CallMeMaybe)
    self.assertEqual(context.exception.varName, '__private_key__')
    self.assertEqual(context.exception.actualObject, 42)
    self.assertIs(context.exception.actualType, int)
    self.assertEqual(context.exception.expectedTypes, (str,))
    self.assertIn("'__private_key__'", str(context.exception))
    holder = CallMeMaybe(_echo)
    object.__setattr__(holder, '__function_case__', 'x')
    with self.assertRaises(TypeException) as context:
      _ = holder.__wrapped__
    self.assertEqual(context.exception.varName, 'funcTuple')
    self.assertEqual(context.exception.actualObject, 'x')
    self.assertIs(context.exception.actualType, str)
    self.assertEqual(context.exception.expectedTypes, (tuple,))
    self.assertIn("'funcTuple'", str(context.exception))

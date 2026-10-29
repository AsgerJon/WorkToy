"""
TestDispatcherRefuseUncallable subclasses 'DispatcherTest' and pins that
the decorators of a 'Dispatcher' wired by hand, 'overload', 'flex',
'fallback' and 'finalize', refuse what the 'overload' decorator refuses:
a 'staticmethod' or 'classmethod' object, which the dispatcher could not
call with an instance first, and anything that cannot be called, with
'TypeException' naming 'func' at the decorator. Such an object used to be
registered and fail at the first call, with "'int' object is not
callable" or the method's own arity error.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.dispatch import Dispatcher
from worktoy.waitaminute import TypeException

from . import DispatcherTest


def _plain(self, *args) -> tuple:
  return args  # pragma: no cover


class TestDispatcherRefuseUncallable(DispatcherTest):
  """
  TestDispatcherRefuseUncallable provides tests for the refusal of
  method objects and uncallable objects by a 'Dispatcher' wired by hand.
  """

  def test_value_refused_naming_func(self) -> None:
    """A bare value is refused by 'overload', naming 'func'."""
    with self.assertRaises(TypeException) as context:
      Dispatcher().overload(int)(42)
    self.assertEqual(context.exception.varName, 'func')

  def test_method_kinds_refused_by_every_decorator(self) -> None:
    """A staticmethod, a classmethod and a value are refused by every
    decorator of the dispatcher."""
    for bad in (staticmethod(_plain), classmethod(_plain), 42):
      dispatcher = Dispatcher()
      decorators = (
        dispatcher.overload(int),
        dispatcher.flex(int, str),
        dispatcher.fallback,
        dispatcher.finalize,
      )
      for decorator in decorators:
        with self.subTest(bad=type(bad).__name__, decorator=decorator):
          with self.assertRaises(TypeException):
            decorator(bad)

  def test_nothing_registered_after_refusal(self) -> None:
    """A refused registration leaves the dispatcher as it was."""
    dispatcher = Dispatcher()
    with self.assertRaises(TypeException):
      dispatcher.overload(int)(42)
    self.assertEqual(dispatcher._getSigFuncList(), [])
    self.assertIsNone(dispatcher._getFallbackFunction())

  def test_callable_accepted(self) -> None:
    """A plain function and a callable object are accepted."""

    class Callable:
      def __call__(self, instance, *args) -> tuple:
        return args  # pragma: no cover

    dispatcher = Dispatcher()
    self.assertIs(dispatcher.overload(int)(_plain), dispatcher)
    self.assertIs(dispatcher.overload(str)(Callable()), dispatcher)
    self.assertEqual(len(dispatcher._getSigFuncList()), 2)

"""
TestOverloadRefuseUncallable subclasses 'OverloadTest' and pins that
'overload', 'overload.flex', 'overload.fallback' and 'overload.finalize'
refuse an object that cannot be called, such as a 'property' stacked
below the decorator or a bare value, with 'TypeException' at the
decorator. Such an object used to be registered and the class built, so
the first call failed with "'property' object is not callable".
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.dispatch import overload
from worktoy.waitaminute import TypeException

from . import OverloadTest


def _plain(self, *args) -> tuple:
  return args  # pragma: no cover


class TestOverloadRefuseUncallable(OverloadTest):
  """
  TestOverloadRefuseUncallable provides tests for the refusal of objects
  that cannot be called.
  """

  def test_property_refused(self) -> None:
    """A 'property' below '@overload' is refused, naming 'func'."""
    with self.assertRaises(TypeException) as context:
      overload(int)(property(_plain))
    self.assertEqual(context.exception.varName, 'func')

  def test_value_refused(self) -> None:
    """A bare value is refused by every decorator."""
    decorators = (
      overload(int),
      overload.flex(int, str),
      overload.fallback,
      overload.finalize,
    )
    for decorator in decorators:
      with self.subTest(decorator=decorator):
        with self.assertRaises(TypeException):
          decorator(42)

  def test_callable_accepted(self) -> None:
    """A plain function and a callable object are accepted."""

    class Callable:
      def __call__(self, instance, *args) -> tuple:
        return args  # pragma: no cover

    self.assertIsInstance(overload(int)(_plain), overload)
    self.assertIsInstance(overload(int)(Callable()), overload)

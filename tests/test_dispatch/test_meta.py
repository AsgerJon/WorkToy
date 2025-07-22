"""
TestMeta provides coverage gymnastics for the overload implementations
through the metaclass.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.dispatch import overload
from worktoy.mcls import BaseObject
from . import DispatcherTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class TestMeta(DispatcherTest):
  """
  TestMeta provides coverage gymnastics for the overload implementations
  through the metaclass.
  """

  def test_fallback(self) -> None:
    """Tests the fallback functionality of the Dispatcher."""

    class Foo(BaseObject):
      """The 'bar' method is overloaded with fallback"""

      __bar_value__ = None

      def getBar(self) -> Any:
        """Get the bar value."""
        return self.__bar_value__

      @overload(int, int)
      def bar(self, x: int, y: int) -> None:
        """Overloaded method for two integers."""
        self.__bar_value__ = str(x + y)

      @overload(int)
      def bar(self, x: int) -> None:
        """Overloaded method for one integer."""
        self.__bar_value__ = str(x)

      @overload.fallback
      def bar(self, *args, **kwargs) -> None:
        """Fallback method for unsupported types."""
        self.__bar_value__ = '%s | %s' % (str(args, ), str(kwargs, ))

    foo = Foo()
    posArgs = (69, 420)
    foo.bar(*posArgs)
    self.assertEqual(foo.getBar(), '489')
    foo.bar(69)
    self.assertEqual(foo.getBar(), '69')
    foo.bar(69, 420, 1337, lmao=True)
    expected = """(69, 420, 1337) | {'lmao': True}"""
    self.assertEqual(foo.getBar(), expected)

  def test_latest_none(self) -> None:
    """Tests the latest method with None as the latest value."""

    foo = overload(_root=True)
    with self.assertRaises(RuntimeError):
      _ = foo._getLatestFunc()

    def breh() -> None:
      """Placeholder function."""

    foo._setFallbackFunc(breh)
    self.assertEqual(foo.__name__, 'breh')

    bar = overload(_root=True)
    with self.assertRaises(AttributeError):
      _ = bar.__name__

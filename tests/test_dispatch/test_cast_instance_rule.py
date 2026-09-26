"""
TestCastInstanceRule subclasses 'DispatcherTest' and pins what the cast
passes of a 'Dispatcher' do with a type whose constructor hands back
something other than an instance of it. The cast to such a type fails, so
its signature does not match and the call moves on, here to the
fallback, instead of reaching the overload with a value of the wrong
type.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.dispatch import overload
from worktoy.mcls import BaseObject

from . import DispatcherTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class TestCastInstanceRule(DispatcherTest):
  """
  TestCastInstanceRule provides tests for the cast passes of a
  'Dispatcher' and types whose constructor misbehaves.
  """

  def test_shifty_signature_skipped(self) -> None:
    """A call that could match only by casting to such a type goes to
    the fallback, while a value already of the type still reaches the
    overload."""

    class Shifty:
      def __new__(cls, *args: Any) -> Any:
        if args:
          return 42
        return object.__new__(cls)

    class Router(BaseObject):
      @overload(Shifty)
      def route(self, value: Any) -> Any:
        return 'shifty', value

      @overload.fallback
      def route(self, *args: Any) -> Any:
        return 'fallback', args

    router = Router()
    self.assertEqual(router.route('x'), ('fallback', ('x',)))
    shifty = Shifty()
    self.assertEqual(router.route(shifty), ('shifty', shifty))

"""
TestCastText subclasses 'DispatcherTest' and pins what the cast passes of
a 'Dispatcher' do with the text types. A call reaches a 'str', 'bytes' or
'bytearray' signature through a cast only with text, converted as UTF-8,
so an 'int' no longer lands in a 'bytes' overload as zero bytes, and goes
on to the fallback instead.
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


class TestCastText(DispatcherTest):
  """
  TestCastText provides tests for the cast passes of a 'Dispatcher' and
  signatures over the text types.
  """

  def test_text_signatures(self) -> None:
    """An 'int' matches no text signature and reaches the fallback, while
    text casts to the signature it fits."""

    class Router(BaseObject):
      @overload(bytes)
      def route(self, value: Any) -> Any:
        return 'bytes', value

      @overload(bytearray, bytearray)
      def route(self, *values: Any) -> Any:
        return 'bytearray', values

      @overload.fallback
      def route(self, *args: Any) -> Any:
        return 'fallback', args

    router = Router()
    self.assertEqual(router.route(3), ('fallback', (3,)))
    self.assertEqual(router.route('ab'), ('bytes', b'ab'))
    pair = router.route('a', b'b')
    self.assertEqual(pair, ('bytearray', (bytearray(b'a'), bytearray(b'b'))))

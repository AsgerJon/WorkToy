"""
TestInlineLorem tests the 'InlineLorem' class from the 'worktoy.markdown'
package.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from random import randint
from typing import TYPE_CHECKING

from worktoy.markwork import InlineLorem

from . import MarkworkTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Optional, Union, Self


class TestInlineLorem(MarkworkTest):
  """
  TestInlineLorem tests the 'InlineLorem' class from the 'worktoy.markdown'
  package.
  """

  def test_init(self, ) -> None:
    """
    This method tests the different constructors of the 'InlineLorem'
    class. Please note that constructors inherited from 'InlineText' are
    not tested here, but in the 'TestInlineText' class.

    Overloaded Constructors
    -----------------------
    @overload(str)  # Disabled
    def __init__(self, *_) -> Never: ...

    @overload(int)
    def __init__(self, count: int) -> None: ...

    @overload()
    def __init__(self) -> None: ...

    @overload(THIS)
    def __init__(self, other: Self) -> None: ...
    """

    countOffset = str.__len__("""<InlineLorem: >""")

    with self.assertRaises(TypeError):
      InlineLorem("""Never gonna give you up, """)

    for _ in range(10):
      count = randint(69, 420)
      loremLine = InlineLorem(count)
      loremText = str(loremLine)
      expectedLength = count + countOffset
      actualLength = len(loremText)
      self.assertEqual(expectedLength, actualLength)

    emptyLine = InlineLorem()
    emptyText = str(emptyLine)
    expectedLength = InlineLorem.__fallback_count__ + countOffset
    actualLength = len(emptyText)
    self.assertEqual(expectedLength, actualLength)

    for thisLorem in self.randomInlineLorems(69, 10):
      loremLine = InlineLorem(thisLorem)
      count = loremLine.lorem.charCount
      loremText = str(loremLine)
      expectedLength = count + countOffset
      actualLength = len(loremText)
      self.assertEqual(expectedLength, actualLength)

  def test_recursion_guard(self, ) -> None:
    """
    This method covers the sanity-checking recursion guard in the
    '_getCache' method of 'InlineLorem'.
    """

    class RecursionInlineLorem(InlineLorem):
      def _createCache(self, ) -> None:
        """
        This reimplementation of prevents the cache from being created,
        causing the 'getCache' method to recursively call itself, except
        for a recursion guard.
        """
        pass

    recursionLine = RecursionInlineLorem()
    with self.assertRaises(RecursionError):
      _ = recursionLine.cached

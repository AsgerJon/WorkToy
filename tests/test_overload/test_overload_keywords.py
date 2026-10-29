"""
TestOverloadKeywords subclasses 'OverloadTest' and pins that 'overload'
takes no keyword. It used to take 'strict', which went undocumented, and
ignored any other keyword, so a misspelled 'strict' left the signature
open to casts without a word; now that 'typeCast' decides every cast by
one rule, 'strict' is gone and refused like any other keyword.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.dispatch import overload

from . import OverloadTest


class TestOverloadKeywords(OverloadTest):
  """
  TestOverloadKeywords provides tests for the keywords of 'overload'.
  """

  def test_unknown_keyword_refused(self) -> None:
    """A keyword 'overload' does not take raises 'TypeError'."""
    with self.assertRaises(TypeError) as context:
      overload(int, strikt=True)
    self.assertIn('strikt', str(context.exception))

  def test_strict_refused(self) -> None:
    """'strict' is no keyword any more and is refused as any other."""
    for strict in (True, False):
      with self.subTest(strict=strict):
        with self.assertRaises(TypeError) as context:
          overload(int, strict=strict)
        self.assertIn('strict', str(context.exception))

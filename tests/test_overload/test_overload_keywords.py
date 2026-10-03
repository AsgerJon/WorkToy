"""
TestOverloadKeywords subclasses 'OverloadTest' and pins the keywords
'overload' takes. It took 'strict', which goes undocumented, and ignored
any other keyword, so a misspelled 'strict' left the signature open to
casts without a word.
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

  def test_strict_taken(self) -> None:
    """'strict' is taken either way."""
    for strict in (True, False):
      with self.subTest(strict=strict):
        self.assertTrue(callable(overload(int, strict=strict)))

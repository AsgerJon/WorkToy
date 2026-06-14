"""
TestOverloadRepr covers the string representation of an 'overload'
instance that carries only a fallback, only a finalizer, or no function
at all, the branches that render a short note instead of a signature
listing.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.dispatch import overload
from . import OverloadTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class TestOverloadRepr(OverloadTest):
  """
  TestOverloadRepr pins the '__str__' output of an 'overload' that has no
  registered signature-function pair yet, so it renders a note naming the
  fallback or finalizer rather than raising.
  """

  def test_fallback_only_str(self) -> None:
    """An overload carrying only a fallback names that fallback."""

    def fallbackFunc(self, *args) -> Any:
      return 'fallback ran'

    self.assertEqual(fallbackFunc(None), 'fallback ran')
    ovl = overload.fallback(fallbackFunc)
    info = str(ovl)
    self.assertEqual(str(ovl), repr(ovl))
    self.assertIn('fallback', info)
    self.assertIn('fallbackFunc', info)

  def test_finalizer_only_str(self) -> None:
    """An overload carrying only a finalizer names that finalizer."""

    def finalizerFunc(self, *args) -> Any:
      return 'finalizer ran'

    self.assertEqual(finalizerFunc(None), 'finalizer ran')
    ovl = overload.finalize(finalizerFunc)
    info = str(ovl)
    self.assertEqual(str(ovl), repr(ovl))
    self.assertIn('finalizer', info)
    self.assertIn('finalizerFunc', info)

  def test_empty_overload_str(self) -> None:
    """A bare overload with nothing registered renders a plain note."""
    ovl = overload(_root=True)
    info = str(ovl)
    self.assertEqual(str(ovl), repr(ovl))
    self.assertIn('no function', info)

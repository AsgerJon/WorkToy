"""
RefusedHasCastRule holds the refusals that belong with
'design.promises.utilities.promise_has_cast_rule'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.utilities import hasCastRule
from worktoy.waitaminute.dispatch import UnboundCastHook


class RefusedHasCastRule(TestCase):
  """
  Each of the following is refused, and the exception named is the one raised
  as of 1.2.3. A '__cast_as__' without '@classmethod' raises
  'UnboundCastHook'. Source: the 'hasCastRule' docstring.
  """

  def test_unbound_hook(self) -> None:
    class Loose:
      def __cast_as__(cls, value):
        return cls()

    with self.assertRaises(Exception) as refused:
      hasCastRule(Loose)
    self.assertIsInstance(refused.exception, UnboundCastHook)

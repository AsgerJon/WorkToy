"""
RefusedResolveMRO holds the refusals that belong with
'design.promises.utilities.promise_resolve_mro'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.utilities import resolveMRO


class RefusedResolveMRO(TestCase):
  """
  Each of the following is refused, and the exception named is the one raised
  as of 1.2.3. Bases Python would refuse raise 'TypeError', as the class
  statement does. Source: the 'resolveMRO' docstring and its example.
  """

  def test_inconsistent(self) -> None:
    class A:
      pass

    class B(A):
      pass

    with self.assertRaises(Exception) as refused:
      resolveMRO(A, B)
    self.assertIsInstance(refused.exception, TypeError)

"""TestTypeSig tests the type signature"""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.meta import TypeSig


class TestTypeSig(TestCase):
  """TestTypeSig tests the type signature"""

  def setUp(self) -> None:
    """Set up the test case."""
    self.pointSig = TypeSig(float, float)
    self.complexSig = TypeSig(complex)

  def test_cast(self) -> None:
    """Testing if types cast correctly"""
    x, y = self.pointSig.cast(7, 9)
    self.assertEqual(x, 7)
    self.assertEqual(y, 9)

    z = self.complexSig.cast(7 + 9j).pop()
    self.assertEqual(z.real, 7.0)
    self.assertEqual(z.imag, 9.0)

    nope = self.pointSig.cast('lol')
    self.assertIsNone(nope)

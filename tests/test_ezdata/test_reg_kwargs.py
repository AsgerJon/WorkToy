"""
TestRegKwargs tests instantiating EZData classes with keyword arguments.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from . import EZTest, RegularClass

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestRegKwargs(EZTest):
  """
  TestRegKwargs tests instantiating EZData classes with keyword arguments.
  """

  def test_base_get_kwargs(self) -> None:
    """Testing 'get' on the base class with keyword arguments."""
    ez = RegularClass(a=69, b=420, c=1337)
    self.assertEqual(ez.a, 69)
    self.assertEqual(ez.b, 420)
    self.assertEqual(ez.c, 1337)

  def test_base_set_kwargs(self) -> None:
    """Testing 'set' on the base class with keyword arguments."""
    ez = RegularClass()
    self.assertEqual(ez.a, 0)
    self.assertEqual(ez.b, 10)
    self.assertEqual(ez.c, 20)
    ez.a = 69
    ez.b = 420
    ez.c = 1337
    self.assertEqual(ez.a, 69)
    self.assertEqual(ez.b, 420)
    self.assertEqual(ez.c, 1337)

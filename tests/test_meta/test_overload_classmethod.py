"""TestOverloadClassmethod tests that the overload decorator correctly
handles methods decorated with '@classmethod'. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.base import BaseObject, overload
from worktoy.desc import AttriBox


class Complex(BaseObject):
  """Complex uses classmethods for testing. """

  r = AttriBox[float](0.0)
  i = AttriBox[float](0.0)

  def __init__(self, r: float, i: float) -> None:
    self.r = r
    self.i = i


class TestOverloadClassmethod(TestCase):
  """TestOverloadClassmethod tests that the overload decorator correctly
  handles methods decorated with '@classmethod'. """

  def setUp(self) -> None:
    self.z = Complex(69, 420)

  def test_create(self) -> None:
    """Test that the 'create' method works as expected. """
    self.assertEqual(self.z.r, 69)
    self.assertEqual(self.z.i, 420)

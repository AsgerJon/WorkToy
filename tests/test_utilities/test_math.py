"""
TestMath tests the mathematical utilities in the
'worktoy.utilities.mathematics' module.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from random import random
from typing import TYPE_CHECKING

from . import UtilitiesTest
from worktoy.utilities.mathematics import pi, log, exp, sin, cos, tan, \
  cosh, sinh, arcTan, tanh, atan2

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestMath(UtilitiesTest):
  """
  TestMath tests the mathematical utilities in the
  'worktoy.utilities.mathematics' module.
  """

  def testConstants(self) -> None:
    """Test mathematical constants."""
    self.assertAlmostEqual(cos(pi / 4), sin(pi / 4), )
    self.assertAlmostEqual(exp(log(69)), 69, )

  def testTrigonometry(self) -> None:
    """Test trigonometric functions."""
    self.assertAlmostEqual(sin(pi / 2), 1.0, )
    self.assertAlmostEqual(cos(pi), -1.0, )
    self.assertAlmostEqual(tan(pi / 4), 1.0, )

  def test_identities_real(self) -> None:
    """Test sampling functions."""
    for _ in range(100):
      x = - 1. + (random() * 2)
      self.assertAlmostEqual(exp(x) * exp(-x), 1.0)
      self.assertAlmostEqual(log(exp(x)), x)
      self.assertAlmostEqual(sin(x) ** 2 + cos(x) ** 2, 1.0)
      self.assertAlmostEqual(cos(x * 1j), cosh(x))
      self.assertAlmostEqual(sin(x * 1j), sinh(x) * 1j)

  def test_identities_complex(self) -> None:
    """Test sampling functions."""
    for _ in range(100):
      x = - 1. + (random() * 2)
      y = - 1. + (random() * 2)
      z = x + y * 1j
      self.assertAlmostEqual(exp(z) * exp(-z), 1.0)
      self.assertAlmostEqual(cos(z) ** 2 + sin(z) ** 2, 1.0)
      self.assertAlmostEqual(cosh(z) ** 2 - sinh(z) ** 2, 1.0)
      self.assertAlmostEqual(sin(x + y * 1j).real, sin(x - y * 1j).real)
      self.assertAlmostEqual(sin(x + y * 1j).imag, -sin(x - y * 1j).imag)
      self.assertAlmostEqual(cos(x + y * 1j).real, cos(x - y * 1j).real)
      self.assertAlmostEqual(cos(x + y * 1j).imag, -cos(x - y * 1j).imag)

  def test_zeros(self) -> None:
    """Test zeros of functions."""
    self.assertAlmostEqual(sin(0), 0.0, )
    self.assertAlmostEqual(cos(pi), -1.0, )
    self.assertAlmostEqual(cosh(0), 1.0, )
    self.assertAlmostEqual(sinh(0), 0.0, )
    self.assertAlmostEqual(tan(0), 0.0, )

  def test_hyperbolic(self) -> None:
    """Test hyperbolic functions."""
    self.assertAlmostEqual(cosh(0), 1.0, )
    self.assertAlmostEqual(sinh(0), 0.0, )
    self.assertAlmostEqual(tanh(0), 0.0, )
    self.assertAlmostEqual(cosh(pi / 2), cos(pi / 2 * 1j), )
    self.assertAlmostEqual(sinh(69j), 1j * sin(69), )
    self.assertAlmostEqual(sinh(420j), 1j * sin(420), )
    self.assertAlmostEqual(tanh(69j), 1j * tan(69), )

  def test_bad_log(self) -> None:
    """Test bad log inputs."""
    with self.assertRaises(ValueError):
      log('breh')
    with self.assertRaises(ZeroDivisionError):
      log(0.0)

  def test_bad_tan(self) -> None:
    with self.assertRaises(ZeroDivisionError):
      tan(pi / 2)

  def test_complex_log(self) -> None:
    """Test complex logarithm."""
    self.assertAlmostEqual(log(-1), pi * 1j, )
    self.assertAlmostEqual(log(1), 0)
    z = 69 + 420j
    actual = log(z)
    expectedRe = log(abs(z))
    expectedIm = atan2(z.imag, z.real)
    expected = expectedRe + expectedIm * 1j
    self.assertAlmostEqual(actual, expected, )

  def test_unit_arc_tan(self) -> None:
    """Test unit arctangent."""
    a = 0.95
    b = 1.05
    for i in range(101):
      x = a + (b - a) * i / 100
      self.assertAlmostEqual(sin(arcTan(x)), x / (1 + x ** 2) ** 0.5)
      self.assertAlmostEqual(cos(arcTan(x)), 1 / (1 + x ** 2) ** 0.5)

  def test_arc_tan(self) -> None:
    a = -0.05
    b = 0.05
    for i in range(101):
      x = a + (b - a) * i / 100
      self.assertAlmostEqual(sin(arcTan(x)), x / (1 + x ** 2) ** 0.5)
      self.assertAlmostEqual(cos(arcTan(x)), 1 / (1 + x ** 2) ** 0.5)

  def test_atan2(self) -> None:
    """Test atan2 function."""
    self.assertAlmostEqual(atan2(0, 1), 0.0, )
    self.assertAlmostEqual(atan2(1, 0), pi / 2, )
    self.assertAlmostEqual(atan2(0, -1), pi, )
    self.assertAlmostEqual(atan2(-1, 0), -pi / 2, )
    self.assertAlmostEqual(atan2(-1, -1), -3 * pi / 4, )
    self.assertAlmostEqual(atan2(1, -1), 3 * pi / 4, )

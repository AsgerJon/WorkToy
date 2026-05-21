"""
ComplexTest exercises the arithmetic dunder methods that 'ComplexMixin'
provides. The point of the mixin is that several different complex
number implementations can share one set of arithmetic dunders, and
this single test class is the shared testing framework for them.

List the implementations to test in the 'targets' class attribute.
Each one is a class that mixes in 'ComplexMixin' and is constructed
from two positional arguments: the real part and the imaginary part.
Every test runs once against each target.

The tests touch nothing but the 'REAL' and 'IMAG' attributes.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ._base_test import BaseTest
from ._complex_mixin import ComplexMixin

if TYPE_CHECKING:  # pragma: no cover
  from typing import Type


class ComplexTest(BaseTest):
  """
  Shared test framework for the arithmetic dunder methods of
  'ComplexMixin'. Set 'targets' to the complex number classes under
  test.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  targets: tuple[Type[ComplexMixin], ...] = ()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  UNARY OPERATORS  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def test_pos(self) -> None:
    """Unary plus leaves both parts unchanged."""
    for target in self.targets:
      with self.subTest(target=target.__name__):
        result = +target(3, 4)
        self.assertEqual(result.REAL, 3.0)
        self.assertEqual(result.IMAG, 4.0)

  def test_neg(self) -> None:
    """Unary minus negates both parts."""
    for target in self.targets:
      with self.subTest(target=target.__name__):
        result = -target(3, 4)
        self.assertEqual(result.REAL, -3.0)
        self.assertEqual(result.IMAG, -4.0)

  def test_invert(self) -> None:
    """The invert operator conjugates by negating the imag part."""
    for target in self.targets:
      with self.subTest(target=target.__name__):
        result = ~target(3, 4)
        self.assertEqual(result.REAL, 3.0)
        self.assertEqual(result.IMAG, -4.0)

  def test_abs(self) -> None:
    """The absolute value is the Euclidean magnitude."""
    for target in self.targets:
      with self.subTest(target=target.__name__):
        result = abs(target(3, 4))
        self.assertAlmostEqual(result, 5.0)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  ADDITION   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def test_add_instances(self) -> None:
    """Adding two instances sums both parts."""
    for target in self.targets:
      with self.subTest(target=target.__name__):
        result = target(3, 4) + target(1, 2)
        self.assertEqual(result.REAL, 4.0)
        self.assertEqual(result.IMAG, 6.0)

  def test_add_builtin_complex(self) -> None:
    """A builtin complex is a valid right operand for addition."""
    for target in self.targets:
      with self.subTest(target=target.__name__):
        result = target(3, 4) + (1 + 2j)
        self.assertEqual(result.REAL, 4.0)
        self.assertEqual(result.IMAG, 6.0)

  def test_add_scalar(self) -> None:
    """A real scalar adds to the real part only."""
    for target in self.targets:
      with self.subTest(target=target.__name__):
        result = target(3, 4) + 2
        self.assertEqual(result.REAL, 5.0)
        self.assertEqual(result.IMAG, 4.0)

  def test_radd_scalar(self) -> None:
    """Reflected addition with a scalar left operand works."""
    for target in self.targets:
      with self.subTest(target=target.__name__):
        result = 2 + target(3, 4)
        self.assertEqual(result.REAL, 5.0)
        self.assertEqual(result.IMAG, 4.0)

  def test_add_unsupported(self) -> None:
    """Adding an unsupported type raises TypeError."""
    for target in self.targets:
      with self.subTest(target=target.__name__):
        with self.assertRaises(TypeError):
          _ = target(3, 4) + 'x'

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SUBTRACTION  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def test_sub_instances(self) -> None:
    """Subtracting two instances subtracts both parts."""
    for target in self.targets:
      with self.subTest(target=target.__name__):
        result = target(3, 4) - target(1, 2)
        self.assertEqual(result.REAL, 2.0)
        self.assertEqual(result.IMAG, 2.0)

  def test_sub_scalar(self) -> None:
    """A real scalar subtracts from the real part only."""
    for target in self.targets:
      with self.subTest(target=target.__name__):
        result = target(3, 4) - 1
        self.assertEqual(result.REAL, 2.0)
        self.assertEqual(result.IMAG, 4.0)

  def test_rsub_scalar(self) -> None:
    """Reflected subtraction with a scalar left operand works."""
    for target in self.targets:
      with self.subTest(target=target.__name__):
        result = 10 - target(3, 4)
        self.assertEqual(result.REAL, 7.0)
        self.assertEqual(result.IMAG, -4.0)

  def test_sub_unsupported(self) -> None:
    """Subtracting an unsupported type raises TypeError."""
    for target in self.targets:
      with self.subTest(target=target.__name__):
        with self.assertRaises(TypeError):
          _ = target(3, 4) - 'x'

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  MULTIPLICATION   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def test_mul_instances(self) -> None:
    """Multiplying two instances follows the complex product rule."""
    for target in self.targets:
      with self.subTest(target=target.__name__):
        result = target(3, 4) * target(0, 1)
        self.assertEqual(result.REAL, -4.0)
        self.assertEqual(result.IMAG, 3.0)

  def test_mul_scalar(self) -> None:
    """A real scalar scales both parts."""
    for target in self.targets:
      with self.subTest(target=target.__name__):
        result = target(3, 4) * 2
        self.assertEqual(result.REAL, 6.0)
        self.assertEqual(result.IMAG, 8.0)

  def test_rmul_scalar(self) -> None:
    """Reflected multiplication with a scalar left operand works."""
    for target in self.targets:
      with self.subTest(target=target.__name__):
        result = 2 * target(3, 4)
        self.assertEqual(result.REAL, 6.0)
        self.assertEqual(result.IMAG, 8.0)

  def test_mul_unsupported(self) -> None:
    """Multiplying by an unsupported type raises TypeError."""
    for target in self.targets:
      with self.subTest(target=target.__name__):
        with self.assertRaises(TypeError):
          _ = target(3, 4) * 'x'

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DIVISION   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def test_truediv_instances(self) -> None:
    """Dividing two instances follows the complex quotient rule."""
    for target in self.targets:
      with self.subTest(target=target.__name__):
        result = target(3, 4) / target(1, 2)
        self.assertAlmostEqual(result.REAL, 2.2)
        self.assertAlmostEqual(result.IMAG, -0.4)

  def test_truediv_scalar(self) -> None:
    """A real scalar divisor scales both parts down."""
    for target in self.targets:
      with self.subTest(target=target.__name__):
        result = target(4, 8) / 2
        self.assertAlmostEqual(result.REAL, 2.0)
        self.assertAlmostEqual(result.IMAG, 4.0)

  def test_rtruediv_scalar(self) -> None:
    """Reflected division with a scalar left operand works."""
    for target in self.targets:
      with self.subTest(target=target.__name__):
        result = 2 / target(1, 1)
        self.assertAlmostEqual(result.REAL, 1.0)
        self.assertAlmostEqual(result.IMAG, -1.0)

  def test_truediv_by_zero(self) -> None:
    """Dividing by zero raises ZeroDivisionError."""
    for target in self.targets:
      with self.subTest(target=target.__name__):
        with self.assertRaises(ZeroDivisionError):
          _ = target(3, 4) / target(0, 0)

  def test_truediv_unsupported(self) -> None:
    """Dividing by an unsupported type raises TypeError."""
    for target in self.targets:
      with self.subTest(target=target.__name__):
        with self.assertRaises(TypeError):
          _ = target(3, 4) / 'x'

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  POWER  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def test_pow_scalar(self) -> None:
    """Raising an instance to a real power follows complex power."""
    for target in self.targets:
      with self.subTest(target=target.__name__):
        result = target(2, 0) ** 2
        self.assertAlmostEqual(result.REAL, 4.0)
        self.assertAlmostEqual(result.IMAG, 0.0)

  def test_rpow_scalar(self) -> None:
    """Reflected power with a scalar base operand works."""
    for target in self.targets:
      with self.subTest(target=target.__name__):
        result = 2 ** target(3, 0)
        self.assertAlmostEqual(result.REAL, 8.0)
        self.assertAlmostEqual(result.IMAG, 0.0)

  def test_pow_unsupported(self) -> None:
    """Raising to an unsupported exponent raises TypeError."""
    for target in self.targets:
      with self.subTest(target=target.__name__):
        with self.assertRaises(TypeError):
          _ = target(2, 0) ** 'x'

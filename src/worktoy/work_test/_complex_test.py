"""
ComplexTest is the shared test framework for the 'ComplexMixin' arithmetic
dunders.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING
from unittest import SkipTest, TestCase

from ..utilities import textFmt
from ._complex_mixin import ComplexMixin

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Type


class ComplexTest:
  """
  Several implementations of one interface, here complex arithmetic,
  should pass one bank of tests, written once, without each
  implementation copying it. 'ComplexTest' is that bank for the dunder
  methods of 'ComplexMixin': a test class lists the bank before
  'BaseTest' and its implementations in 'targets', and every test runs
  once against each of them.

    class TestMyComplex(ComplexTest, BaseTest):
      targets = (MyComplex,)

  Implementation
  --------------

  'ComplexTest' has no base of its own, so no loader collects the bank
  itself and no test module importing it pays twenty-five skipped
  tests; the assertions and 'subTest' come from the test case listed
  after it. The twenty-five test methods are each a loop over 'targets'
  with one block of 'subTest' per target labelled by the target's name,
  touching nothing but the 'REAL' and 'IMAG' attributes and
  constructing each target from two positional arguments, the real and
  imaginary parts. 'setUp' hands on and then skips every test of a
  class without targets, so a class that forgot them reports skips
  rather than vacuous passes, and a class may set its targets in
  'setUpClass'. A class listing the bank without a 'TestCase', the
  shape the bank had when it was a 'BaseTest', is refused at the class
  statement with a 'TypeError' naming the shape to write, so its tests
  cannot vanish from a run unnoticed.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  targets: tuple[Type[ComplexMixin], ...] = ()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init_subclass__(cls, **kwargs) -> None:
    """
    A class listing the bank without a test case would be collected by
    no loader, and its tests would vanish from the run without a word;
    it is refused here, at the class statement, with the shape to
    write. A class listing a test case hands on along its resolution
    order.
    """
    if not issubclass(cls, TestCase):
      infoSpec = """'%s' lists 'ComplexTest' as a base but no test case,
      so no loader would run its tests. The bank runs as part of a test
      case: write 'class %s(ComplexTest, BaseTest):' with the
      targets."""
      raise TypeError(textFmt(infoSpec % (cls.__name__, cls.__name__)))
    super().__init_subclass__(**kwargs)

  def setUp(self) -> None:
    """
    A class without targets skips each of its tests rather than running
    them against nothing. The check waits for 'setUp', since a class may
    set its targets in 'setUpClass'. The super call reaches the 'setUp'
    of the test case listed after the bank.
    """
    super().setUp()
    if not self.targets:
      raise SkipTest('%s has no targets' % type(self).__name__)

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
        #  4, since '2 - (1 + 1j)' is also '1 - 1j' and would pass a
        #  reflected division that subtracts.
        result = 4 / target(1, 1)
        self.assertAlmostEqual(result.REAL, 2.0)
        self.assertAlmostEqual(result.IMAG, -2.0)

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
        #  3, since '2 * 2' is also '4' and would pass a power that
        #  multiplies.
        result = target(3, 0) ** 2
        self.assertAlmostEqual(result.REAL, 9.0)
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

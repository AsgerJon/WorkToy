"""
TestEZComplex subclasses 'ComplexTest' from the 'worktoy.work_test'
package and provides complex number implementation tests for classes that
share the 'ComplexMixin' from the same package.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.waitaminute.ezdata import ExtraPositionalException
from worktoy.work_test import ComplexTest
from worktoy.waitaminute import TypeException
from worktoy.ezdata import EZData, EZField
from tests.test_ezdata.examples import EZComplex

if TYPE_CHECKING:  # pragma: no cover
  pass


class FrozenComplex(EZComplex, frozen=True):
  pass


class EZTriple(EZData):
  """A three-field 'EZData' class, not congruent with 'EZComplex'."""

  a = EZField[float](0.0)
  b = EZField[float](0.0)
  c = EZField[float](0.0)


class TestEZComplex(ComplexTest):
  """
  TestEZComplex provides complex number implementation tests for classes that
  share the 'ComplexMixin' from the 'worktoy.work_test' package.
  """

  @classmethod
  def setUpClass(cls) -> None:
    super().setUpClass()
    cls.targets = (EZComplex, FrozenComplex,)

  def test_frozen(self, ) -> None:
    """A 'FrozenComplex' instance rejects attribute assignment."""
    frozen = FrozenComplex(3, 4)
    self.assertEqual(frozen.REAL, 3.0)
    self.assertEqual(frozen.IMAG, 4.0)
    with self.assertRaises(AttributeError):
      frozen.REAL = 9.0

  def test_mutable(self, ) -> None:
    """A plain 'EZComplex' instance allows attribute assignment."""
    z = EZComplex(3, 4)
    z.REAL = 9.0
    self.assertEqual(z.REAL, 9.0)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTION   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def test_init_keyword(self, ) -> None:
    """Keyword arguments fill the fields by name."""
    z = EZComplex(REAL=3, IMAG=4)
    self.assertEqual(z.REAL, 3.0)
    self.assertEqual(z.IMAG, 4.0)

  def test_init_defaults(self, ) -> None:
    """An argument-free constructor falls back to the field defaults."""
    z = EZComplex()
    self.assertEqual(z.REAL, 0.0)
    self.assertEqual(z.IMAG, 0.0)

  def test_init_partial(self, ) -> None:
    """An omitted field receives its default value."""
    z = EZComplex(3)
    self.assertEqual(z.REAL, 3.0)
    self.assertEqual(z.IMAG, 0.0)

  def test_init_coerces_to_float(self, ) -> None:
    """Integer arguments are coerced to the float field type."""
    z = EZComplex(3, 4)
    self.assertIsInstance(z.REAL, float)
    self.assertIsInstance(z.IMAG, float)

  def test_init_rejects_bad_type(self, ) -> None:
    """An argument that cannot become a float raises TypeException."""
    with self.assertRaises(TypeException):
      EZComplex(object(), 4)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GENERATED DUNDERS  # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def test_repr(self, ) -> None:
    """The repr names the class and every field as 'name=value'."""
    text = repr(EZComplex(3, 4))
    self.assertIn('EZComplex(', text)
    self.assertIn('3.0', text)
    self.assertIn('4.0', text)

  def test_eq(self, ) -> None:
    """Instances with equal fields compare equal."""
    self.assertEqual(EZComplex(3, 4), EZComplex(3, 4))

  def test_not_eq(self, ) -> None:
    """Instances with differing fields compare unequal."""
    self.assertNotEqual(EZComplex(3, 4), EZComplex(3, 5))

  def test_congruent_equality(self, ) -> None:
    """A plain and a frozen instance are equal when congruent."""
    self.assertEqual(EZComplex(3, 4), FrozenComplex(3, 4))

  def test_iter(self, ) -> None:
    """Iterating an instance yields the field values in order."""
    self.assertEqual((*EZComplex(3, 4),), (3.0, 4.0))

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  KEYWORD ARGUMENTS  # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def test_frozen_hashable(self, ) -> None:
    """A frozen instance is hashable and equal instances hash alike."""
    self.assertEqual(hash(FrozenComplex(3, 4)), hash(FrozenComplex(3, 4)))

  def test_unfrozen_unhashable(self, ) -> None:
    """A non-frozen instance is unhashable, matching the dataclass."""
    with self.assertRaises(TypeError):
      hash(EZComplex(3, 4))

  def test_frozen_delattr(self, ) -> None:
    """A frozen instance rejects attribute deletion."""
    frozen = FrozenComplex(3, 4)
    with self.assertRaises(AttributeError):
      del frozen.REAL

  def test_not_orderable(self, ) -> None:
    """'EZComplex' is not ordered, so comparison raises TypeError."""
    with self.assertRaises(TypeError):
      _ = EZComplex(1, 2) < EZComplex(3, 4)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONGRUENCE   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def test_congruence_symmetric(self, ) -> None:
    """Congruent equality holds regardless of operand order."""
    self.assertEqual(FrozenComplex(3, 4), EZComplex(3, 4))

  def test_is_congruent_true(self, ) -> None:
    """A class is congruent with a frozen subclass sharing its fields."""
    self.assertTrue(EZComplex.isCongruent(FrozenComplex))

  def test_is_congruent_false(self, ) -> None:
    """A class is not congruent with a differently-fielded class."""
    self.assertFalse(EZComplex.isCongruent(EZTriple))

  def test_eq_unrelated_type(self, ) -> None:
    """An instance never compares equal to an unrelated type."""
    self.assertNotEqual(EZComplex(3, 4), 'three plus four')

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  RESULT TYPES   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def test_add_returns_ez_complex(self, ) -> None:
    """Arithmetic on an 'EZComplex' yields another 'EZComplex'."""
    result = EZComplex(3, 4) + EZComplex(1, 2)
    self.assertIsInstance(result, EZComplex)

  def test_frozen_arithmetic_returns_frozen(self, ) -> None:
    """Arithmetic on a frozen instance yields a frozen instance."""
    result = FrozenComplex(3, 4) + FrozenComplex(1, 2)
    self.assertIsInstance(result, FrozenComplex)
    with self.assertRaises(AttributeError):
      result.REAL = 0.0

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  EDGE CASES   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def test_init_too_many_args(self, ) -> None:
    """More positional arguments than fields raises ValueError."""
    with self.assertRaises(ExtraPositionalException) as context:
      EZComplex(1, 2, 3)
    e = context.exception
    self.assertIs(EZComplex, e.cls)
    self.assertEqual(2, e.fieldCount)
    self.assertEqual(3, e.argCount)
    self.assertEqual(str(e), repr(e))

  def test_init_mixed_args_kwargs(self, ) -> None:
    """A field may come positionally and another by keyword."""
    z = EZComplex(3, IMAG=4)
    self.assertEqual(z.REAL, 3.0)
    self.assertEqual(z.IMAG, 4.0)

  def test_kwarg_overrides_positional(self, ) -> None:
    """A keyword argument overrides a positional one for a field."""
    z = EZComplex(1, REAL=9)
    self.assertEqual(z.REAL, 9.0)

  def test_frozen_iterable(self, ) -> None:
    """A frozen instance is still iterable over its field values."""
    self.assertEqual((*FrozenComplex(3, 4),), (3.0, 4.0))

  def test_conjugate(self) -> None:
    """The 'conjugate' method returns the complex conjugate."""
    z = EZComplex(69, 420)
    zConj = z.conjugate()
    self.assertAlmostEqual(z * zConj, abs(z) ** 2)

"""
TestComplexMixin subclasses 'ComplexTest' from the 'worktoy.work_test'
package and provides tests for 'ComplexMixin' from the
'worktoy.work_test.mixins' package.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.waitaminute import TypeException
from worktoy.work_test import ComplexTest, ComplexMixin
from . import SimpleComplex

if TYPE_CHECKING:  # pragma: no cover
  from typing import Type


class TestComplexMixin(ComplexTest):
  """
  TestComplexMixin subclasses 'ComplexTest' from the 'worktoy.work_test'
  package and provides tests for 'ComplexMixin' from the
  'worktoy.work_test.mixins' package.
  """

  targets: tuple[Type[ComplexMixin], ...] = (SimpleComplex,)

  def test_init(self, ) -> None:
    """
    Test that the 'ComplexMixin' can be initialized without errors.
    """
    for target in self.targets:
      instance = target()
      self.assertIsInstance(instance, ComplexMixin)
      self.assertFalse(instance.REAL)
      self.assertFalse(instance.IMAG)

  def test_recursion(self, ) -> None:
    """
    Test that the 'ComplexMixin' does not cause recursion errors when
    accessing the REAL and IMAG properties.
    """
    for target in self.targets:
      instance = target()
      with self.assertRaises(RecursionError):
        _ = instance._getReal(_recursion=True)
      with self.assertRaises(RecursionError):
        _ = instance._getImag(_recursion=True)

  def test_bad_type_get(self, ) -> None:
    """Arithmetic with an unrelated type returns NotImplemented."""
    z = SimpleComplex(69, 420)
    pvtNames = '__real_value__', '__imag_value__'
    pubNames = 'REAL', 'IMAG'
    for pvt, pub in zip(pvtNames, pubNames):
      object.__setattr__(z, pvt, 'sixty-nine')
      with self.assertRaises(TypeException) as context:
        _ = getattr(z, pub)
      e = context.exception
      self.assertEqual(e.varName, pvt)
      self.assertEqual(e.actualObject, 'sixty-nine')
      self.assertIs(e.actualType, str)
      self.assertIn(float, e.expectedTypes)
      self.assertEqual(str(e), repr(e))

  def test_bad_type_set(self, ) -> None:
    """Setting a field to an incompatible type raises TypeException."""
    z = SimpleComplex(69, 420)
    for name in 'REAL', 'IMAG':
      with self.assertRaises(TypeException) as context:
        setattr(z, name, 'sixty-nine')
      e = context.exception
      self.assertIs(e.varName, name)
      self.assertEqual(e.actualObject, 'sixty-nine')
      self.assertIs(e.actualType, str)
      self.assertIn(float, e.expectedTypes)
      self.assertEqual(str(e), repr(e))

  def test_init_positional(self, ) -> None:
    """Positional arguments fill the fields in declaration order."""
    z1 = SimpleComplex(69 + 420j)
    self.assertEqual(z1.REAL, 69.0)
    self.assertEqual(z1.IMAG, 420.0)
    z2 = SimpleComplex(3, 4)
    self.assertEqual(z2.REAL, 3.0)
    self.assertEqual(z2.IMAG, 4.0)
    z3 = SimpleComplex(1337.)
    self.assertEqual(z3.REAL, 1337.0)

  def test_resolve_other(self) -> None:
    """Arithmetic with an unrelated type returns NotImplemented."""
    expectedObject = NotImplemented
    actualObject = SimpleComplex._resolveOther(object())
    self.assertIs(actualObject, expectedObject)
    expectedObject = SimpleComplex('69+420j')
    actualObject = SimpleComplex._resolveOther('69+420j')
    self.assertEqual(actualObject, expectedObject)
    expectedObject = SimpleComplex(69, 420)
    actualObject = SimpleComplex._resolveOther((69, 420))
    self.assertEqual(actualObject, expectedObject)
    expectedObject = NotImplemented
    actualObject = SimpleComplex._resolveOther((object(), object()))
    self.assertIs(actualObject, expectedObject)

  def test_init_str(self) -> None:
    """Initialization with a string parses the real and imaginary parts."""
    z = SimpleComplex('69+420j')
    self.assertEqual(z.REAL, 69.0)
    self.assertEqual(z.IMAG, 420.0)

  def test_repr(self) -> None:
    """The repr of a SimpleComplex instance includes the class name and
    field values."""
    z = SimpleComplex()
    expectedRepr = 'SimpleComplex()'
    actualRepr = repr(z)
    self.assertEqual(actualRepr, expectedRepr)
    z = SimpleComplex(69)
    expectedRepr = 'SimpleComplex(69.)'
    actualRepr = str.replace(repr(z), '0', '')
    self.assertEqual(actualRepr, expectedRepr)
    z = SimpleComplex(69j)
    expectedRepr = 'SimpleComplex(0.0, 69.0)'
    actualRepr = repr(z)
    n = len(expectedRepr) - 2
    self.assertEqual(actualRepr[:n], expectedRepr[:n])
    z = SimpleComplex(69, 420)
    zRepr = repr(z)
    self.assertTrue(str.startswith(zRepr, 'SimpleComplex('))
    self.assertTrue(str.endswith(zRepr, ')'))
    self.assertIn('69.0', zRepr)
    self.assertIn('420.0', zRepr)

  def test_str(self, ) -> None:
    """
    This method tests the string representation of 'SimpleComplex' instances.
    """
    z = SimpleComplex()
    expectedStr = '0'
    actualStr = str(z)
    self.assertEqual(actualStr, expectedStr)
    z = SimpleComplex(69)
    expectedStr = '69.0'
    actualStr = str(z)
    self.assertEqual(actualStr[:len(expectedStr)], expectedStr)
    z = SimpleComplex(69j)
    expectedStr = '69.J'
    actualStr = str.replace(str(z), '0', '')
    self.assertEqual(actualStr, expectedStr)
    z = SimpleComplex(69, 1337)
    expectedStr = '69. + 1337.J'
    actualStr = str.replace(str(z), '0', '')
    self.assertEqual(actualStr, expectedStr)

  def test_complex(self) -> None:
    """
    This method tests the casting to 'complex' using the '__complex__'
    method on the 'SimpleComplex' class, which should return a built-in
    'complex' instance.
    """
    z = SimpleComplex(69, 420)
    expectedComplex = 69 + 420j
    actualComplex = complex(z)
    self.assertEqual(actualComplex, expectedComplex)

  def test_eq(self, ) -> None:
    """
    This method tests the '__eq__' dunder method on the 'SimpleComplex'
    class, which should return True when the real and imaginary parts of
    two instances are equal, and False otherwise.
    """
    z = SimpleComplex(69, 420)
    expectedResult = NotImplemented
    actualResult = z.__eq__(object())
    self.assertIs(actualResult, expectedResult)
    z2 = SimpleComplex(1337, 80085)
    self.assertNotEqual(z, z2)

  def test_hash(self, ) -> None:
    """
    This method tests the hashing of 'SimpleComplex' instances.
    """
    z1 = SimpleComplex(69, 420)
    z2 = SimpleComplex(1337, 80085)
    z1Hash = hash(z1)
    z2Hash = hash(z2)
    self.assertIsInstance(z1Hash, int)
    self.assertIsInstance(z2Hash, int)
    data = {
      z1: 'sixty-nine, four-twenty',
      z2: 'elite, [REDACTED]'
    }
    self.assertEqual(data[z1], 'sixty-nine, four-twenty')
    self.assertEqual(data[z2], 'elite, [REDACTED]')

  def test_reflected_sub(self, ) -> None:
    """
    This method covers the bad branches of the '__rsub__' reflection method.
    """
    z = SimpleComplex(69, 420)
    expectedResult = NotImplemented
    actualResult = z.__rsub__(object())
    self.assertIs(actualResult, expectedResult)

  def test_reflected_true_div(self, ) -> None:
    """
    This method covers the bad branches of the '__rtruediv__' reflection
    method.
    """
    z = SimpleComplex(69, 420)
    expectedResult = NotImplemented
    actualResult = z.__rtruediv__(object())
    self.assertIs(actualResult, expectedResult)

    z0 = SimpleComplex()
    with self.assertRaises(ZeroDivisionError):
      _ = z / z0
    with self.assertRaises(ZeroDivisionError):
      _ = 1.0 / z0

  def test_reflected_pow(self, ) -> None:
    """
    This method covers the bad branches of the '__rpow__' reflection method.
    """
    z = SimpleComplex(69, 420)
    expectedResult = NotImplemented
    actualResult = z.__rpow__(object())
    self.assertIs(actualResult, expectedResult)

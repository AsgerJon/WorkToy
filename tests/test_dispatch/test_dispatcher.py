"""
TestDispatcher provides tests for the 'Dispatcher' and 'TypeSig'
classes from the 'worktoy.dispatch' package.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.core.sentinels import THIS
from worktoy.mcls import BaseObject
from worktoy.desc import AttriBox
from worktoy.dispatch import TypeSig, Dispatcher, overload
from worktoy.utilities import stringList, textFmt
from worktoy.waitaminute import MissingVariable
from . import DispatcherTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Union, Self, Iterator

  FloatBox: TypeAlias = Union[AttriBox, float]


def funcIntInt(x: int, y: int) -> int:
  return x + y


def funcInt(x: int) -> int:
  return x


def funcStr(x: str) -> str:
  return x


class ComplexCartesian(BaseObject):
  """
  Base for complex number implementations
  """

  realPart: FloatBox = AttriBox[float](0.)
  imagPart: FloatBox = AttriBox[float](0.)

  def __iter__(self, ) -> Iterator[float]:
    yield self.realPart
    yield self.imagPart

  @overload(float, float)
  def __init__(self, real: float, imag: float) -> None:
    self.realPart = real
    self.imagPart = imag

  @overload(THIS)
  def __init__(self, other: Self) -> None:
    self.__init__(*other, )

  @overload(complex)
  def __init__(self, other: complex) -> None:
    self.__init__(other.real, other.imag)

  @overload(float)
  def __init__(self, realPart: float) -> None:
    self.__init__(realPart, 0.)

  @overload()
  def __init__(self, ) -> None:
    self.__init__(0., 0.)

  def __str__(self) -> str:
    if abs(self.realPart) < 1e-12 and abs(self.imagPart) < 1e-12:
      return '0'
    if abs(self.realPart) < 1e-12:
      if abs(self.imagPart - 1.) < 1e-12:
        return 'J'
      if abs(self.imagPart + 1.) < 1e-12:
        return '-J'
      return '%.2fJ' % self.imagPart
    if abs(self.imagPart) < 1e-12:
      return '%.2f' % self.realPart
    if self.imagPart > 0:
      return '%.2f + %.2fJ' % (self.realPart, self.imagPart)
    return '%.2f - %.2fJ' % (self.realPart, -self.imagPart)

  def __repr__(self, ) -> str:
    infoSpec = """%s(%.3f, %.3f)"""
    clsName = type(self).__name__
    return infoSpec % (clsName, self.realPart, self.imagPart)


class Complex(ComplexCartesian):
  """
  Complex subclasses 'ComplexCartesian' and provides a more specific
  implementation of complex numbers. It remains identical to
  'ComplexCartesian' in terms of functionality, but serves as a more
  semantically meaningful class.
  """

  @overload(complex, complex)
  def __init__(self, z0: complex, z1: complex) -> None:
    self.__init__(z1 - z0)

  def __complex__(self, ) -> complex:
    return self.realPart + self.imagPart * 1j

  def __abs__(self, ) -> float:
    return (self.realPart ** 2 + self.imagPart ** 2) ** 0.5

  def __bool__(self, ) -> bool:
    return True if abs(self) > 1e-12 else False


class TestDispatcher(DispatcherTest):
  """
  TestDispatcher provides tests for the 'Dispatcher' and 'TypeSig'
  classes from the 'worktoy.dispatch' package.
  """

  def setUp(self, ) -> None:
    self.sigFunc = {
      TypeSig(int, int): funcIntInt,
      TypeSig(int)     : funcInt,
      TypeSig(str)     : funcStr,
    }
    self.sigIntInt = TypeSig(int, int)
    self.sigInt = TypeSig(int)
    self.sigStr = TypeSig(str)

  def test_dict_keys_in(self) -> None:
    """Tests that 'sigFunc' contains the expected keys."""
    self.assertIn(self.sigIntInt, self.sigFunc)
    self.assertIn(self.sigInt, self.sigFunc)
    self.assertIn(self.sigStr, self.sigFunc)

  def test_dict_getitem(self) -> None:
    """Tests that 'sigFunc' returns the expected functions."""
    self.assertIs(self.sigFunc[self.sigIntInt], funcIntInt)
    self.assertIs(self.sigFunc[self.sigInt], funcInt)
    self.assertIs(self.sigFunc[self.sigStr], funcStr)

  def test_from_args(self, ) -> None:
    """Tests that 'TypeSig.from_args' returns the expected function."""
    fromIntInt = TypeSig.fromArgs(69, 420)
    fromInt = TypeSig.fromArgs(1337)
    fromStr = TypeSig.fromArgs('lol')
    self.assertEqual(fromIntInt, self.sigIntInt)
    self.assertEqual(fromInt, self.sigInt)
    self.assertEqual(fromStr, self.sigStr)

  def test_coverage_gymnastics(self) -> None:
    self.assertEqual(len(self.sigIntInt), 2)
    self.assertEqual(len(self.sigInt), 1)
    self.assertEqual(len(self.sigStr), 1)

    self.assertEqual(69 + 420, self.sigFunc[self.sigIntInt](69, 420))
    self.assertEqual(1337, self.sigFunc[self.sigInt](1337))
    self.assertEqual('lol', self.sigFunc[self.sigStr]('lol'))

    for item in self.sigIntInt:
      self.assertIs(item, int)

    for item in self.sigInt:
      self.assertIs(item, int)

    for item in self.sigStr:
      self.assertIs(item, str)

    self.assertFalse(self.sigIntInt == 'breh')
    self.assertFalse(self.sigInt == 'breh')
    self.assertFalse(self.sigStr == 'breh')

    longSig = TypeSig.fromArgs(
      *stringList(
        """
            Never, gonna, give, you, up
            """,
      ),
    )

    self.assertFalse(self.sigIntInt == 'breh')
    self.assertFalse(self.sigInt == 'breh')
    self.assertFalse(self.sigStr == 'breh')

    self.assertFalse(self.sigIntInt == longSig)
    self.assertFalse(self.sigInt == longSig)
    self.assertFalse(self.sigStr == longSig)

    sigFloatFloat = TypeSig(float, float)
    sigFloat = TypeSig(float)

    self.assertFalse(self.sigIntInt == sigFloatFloat)
    self.assertFalse(self.sigInt == sigFloat)
    self.assertFalse(self.sigStr == sigFloat)

    self.assertIn(float, sigFloat)
    self.assertIn(float, sigFloatFloat)
    self.assertNotIn(int, sigFloat)
    self.assertNotIn(int, sigFloatFloat)

    self.assertGreater(len(str(sigFloatFloat)), len(str(sigFloat)))
    self.assertGreater(len(repr(sigFloatFloat)), len(repr(sigFloat)))

  def test_clone_fallback(self) -> None:
    """Tests that 'TypeSig.clone' returns a new instance."""

    class Parent:
      foo = Dispatcher()

      @foo.fallback
      def foo(self, *__, **_) -> str:
        return 'fallback'

    class Child(Parent):
      foo = Parent.__dict__['foo'].clone()

      @foo.overload(int, int, int)
      def foo(self, x: int, y: int, z: int) -> str:
        infoSpec = """%s(%d, %d, %d)"""
        info = infoSpec % (type(self).__name__, x, y, z)
        return textFmt(info)

    self.assertEqual(Parent().foo('breh'), 'fallback')
    self.assertEqual(Child().foo(69, 420, 1337), 'Child(69, 420, 1337)')

  def test_overload_call(self, ) -> None:
    """Tests that 'overload' created intermediate objects correctly raises
    TypeError when called."""

    def func() -> None:
      """Placeholder function."""

    sig = TypeSig(int, int)
    load = overload(sig, func)

    with self.assertRaises(TypeError):
      _ = load(69, 420)  # NOQA, it's okay pycharm, 'unreachable' i kno.

  def test_str_repr(self, ) -> None:
    """
    This method tests the '__str__' and '__repr__' methods on the
    'Dispatcher' class. Both names map to the same method.
    """
    self.assertIs(Dispatcher.__str__, Dispatcher.__repr__)
    z = Complex(69, 420)
    dispatcher = Dispatcher()
    actualStr = str(dispatcher)

  def test_complex(self, ) -> None:
    """
    Testing the 'Complex' class
    """

    z0 = Complex()
    z1 = Complex(z0)
    z2 = Complex(complex(69, 420))
    z3 = Complex(1337.)
    z4 = Complex(69, 420)
    z5 = Complex(69 + 420j, 1000000 + 1000000j)

    self.assertAlmostEqual(z0.realPart, 0.)
    self.assertAlmostEqual(z0.imagPart, 0.)
    self.assertAlmostEqual(z1.realPart, 0.)
    self.assertAlmostEqual(z1.imagPart, 0.)
    self.assertAlmostEqual(z2.realPart, 69.)
    self.assertAlmostEqual(z2.imagPart, 420.)
    self.assertAlmostEqual(z3.realPart, 1337.)
    self.assertAlmostEqual(z3.imagPart, 0.)
    self.assertAlmostEqual(z4.realPart, 69.)
    self.assertAlmostEqual(z4.imagPart, 420.)
    self.assertAlmostEqual(z5.realPart, 1000000 - 69.)
    self.assertAlmostEqual(z5.imagPart, 1000000 - 420.)

    self.assertIn('Complex', repr(z0))

    self.assertAlmostEqual(abs(Complex(3, 4)), 5.)
    self.assertTrue(Complex(3, 4))
    self.assertFalse(Complex())

    self.assertEqual(str(Complex()), '0')
    self.assertEqual(str(Complex(69)), '69.00')
    self.assertEqual(str(Complex(0, 420)), '420.00J')
    self.assertEqual(str(Complex(69, 420)), '69.00 + 420.00J')
    self.assertEqual(str(Complex(69, -420)), '69.00 - 420.00J')
    self.assertEqual(str(Complex(-69, -420)), '-69.00 - 420.00J')

    self.assertEqual(str(Complex(0, 1)), 'J')
    self.assertEqual(str(Complex(0, -1)), '-J')

    self.randomFloat.rowCount = 16
    self.randomFloat.colCount = 2
    for x, y in self.randomFloat.table:
      z0 = x + y * 1j
      z1 = complex(Complex(z0))
      self.assertEqual(z0, z1)

  def test_field_name_owner(self) -> None:
    """
    Testing the 'MissingVariable' exceptions raised by '_getFieldName' and
    '_getFieldOwner'.
    """
    dispatcher = Dispatcher()
    with self.assertRaises(MissingVariable) as context:
      dispatcher._getFieldName()
    e = context.exception
    self.assertEqual(e.varName, '__field_name__')
    self.assertIs(e.instance, dispatcher)
    self.assertIn(str, e.expectedTypes)
    with self.assertRaises(MissingVariable) as context:
      dispatcher._getFieldOwner()
    e = context.exception
    self.assertEqual(e.varName, '__field_owner__')
    self.assertIs(e.instance, dispatcher)
    self.assertIn(type, e.expectedTypes)

  def test_peek(self, ) -> None:
    """
    Testing the 'peeking' pattern.
    """

    class Foo:
      bar = Dispatcher()

    foo = Foo()
    setattr(foo, '__field_name__', 'foo')

    with self.assertRaises(RecursionError):
      Foo.__dict__['bar'].__get__(foo, object, _recursion=True)

    with self.assertRaises(RecursionError):
      Foo.__dict__['bar']._getCachedFunction(_recursion=True)

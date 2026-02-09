"""
TestDispatchUmbrella provides coverage gymnastics for the 'Dispatcher'
class from the 'worktoy.dispatch' module.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from types import FunctionType as Func
from types import MethodType as Meth
from typing import TYPE_CHECKING

from worktoy.waitaminute import TypeException, VariableNotNone
from worktoy.dispatch import Dispatcher, TypeSig, overload
from worktoy.waitaminute.desc import ReadOnlyError, ProtectedError
from . import DispatcherTest, ComplexNumber, PlanePoint
from . import SusComplex, ComplexMetaSub, SpacePoint

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestDispatchUmbrella(DispatcherTest):
  """
  TestDispatchUmbrella provides coverage gymnastics for the 'Dispatcher'
  class from the 'worktoy.dispatch' module.
  """

  def test_plane_point(self) -> None:
    """Test PlanePoint class"""
    p = PlanePoint(0.123456789)
    self.assertEqual(p.x, 0.123456789)
    self.assertEqual(p.y, 0.0)

  def test_hash_trolling(self) -> None:
    """Test hash trolling"""
    complexHash = TypeSig(complex)
    floatHash = TypeSig(float)

  def test_sus(self) -> None:
    """Test sus"""
    sus0 = SusComplex()
    sus1 = SusComplex(69.)
    sus2 = SusComplex(69.0, 420.0)
    z0 = ComplexMetaSub(sus0)
    z1 = ComplexMetaSub(sus1)
    z2 = ComplexMetaSub(sus2)
    self.assertEqual(z0.RE, complex(sus0).real)
    self.assertEqual(z0.IM, complex(sus0).imag)
    self.assertEqual(z1.RE, complex(sus1).real)
    self.assertEqual(z1.IM, complex(sus1).imag)
    self.assertEqual(z2.RE, complex(sus2).real)
    self.assertEqual(z2.IM, complex(sus2).imag)

  def test_plane_point_str_repr(self) -> None:
    """The final bit of coverage gymnastics for PlanePoint!"""
    p = PlanePoint(69, 420)
    self.assertEqual(str(p), repr(p))
    s = SpacePoint(69, 420, 1337)
    self.assertEqual(str(s), repr(s))

  def test_sig_func_map(self) -> None:
    """Test the sig func map"""
    sigFuncDict = ComplexNumber.__init__._getSigFuncMap()
    self.assertIsInstance(sigFuncDict, dict)

  def test_callback_setter(self) -> None:
    """Test the callback setter"""
    dispatcher = Dispatcher()
    self.assertIsNone(dispatcher._getFallbackFunction())
    with self.assertRaises(TypeException) as context:
      dispatcher.setFallbackFunction('breh')
    e = context.exception
    self.assertEqual(set(e.expectedTypes), {Func, Meth})
    self.assertEqual(e.varName, '__fallback_func__')
    self.assertEqual(e.actualObject, 'breh')
    self.assertIs(e.actualType, str)

    def breh() -> None:
      """breh"""

    dispatcher.setFallbackFunction(breh)
    dispatcher.setFinalizerFunction(breh)

    with self.assertRaises(VariableNotNone) as context:
      dispatcher.setFallbackFunction(breh)
    e = context.exception
    self.assertEqual(e.name, '__fallback_func__')
    self.assertIs(e.value, breh)

    with self.assertRaises(VariableNotNone) as context:
      dispatcher.setFinalizerFunction(breh)
    e = context.exception
    self.assertEqual(e.name, '__finalizer_func__')
    self.assertIs(e.value, breh)

    with self.assertRaises(TypeException) as context:
      dispatcher.setFallbackFunction('breh')
    e = context.exception
    self.assertEqual(set(e.expectedTypes), {Func, Meth})
    self.assertEqual(e.varName, '__fallback_func__')
    self.assertEqual(e.actualObject, 'breh')
    self.assertIs(e.actualType, str)

    with self.assertRaises(TypeException) as context:
      dispatcher.setFinalizerFunction('breh')
    e = context.exception
    self.assertEqual(set(e.expectedTypes), {Func, Meth})
    self.assertEqual(e.varName, '__finalizer_func__')
    self.assertEqual(e.actualObject, 'breh')
    self.assertIs(e.actualType, str)

  def test_bad_del_set(self) -> None:
    """Testing bad del and set"""

    class Foo:
      bar = Dispatcher()

    with self.assertRaises(ReadOnlyError):
      Foo().bar = 777

    with self.assertRaises(ProtectedError):
      del Foo().bar

    Foo.bar.clone()

  def test_no_finalize(self) -> None:
    class Foo:
      bar = Dispatcher()

      __inner_value__ = None

      @bar.overload(int, int)
      def bar(self, x: int, y: int) -> None:
        """Overloaded method for two integers."""
        self.__inner_value__ = str(x + y)

      @bar.overload(int)
      def bar(self, x: int) -> None:
        """Overloaded method for one integer."""
        self.__inner_value__ = str(x)

      @bar.fallback
      def bar(self, *args, **kwargs) -> None:
        """Fallback method for unsupported types."""
        self.__inner_value__ = '%s | %s' % (str(args, ), str(kwargs, ))

    foo = Foo()
    self.assertEqual(foo.bar(69, 420), None)
    self.assertEqual(foo.__inner_value__, '489')
    self.assertEqual(foo.bar(69), None)
    self.assertEqual(foo.__inner_value__, '69')
    foo.bar(69, 420, 1337, lmao=True)
    expected = """(69, 420, 1337) | {'lmao': True}"""
    self.assertEqual(foo.__inner_value__, expected)

  def test_fallback_get_attr(self) -> None:
    fb = overload.fallback(lambda *args, **kwargs: 'fallback')
    with self.assertRaises(AttributeError) as context:
      _ = fb.im_an_attribute_trust_me_bro

  def test_finalize(self) -> None:
    class Foo:
      bar = Dispatcher()

      __inner_value__ = None

      @bar.overload(int, int)
      def bar(self, x: int, y: int) -> None:
        """Overloaded method for two integers."""
        self.__inner_value__ = str(x + y)

      @bar.overload(int)
      def bar(self, x: int) -> None:
        """Overloaded method for one integer."""
        self.__inner_value__ = str(x)

      @bar.fallback
      def bar(self, *args, **kwargs) -> None:
        """Fallback method for unsupported types."""
        self.__inner_value__ = '%s | %s' % (str(args, ), str(kwargs, ))

      @bar.finalize
      def bar(self, *args, **kwargs) -> None:
        """Finalizer method for the bar method."""
        self.__inner_value__ = 'finalized: %s' % (self.__inner_value__,)

    foo = Foo()
    self.assertEqual(foo.bar(69, 420), None)
    self.assertEqual(foo.__inner_value__, 'finalized: 489')
    self.assertEqual(foo.bar(69), None)
    self.assertEqual(foo.__inner_value__, 'finalized: 69')
    foo.bar(69, 420, 1337, lmao=True)
    expected = """finalized: (69, 420, 1337) | {'lmao': True}"""
    self.assertEqual(foo.__inner_value__, expected)
    self.assertEqual(foo.bar(True, False), None)
    self.assertIn('finalized', foo.__inner_value__)
    self.assertEqual(foo.bar('never', 'gonna', 'give', 'you', 'up'), None)
    self.assertIn('finalized', foo.__inner_value__)

  def test_bad_finalizer(self) -> None:
    """Testing errors raised in finalizers"""

    class FinalizeError(Exception):
      pass

    class Foo:
      bar = Dispatcher()

      __inner_value__ = None

      @bar.overload(int, int)
      def bar(self, x: int, y: int) -> None:
        """Overloaded method for two integers."""
        self.__inner_value__ = str(x + y)

      @bar.overload(int)
      def bar(self, x: int) -> None:
        """Overloaded method for one integer."""
        self.__inner_value__ = str(x)

      @bar.overload(str)
      def bar(self, cmd: str) -> None:
        """Overloaded method for a string."""
        if cmd == 'raise':
          raise ValueError('This is a test error from the bar method.')
        self.__inner_value__ = cmd

      @bar.fallback
      def bar(self, *args, **kwargs) -> None:
        """Fallback method for unsupported types."""
        self.__inner_value__ = '%s | %s' % (str(args, ), str(kwargs, ))

      @bar.finalize
      def bar(self, *args, **kwargs) -> None:
        """Finalizer method for the bar method."""
        if 'finalRaise' in args or 'raise' in args:
          raise FinalizeError
        self.__inner_value__ = 'finalized: %s' % (self.__inner_value__,)

    foo = Foo()
    self.assertEqual(foo.bar(69, 420), None)
    self.assertEqual(foo.__inner_value__, 'finalized: 489')
    self.assertEqual(foo.bar(69), None)
    self.assertEqual(foo.__inner_value__, 'finalized: 69')
    foo.bar(69, 420, 1337, lmao=True)
    expected = """finalized: (69, 420, 1337) | {'lmao': True}"""
    self.assertEqual(foo.__inner_value__, expected)
    self.assertEqual(foo.bar(True, False), None)
    self.assertIn('finalized', foo.__inner_value__)
    self.assertEqual(foo.bar('never', 'gonna', 'give', 'you', 'up'), None)
    self.assertIn('finalized', foo.__inner_value__)

    with self.assertRaises(FinalizeError):
      foo.bar('finalRaise')

    with self.assertRaises(ValueError):
      foo.bar('raise')

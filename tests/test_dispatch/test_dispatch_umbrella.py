"""
TestDispatchUmbrella provides coverage gymnastics for the 'Dispatcher'
class from the 'worktoy.dispatch' module.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from types import FunctionType as Func
from types import MethodType

from worktoy.waitaminute import TypeException, VariableNotNone
from worktoy.dispatch import Dispatcher, TypeSig, overload
from worktoy.waitaminute.desc import ReadOnlyError, ProtectedError
from worktoy.waitaminute.dispatch import DuplicateSignature
from . import DispatcherTest
from .examples import SusComplex, ComplexMetaSub, SpacePoint
from .examples import ComplexNumber, PlanePoint


class TestDispatchUmbrella(DispatcherTest):
  """
  TestDispatchUmbrella provides coverage gymnastics for the 'Dispatcher'
  class from the 'worktoy.dispatch' module.
  """

  def test_plane_point(self) -> None:
    """Testing the PlanePoint example class."""
    p = PlanePoint(0.123456789)
    self.assertEqual(p.x, 0.123456789)
    self.assertEqual(p.y, 0.0)

  def test_sus(self) -> None:
    """Testing the SusComplex example class."""
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
    """Testing the sig func map"""
    sigFuncDict = ComplexNumber.__dict__['__init__']._getSigFuncMap()
    self.assertIsInstance(sigFuncDict, dict)

  def test_duplicate_signature(self) -> None:
    """Registering a second function under a 'TypeSig' that is
    already present must raise 'DuplicateSignature', carrying the
    colliding signature, the existing function, and the rejected
    duplicate."""
    dispatcher = Dispatcher()
    sig = TypeSig(int, str)

    # noinspection PyUnusedLocal
    def first(self_, x: int, s: str) -> None:
      """first function"""

    # noinspection PyUnusedLocal
    def second(self_, x: int, s: str) -> None:
      """second function"""

    self.assertIsNone(first(object(), 69, 'lol'))
    self.assertIsNone(second(object(), 69, 'lol'))

    # noinspection PyTypeChecker
    dispatcher.addSigFunc(sig, first)
    with self.assertRaises(DuplicateSignature) as context:
      # noinspection PyTypeChecker
      dispatcher.addSigFunc(sig, second)
    e = context.exception
    self.assertEqual(e.sig, sig)
    self.assertIs(e.existing, first)
    self.assertIs(e.duplicate, second)
    self.assertIn(str(sig), str(e))

  def test_callback_setter(self) -> None:
    """Testing the callback setter"""
    dispatcher = Dispatcher()
    self.assertIsNone(dispatcher._getFallbackFunction())
    with self.assertRaises(TypeException) as context:
      # noinspection PyTypeChecker
      dispatcher.setFallbackFunction('breh')
    e = context.exception
    self.assertEqual(set(e.expectedTypes), {Func, MethodType})
    self.assertEqual(e.varName, '__fallback_func__')
    self.assertEqual(e.actualObject, 'breh')
    self.assertIs(e.actualType, str)

    def breh() -> None:
      """breh"""

    # noinspection PyTypeChecker
    dispatcher.setFallbackFunction(breh)
    # noinspection PyTypeChecker
    dispatcher.setFinalizerFunction(breh)

    with self.assertRaises(VariableNotNone) as context:
      # noinspection PyTypeChecker
      dispatcher.setFallbackFunction(breh)
    e = context.exception
    self.assertEqual(e.name, '__fallback_func__')
    self.assertIs(e.value, breh)

    with self.assertRaises(VariableNotNone) as context:
      # noinspection PyTypeChecker
      dispatcher.setFinalizerFunction(breh)
    e = context.exception
    self.assertEqual(e.name, '__finalizer_func__')
    self.assertIs(e.value, breh)

    with self.assertRaises(TypeException) as context:
      # noinspection PyTypeChecker
      dispatcher.setFallbackFunction('breh')
    e = context.exception
    self.assertEqual(set(e.expectedTypes), {Func, MethodType})
    self.assertEqual(e.varName, '__fallback_func__')
    self.assertEqual(e.actualObject, 'breh')
    self.assertIs(e.actualType, str)

    with self.assertRaises(TypeException) as context:
      # noinspection PyTypeChecker
      dispatcher.setFinalizerFunction('breh')
    e = context.exception
    self.assertEqual(set(e.expectedTypes), {Func, MethodType})
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

    Foo.__dict__['bar'].clone()

  def test_clone_copies_state(self) -> None:
    """'Dispatcher.clone' must produce a 'Dispatcher' carrying the
    same registered signatures, fallback, and finalizer as the
    original. None of the per-class fields ('__field_name__',
    '__field_owner__', '__compiled_func__') should leak into the
    clone, since they only become meaningful once '__set_name__'
    fires on the clone's owning class."""
    original = Dispatcher()
    sig = TypeSig(int)

    def body(self_, x: int) -> None:
      """body"""

    def fallback(self_, *args, **kwargs) -> None:
      """fallback"""

    def finalizer(self_, *args, **kwargs) -> None:
      """finalizer"""

    # noinspection PyTypeChecker
    original.addSigFunc(sig, body)
    # noinspection PyTypeChecker
    original.setFallbackFunction(fallback)
    # noinspection PyTypeChecker
    original.setFinalizerFunction(finalizer)

    clone = original.clone()
    self.assertIsNot(clone, original)
    self.assertEqual(
        clone._getSigFuncList(), original._getSigFuncList(),
    )
    self.assertIs(clone._getFallbackFunction(), fallback)
    self.assertIs(clone._getFinalizerFunction(), finalizer)

  def test_clone_independence(self) -> None:
    """A 'Dispatcher' clone must be a genuine copy: subsequent
    registrations on the clone may not bleed back into the
    original, and vice versa. The clone also starts with an empty
    compiled-function cache so that its first dispatch through
    '_getCachedFunction' reflects its own state, not the
    original's snapshot."""

    def first(self_, x: int) -> None:
      """first"""

    def second(self_, x: int, y: int) -> None:
      """second"""

    original = Dispatcher()
    # noinspection PyTypeChecker
    original.addSigFunc(TypeSig(int), first)

    clone = original.clone()
    # noinspection PyTypeChecker
    clone.addSigFunc(TypeSig(int, int), second)

    originalSigs = [sig for sig, _ in original._getSigFuncList()]
    cloneSigs = [sig for sig, _ in clone._getSigFuncList()]
    self.assertEqual(originalSigs, [TypeSig(int)])
    self.assertEqual(cloneSigs, [TypeSig(int), TypeSig(int, int)])

    self.assertIsNone(original.__compiled_func__)
    self.assertIsNone(clone.__compiled_func__)

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
    with self.assertRaises(AttributeError):
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
      def bar(self, *__, **_) -> None:
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
      def bar(self, *args, **_) -> None:
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

    with self.assertRaises(FinalizeError) as context:
      foo.bar('raise')
    e = context.exception
    self.assertIsInstance(e.__cause__, ValueError)

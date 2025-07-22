"""
TestDispatchUmbrella provides coverage gymnastics for the 'Dispatcher'
class from the 'worktoy.dispatch' module.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from types import FunctionType as Func
from types import MethodType as Meth
from typing import TYPE_CHECKING

from worktoy.waitaminute import TypeException, VariableNotNone
from worktoy.dispatch import Dispatcher, TypeSig
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

    with self.assertRaises(VariableNotNone) as context:
      dispatcher.setFallbackFunction(breh)
    e = context.exception
    self.assertEqual(e.name, '__fallback_func__')
    self.assertIs(e.value, breh)

  def test_bad_del_set(self) -> None:
    """Testing bad del and set"""

    class Foo:
      bar = Dispatcher()

    with self.assertRaises(ReadOnlyError):
      Foo().bar = 777

    with self.assertRaises(ProtectedError):
      del Foo().bar

    Foo.bar.clone()

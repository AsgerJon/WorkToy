"""
TestDispatchUmbrella provides coverage gymnastics for the 'Dispatcher'
class from the 'worktoy.dispatch' module.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core.sentinels import FALLBACK, WILDCARD
from worktoy.desc import AttriBox
from worktoy.waitaminute.dispatch import CastMismatch
from worktoy.waitaminute.meta import ReservedName
from worktoy.dispatch import Dispatcher, TypeSignature

from . import DispatcherTest, ComplexSubclass, ComplexNumber, PlanePoint, \
  SusComplex, ComplexMetaSub, SpacePoint

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Callable, Dict, Optional, TypeAlias, Self


class TestDispatchUmbrella(DispatcherTest):
  """
  TestDispatchUmbrella provides coverage gymnastics for the 'Dispatcher'
  class from the 'worktoy.dispatch' module.
  """

  def test_recursion_is_wild(self) -> None:
    """Test recursion is wild"""
    with self.assertRaises(RecursionError):
      sig = TypeSignature(int, int, int, int)
      sig._getIsWild(_recursion=True)

  def test_swap_no_types(self) -> None:
    """Test swap no types"""
    with self.assertRaises(ValueError) as context:
      TypeSignature().swapType()
    e = context.exception
    self.assertIn('No types provided to swap.', str(e))
    with self.assertRaises(ValueError) as context:
      TypeSignature().swapType(int, float, complex)
    e = context.exception
    self.assertIn('Too many types provided to swap, expected', str(e))

    class A:
      pass

    class B(A):
      pass

    sig = TypeSignature(A, int, float).swapType(B)
    for i, j in zip(sig, (B, int, float)):
      self.assertIs(i, j)

  def test_wilder(self) -> None:
    """Test catching the wild signature"""
    z = ComplexSubclass(69 + 420j, 'breh', )
    self.assertEqual(z.__test_notes__, ('breh',))

    with self.assertRaises(NotImplementedError):
      _ = TypeSignature(FALLBACK, FALLBACK, FALLBACK, FALLBACK)

    wild = TypeSignature(WILDCARD, WILDCARD, WILDCARD, WILDCARD)
    self.assertTrue(wild.isWild)

  def test_calm(self) -> None:
    """Test calm signature"""

    class PointCalm:
      __init__ = Dispatcher()

      @__init__.overload(float, float)
      def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

      @__init__.overload(complex)
      def __init__(self, x: complex) -> None:
        self.x = x.real
        self.y = x.imag

      @__init__.overload()
      def __init__(self) -> None:
        self.x = 0.0
        self.y = 0.0

    point = PointCalm(69 + 420j)
    self.assertEqual(point.x, 69.0)
    self.assertEqual(point.y, 420.0)
    point = PointCalm(69., 420.)
    self.assertEqual(point.x, 69.0)
    self.assertEqual(point.y, 420.0)
    point = PointCalm()
    self.assertEqual(point.x, 0.0)
    self.assertEqual(point.y, 0.0)

    class PointWild:
      __init__ = Dispatcher()
      x = AttriBox[float](0.0)
      y = AttriBox[float](0.0)

      @__init__.overload(float, float)
      def __init__(self, x: float, y: float, *_) -> None:
        self.x = x
        self.y = y

      @__init__.overload(WILDCARD)
      def __init__(self, *args) -> None:
        self.__test_notes__ = args

      @__init__.overload()
      def __init__(self, *args) -> None:
        self.x = 0.0
        self.y = 0.0

      @__init__.overload(FALLBACK)
      def __init__(self, *args) -> None:
        self.__test_notes__ = 'fallback'

    point = PointWild(69., 420.)
    self.assertEqual(point.x, 69.0)
    self.assertEqual(point.y, 420.0)
    point = PointWild(object)
    self.assertEqual(point.__test_notes__, (object,))
    point = PointWild()
    self.assertEqual(point.x, 0.0)
    self.assertEqual(point.y, 0.0)
    point = PointWild(object, object)
    self.assertEqual(point.__test_notes__, 'fallback')

  def test_plane_point(self) -> None:
    """Test PlanePoint class"""
    p = PlanePoint(0.123456789)
    self.assertEqual(p.x, 0.123456789)
    self.assertEqual(p.y, 0.0)

  def test_hash_trolling(self) -> None:
    """Test hash trolling"""
    complexHash = TypeSignature(complex)
    floatHash = TypeSignature(float)

  def test_cast_mismatch(self) -> None:
    """Test hash mismatch"""
    sig = TypeSignature(int, int, WILDCARD)
    with self.assertRaises(CastMismatch) as context:
      sig.cast(['smoke this lol!', ])
    e = context.exception
    self.assertIs(e.sig, sig)
    self.assertEqual(e.args, (['smoke this lol!', ],))
    self.assertEqual(str(e), repr(e))

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

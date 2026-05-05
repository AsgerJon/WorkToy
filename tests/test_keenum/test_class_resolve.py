"""
TestClassResolve subclasses 'KeeTest' from the 'tests.test_keenum' package
and tests 'KeeNum' enumerations implementing the '__class_resolve__'.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.keenum import KeeNum, Kee
from worktoy.waitaminute.keenum import KeeResolveError
from . import KeeTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class TestClassResolve(KeeTest):
  """
  TestClassResolve subclasses 'KeeTest' from the 'tests.test_keenum' package
  and tests 'KeeNum' enumerations implementing the '__class_resolve__'.
  """

  def test_class_resolve_returning_not_implemented(self) -> None:
    """
    Test that a 'KeeNum' enumeration implementing the '__class_resolve__'
    method that raises 'KeeResolveError' is properly handled by the
    'KeeMeta' metaclass and that the fallback resolvers are attempted.
    """

    class Cardinal(KeeNum):
      NORTH = Kee[complex](1j)
      WEST = Kee[complex](-1)
      SOUTH = Kee[complex](-1j)
      EAST = Kee[complex](1)

      @classmethod
      def __class_resolve__(cls, identifier: Any) -> Any:
        if isinstance(identifier, tuple):
          return identifier[0]
        return NotImplemented

    self.assertIs(Cardinal.NORTH, Cardinal((Cardinal.NORTH,)))
    self.assertIs(Cardinal.WEST, Cardinal((Cardinal.WEST,)))
    self.assertIs(Cardinal.SOUTH, Cardinal((Cardinal.SOUTH,)))
    self.assertIs(Cardinal.EAST, Cardinal((Cardinal.EAST,)))
    with self.assertRaises(KeeResolveError) as context:
      _ = Cardinal(69 + 420j)
    e = context.exception
    self.assertIs(e.keeNum, Cardinal)
    self.assertEqual(e.identifier, 69 + 420j)

    with self.assertRaises(KeeResolveError) as context:
      _ = Cardinal(object())
    e = context.exception
    self.assertIs(e.keeNum, Cardinal)

    with self.assertRaises(KeeResolveError) as context:
      _ = Cardinal.fromValue(69 + 420j)
    e = context.exception
    self.assertIs(e.keeNum, Cardinal)
    self.assertEqual(e.identifier, 69 + 420j)

  def test_class_resolve_int(self) -> None:
    """
    This method tests the '__class_resolve__' method of a 'KeeNum'
    enumeration with 'valueType' of 'int'.
    """

    class Sus(KeeNum):
      A = Kee[int](1)
      B = Kee[int](2)
      C = Kee[int](3)

      @classmethod
      def __class_resolve__(cls, identifier: Any) -> Any:
        return NotImplemented

    self.assertIs(Sus.A, Sus[0])
    self.assertIs(Sus.B, Sus[1])
    self.assertIs(Sus.C, Sus[2])

    with self.assertRaises(KeeResolveError) as context:
      _ = Sus(69 + 420j)
    e = context.exception
    self.assertIs(e.keeNum, Sus)
    self.assertEqual(e.identifier, 69 + 420j)

  def test_polar_bool(self, ) -> None:
    """
    This method tests the '__class_resolve__' method of a 'KeeNum'
    enumeration with 'valueType' of 'bool'.
    """

    class Polar(KeeNum):
      OUI = Kee[bool](True)
      NO = Kee[bool](False)

      @classmethod
      def __class_resolve__(cls, identifier: Any) -> Any:
        if isinstance(identifier, bool):
          return cls.OUI if identifier else cls.NO
        return NotImplemented

    self.assertIs(Polar.OUI, Polar(True))
    self.assertIs(Polar.NO, Polar(False))
    self.assertIs(Polar.__class_resolve__(object()), NotImplemented)
    self.assertIs(Polar.__class_resolve__(69 + 420j), NotImplemented)

    with self.assertRaises(KeeResolveError) as context:
      _ = Polar(69 + 420j)
    e = context.exception
    self.assertIs(e.keeNum, Polar)
    self.assertEqual(e.identifier, 69 + 420j)

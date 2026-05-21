"""
TestKeeMeta subclasses 'KeeTest' from the 'tests.test_keenum' package and
tests the 'KeeMeta' metaclass. These tes
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.keenum import KeeNum, KeeSpace, Kee, KeeMeta
from worktoy.waitaminute import TypeException
from . import KeeTest
from .examples import WeekDay, RGBNum, Point3D

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestKeeMeta(KeeTest):
  """
  TestKeeMeta subclasses 'KeeTest' from the 'tests.test_keenum' package and
  tests the 'KeeMeta' metaclass. These tes
  """

  def test_good_get_base(self, ) -> None:
    """
    Test that 'KeeMeta.get_base' properly returns the base class of a
    'KeeNum' enumeration.
    """

    class Them(KeeNum):
      TOM = Kee[int](69)
      DICK = Kee[int](420)
      HARRY = Kee[int](1337)

    class Monochrome(KeeNum):
      WHITE = Kee[str]("""#FFFFFF""")
      GRAY = Kee[str]("""#888888""")
      BLACK = Kee[str]("""#000000""")

    class RGB(Monochrome):
      RED = Kee[str]("""#FF0000""")
      GREEN = Kee[str]("""#00FF00""")
      BLUE = Kee[str]("""#0000FF""")

    self.assertIs(Them.base, Them)
    self.assertIs(Monochrome.base, Monochrome)
    self.assertIs(RGB.base, Monochrome)

  def test_good_space(self) -> None:
    """
    Covers namespace of good type
    """

    class Sus(KeeNum):
      TOM = Kee[Point3D](1., 2., 3.)
      DICK = Kee[Point3D](4., 5., 6.)
      HARRY = Kee[Point3D](7., 8., 9., )

    type.__setattr__(Sus, '__name_space__', None)

    with self.assertRaises(RecursionError):
      _ = Sus._getSpace(_recursion=True)

    self.assertIsInstance(Sus.space, KeeSpace)

  def test_space_bad_type(self) -> None:
    """
    Covers namespace of bad type
    """

    class Sus(KeeNum):
      pass

    type.__setattr__(Sus, '__namespace__', dict())
    type.__setattr__(Sus, '__name_space__', None)

    with self.assertRaises(TypeException) as context:
      _ = Sus.space
    e = context.exception
    self.assertEqual(e.varName, '__namespace__')
    self.assertIs(e.actualObject, getattr(Sus, '__namespace__'))
    self.assertIs(e.actualType, dict)
    self.assertIn(KeeSpace, e.expectedTypes)

    self.assertAlmostEqual(abs(Point3D(1., 2., 2.)), 3.)

  def test_too_many_bases(self, ) -> None:
    """
    This method tests the situation where a 'KeeMeta' has too many or not
    enough bases.
    """

    class Sus(KeeNum):
      pass

    with self.assertRaises(ValueError):
      # noinspection PyUnusedLocal
      class Eggs(WeekDay, Sus):
        pass

    with self.assertRaises(ValueError):
      # noinspection PyUnusedLocal
      class Ham(metaclass=KeeMeta):
        pass

  def test_good_base(self, ) -> None:
    """
    This method tests the situation where a 'KeeMeta' has a good base.
    """

    class Sus(KeeNum):
      pass

    type.__setattr__(Sus, '__base_class__', None)

    with self.assertRaises(RecursionError):
      _ = Sus._getBase(_recursion=True)

    self.assertIs(Sus.base, Sus)

  def test_good_members(self, ) -> None:
    """
    This method tests the situation where a 'KeeMeta' has good members.
    """

    class Sus(KeeNum):
      pass

    type.__setattr__(Sus, '__registered_members__', None)

    with self.assertRaises(RecursionError):
      _ = Sus._getMembers(_recursion=True)

    self.assertFalse(Sus)

  def test_named_members(self, ) -> None:
    """
    This method tests the situation where a 'KeeMeta' has good named members.
    """

    type.__setattr__(RGBNum, '__named_members__', None)

    namedColors = RGBNum.namedMembers
    for color in RGBNum:
      fromName = namedColors[color.name.lower()]
      self.assertIs(color, fromName)

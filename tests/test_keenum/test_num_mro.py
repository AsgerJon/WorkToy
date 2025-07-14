"""
TestNumMRO tests the MRO (Method Resolution Order) of the KeeNum
enumerations by chaining a series of color enumerating classes.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.keenum._kee_desc import AbstractKeeDesc
from worktoy.waitaminute.keenum import KeeValueError, KeeTypeException
from . import KeeTest, RGB, RootRGB, MoreRGB, EvenMoreRGB, RGBNum
from worktoy.keenum import KeeNum, Kee, KeeMeta

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class TestNumMRO(KeeTest):
  """
  TestNumMRO tests the MRO (Method Resolution Order) of the KeeNum
  enumerations by chaining a series of color enumerating classes.
  """

  def test_mro(self) -> None:
    """
    Test the MRO of the RGBNum class.
    """
    for color in RootRGB:
      self.assertIs(getattr(MoreRGB, color.name), color)
      self.assertIs(getattr(EvenMoreRGB, color.name), color)
      self.assertIs(getattr(RGBNum, color.name), color)
    for color in MoreRGB:
      self.assertIs(getattr(EvenMoreRGB, color.name), color)
      self.assertIs(getattr(RGBNum, color.name), color)
    for color in EvenMoreRGB:
      self.assertIs(getattr(RGBNum, color.name), color)

  def test_color_keys(self) -> None:
    """Test that instances of RGBNum can be used as dictionary keys and
    that RED from any of the color enumerations finds the same entry in
    the dict."""
    color_dict: dict[RootRGB, Any] = {}
    for color in RGBNum:
      color_dict[color] = color

    for key, val in color_dict.items():
      self.assertIs(key, val)

  def test_coverage_gymnastics(self) -> None:
    """Test that the MRO descriptor works as expected."""
    self.assertIsInstance(KeeMeta.members, AbstractKeeDesc)
    self.assertIn('#FF0000', str(RGBNum.RED.value))
    self.assertIn('#00FF00', str(RGBNum.GREEN.value))
    self.assertIn('#0000FF', str(RGBNum.BLUE.value))

  def test_repr(self) -> None:
    """Test that the repr of RGBNum is as expected."""
    redExpected = 'RGB(255, 0, 0)'
    greenExpected = 'RGB(0, 255, 0)'
    blueExpected = 'RGB(0, 0, 255)'
    self.assertEqual(repr(RGBNum.RED.value), redExpected)
    self.assertEqual(repr(RGBNum.GREEN.value), greenExpected)
    self.assertEqual(repr(RGBNum.BLUE.value), blueExpected)

  def test_index(self) -> None:
    """Test that the index of the members is as expected."""
    for i, color in enumerate(RGBNum):
      self.assertEqual(color.index, i)
      self.assertEqual(int(color), i)
      self.assertIs(color, RGBNum[color.name])
      self.assertIs(color, RGBNum[i])

  def test_resolve_index(self) -> None:
    """Test that the resolve_index method works as expected."""
    for i, color in enumerate(RGBNum):
      self.assertIs(RGBNum[i], color)
      self.assertIs(RGBNum(i), color)

  def test_resolve_key(self) -> None:
    """Test that the resolve_key method works as expected."""
    for color in RGBNum:
      self.assertIs(RGBNum[color.name], color)
      self.assertIs(RGBNum(color.name), color)

  def test_base(self) -> None:
    """Tests the 'base' property of the RGBNum class."""
    self.assertIs(RGBNum.base, EvenMoreRGB)
    self.assertIs(EvenMoreRGB.base, MoreRGB)
    self.assertIs(MoreRGB.base, RootRGB)
    self.assertIs(type(RGBNum), KeeMeta)

  def test_mro_num(self) -> None:
    """Test the MRO of the RGBNum class."""
    for cls in RGBNum.mroNum:
      for item in cls.mroNum:
        self.assertIn(item, RGBNum.mroNum)
    self.assertFalse(KeeNum.mroNum)

  def test_identity(self, ) -> None:
    """Test that the identity of the members is as expected."""

    for keenum in RGBNum.mroNum:
      for num in keenum:
        for nextKeenum in RGBNum.mroNum:
          if hasattr(nextKeenum, num.name):
            self.assertIs(getattr(nextKeenum, num.name), num)

  def test_good_resolve_value(self) -> None:
    """Test that the resolve_value method works as expected."""

    for color in RGBNum:
      self.assertIs(RGBNum.fromValue(color.value), color)

  def test_bad_resolve_value(self) -> None:
    """Test that the resolve_value method raises an error for invalid
    values."""

    for color in RGBNum:
      with self.assertRaises(KeeValueError) as context:
        _ = RGBNum.fromValue('bro imma color, trust!')
      e = context.exception
      self.assertIs(e.keenum, RGBNum)
      self.assertEqual(e.value, 'bro imma color, trust!')
      self.assertEqual(str(e), repr(e))

  def test_bad_member_type(self) -> None:
    """Test that passing a member with a value of an unsupported type
    raises a KeeTypeException. """
    with self.assertRaises(KeeTypeException) as context:
      class Breh(KeeNum):
        A = Kee[int](69)
        B = Kee[RGB](69, 420, 1337)
    e = context.exception
    self.assertEqual(e.name, 'B')
    self.assertEqual(e.value, RGB(69, 420, 1337))
    self.assertEqual(set(e.expectedTypes), {int, })
    self.assertEqual(str(e), repr(e))

  def test_bad_case(self) -> None:
    """Test that the case of the member names is preserved."""
   
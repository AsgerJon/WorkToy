"""
TestNumMRO tests the MRO (Method Resolution Order) of the KeeNum
enumerations by chaining a series of color enumerating classes.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING
from collections.abc import Callable

from worktoy.keenum import KeeNum, Kee, KeeMeta
from worktoy.waitaminute import TypeException
from worktoy.waitaminute.keenum import KeeTypeException, KeeResolveError
from . import KeeTest
from .examples import RGB, RootRGB, MoreRGB, EvenMoreRGB, RGBNum

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class TestNumMRO(KeeTest):
  """
  TestNumMRO tests the MRO (Method Resolution Order) of the KeeNum
  enumerations by chaining a series of color enumerating classes.
  """

  def test_mro(self) -> None:
    """
    Testing the MRO of the RGBNum class.
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
    """Testing that instances of RGBNum can be used as dictionary keys and
    that RED from any of the color enumerations finds the same entry in
    the dict."""
    color_dict: dict[RootRGB, Any] = {}
    for color in RGBNum:
      color_dict[color] = color

    for key, val in color_dict.items():
      self.assertIs(key, val)

  def test_coverage_gymnastics(self) -> None:
    """Testing that the MRO descriptor works as expected."""
    self.assertIn('#FF0000', str(RGBNum.RED.value))
    self.assertIn('#00FF00', str(RGBNum.GREEN.value))
    self.assertIn('#0000FF', str(RGBNum.BLUE.value))

  def test_repr(self) -> None:
    """Testing that the repr of RGBNum is as expected."""
    redExpected = 'RGB(255, 0, 0)'
    greenExpected = 'RGB(0, 255, 0)'
    blueExpected = 'RGB(0, 0, 255)'
    self.assertEqual(repr(RGBNum.RED.value), redExpected)
    self.assertEqual(repr(RGBNum.GREEN.value), greenExpected)
    self.assertEqual(repr(RGBNum.BLUE.value), blueExpected)

  def test_index(self) -> None:
    """Testing that the index of the members is as expected."""
    for i, color in enumerate(RGBNum):
      self.assertEqual(int(color), i)
      self.assertIs(color, RGBNum[color.name])
      self.assertIs(color, RGBNum[i])

  def test_resolve_index(self) -> None:
    """Testing that the resolve_index method works as expected."""
    for i, color in enumerate(RGBNum):
      self.assertIs(RGBNum[i], color)

  def test_resolve_key(self) -> None:
    """Testing that the resolve_key method works as expected."""
    for color in RGBNum:
      resolved = RGBNum(color.name)
      self.assertIs(resolved, color)

  def test_base(self) -> None:
    """Tests the 'base' property of the RGBNum class."""
    self.assertIs(RGBNum.base, EvenMoreRGB)
    self.assertIs(EvenMoreRGB.base, MoreRGB)
    self.assertIs(MoreRGB.base, RootRGB)
    self.assertIs(type(RGBNum), KeeMeta)

  def test_mro_num(self) -> None:
    """Testing the MRO of the RGBNum class."""
    for cls in RGBNum.mroNum:
      for item in cls.mroNum:
        self.assertIn(item, RGBNum.mroNum)
    self.assertFalse(KeeNum.mroNum)

  def test_identity(self, ) -> None:
    """Testing that the identity of the members is as expected."""

    for keenum in RGBNum.mroNum:
      for num in keenum:
        for nextKeenum in RGBNum.mroNum:
          if hasattr(nextKeenum, num.name):
            self.assertIs(getattr(nextKeenum, num.name), num)

  def test_good_resolve_value(self) -> None:
    """Testing that the resolve_value method works as expected."""

    for color in RGBNum:
      self.assertIs(RGBNum.fromValue(color.value), color)

  def test_bad_resolve_value(self) -> None:
    """Testing that the resolve_value method raises an error for invalid
    values."""

    with self.assertRaises(TypeException) as context:
      _ = RGBNum.fromValue('bro imma color, trust!')
    e = context.exception
    self.assertEqual(e.varName, 'value')
    self.assertEqual(e.actualObject, 'bro imma color, trust!')
    self.assertIs(e.actualType, str)
    self.assertIn(RGBNum.valueType, e.expectedTypes)

  def test_bad_member_type(self) -> None:
    """Testing that passing a member with a value of an unsupported type
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

  def test_named_members_recursion(self, ) -> None:
    """
    This method tests the recursion of the 'namedMembers' descriptor.
    """

    class Foo(KeeNum):
      pass

    setattr(Foo, '__named_members__', None)

    with self.assertRaises(RecursionError):
      _ = Foo._getNamedMembers(_recursion=True)

  def test_call_empty(self, ) -> None:
    """
    This method tests that calling a KeeNum with no arguments raises
    'TypeException'.
    """
    with self.assertRaises(TypeException) as context:
      _ = RGBNum()  # noqa
    e = context.exception
    self.assertEqual(e.varName, 'identifier')
    self.assertIsNone(e.actualObject)
    self.assertIs(e.actualType, type(None))
    self.assertIn(object, e.expectedTypes)

  def test_contains(self, ) -> None:
    """
    This method tests the '__contains__' method of the RGBNum class.
    """

    class Sus(KeeNum):
      A = Kee[int](69)

    self.assertFalse(KeeNum in Sus)
    self.assertFalse(Sus in KeeNum)

  def test_bool(self, ) -> None:
    """
    This method tests the '__bool__' method of the RGBNum class.
    """

    class Empty(KeeNum):
      pass

    class Some(KeeNum):
      A = Kee[int](69)

    self.assertFalse(Empty)
    self.assertFalse(KeeNum)
    self.assertTrue(Some)

  def test_bad_class_resolve_implementation(self, ) -> None:
    """
    This method covers the case of 'KeeNum' class having a bad
    '__class_resolve__'.
    """
    with self.assertRaises(TypeException) as context:
      class Sus(KeeNum):
        A = Kee[int](69)
        __class_resolve__ = 'never', 'gonna', 'give', 'you', 'up'
    e = context.exception
    self.assertEqual(e.varName, '__class_resolve__')
    self.assertEqual(e.actualObject, ('never', 'gonna', 'give', 'you', 'up'))
    self.assertIs(e.actualType, tuple)
    self.assertIn(Callable, e.expectedTypes)

  def test_resolve_bool(self, ) -> None:
    """
    This method tests the 'resolve_bool' method of the RGBNum class.
    """

    class Sus(KeeNum):
      A = Kee[int](69)

    with self.assertRaises(KeeResolveError) as context:
      _ = Sus[True]
    e = context.exception
    self.assertIs(e.keeNum, Sus)
    self.assertIs(e.identifier, True)

    class Polar(KeeNum):
      YES = Kee[bool](True)
      NO = Kee[bool](False)

    self.assertIs(Polar[True], Polar.YES)
    self.assertIs(Polar[False], Polar.NO)

  def test_inheritance(self, ) -> None:
    """
    This method tests that the MRO of the RGBNum class is as expected.
    """

    colorNums = (RootRGB, MoreRGB, EvenMoreRGB, RGBNum)
    for i, num in enumerate(colorNums):
      for element in num:
        for nextNum in colorNums[i + 1:]:
          nextElement = getattr(nextNum, element.name)
          self.assertIs(element, nextElement)

  def test_members(self, ) -> None:
    """
    This method tests that the members of the RGBNum class are as expected.
    """
    colorNums = (RootRGB, MoreRGB, EvenMoreRGB, RGBNum,)

    for i, element in (*enumerate(RGBNum), *((69420, KeeNum),)):
      if i < len(RGBNum):
        self.assertEqual(element.index, i)
        self.assertEqual(element.kee.index, i)
        self.assertEqual(int(element.kee), i)
      for num in colorNums:
        if i < len(num):
          expectedName = """%s.%s""" % (num.__name__, element.name)
          actualName = str(element)
          self.assertEqual(actualName, expectedName)
          break  # test only the first match

  def test_bad_members(self) -> None:
    """
    This method tests that the members of the RGBNum class are as expected.
    """

    class Sus(KeeNum):
      pass

    type.__setattr__(Sus, '__registered_members__', None)

    with self.assertRaises(RecursionError):
      _ = Sus._getMembers(_recursion=True)

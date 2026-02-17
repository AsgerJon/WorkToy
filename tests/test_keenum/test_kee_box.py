"""
TestKeeBox tests the 'KeeBox' subclass of 'AttriBox' specially tailored
for boxing up enumerations.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.desc import AttriBox
from worktoy.ezdata import EZMeta, EZData
from worktoy.mcls import BaseObject
from worktoy.utilities.mathematics import pi
from worktoy.utilities.mathematics import e as exp1
from worktoy.waitaminute import TypeException
from worktoy.waitaminute.dispatch import DispatchException
from worktoy.waitaminute.keenum import KeeBoxException, \
  KeeBoxValueError, KeeBoxTypeError
from . import KeeTest
from .examples import Pen, RGB, ColorNum
from worktoy.keenum import KeeBox, KeeNum, KeeMeta, KeeFlag, KeeFlags, \
  KeeFlagsMeta, Kee

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestKeeBox(KeeTest):
  """
  TestKeeBox tests the 'KeeBox' subclass of 'AttriBox' specially tailored
  for boxing up enumerations.
  """

  def setUp(self, ) -> None:
    super().setUp()

    self.penSamples = Pen.fullSample()

  def test_init(self, ) -> None:
    """
    Testing that 'Pen' objects instantiate correctly.
    """

    for pen in self.penSamples:
      self.assertIsInstance(pen, Pen)
      self.assertIsInstance(pen.color, ColorNum)
      self.assertIsInstance(pen.color.value, RGB)
      self.assertIsInstance(pen.width, int)

  def test_class(self, ) -> None:
    """
    Testing the class attributes of 'Pen'.
    """
    self.assertIsInstance(Pen.color, KeeBox)
    self.assertIsInstance(Pen.color.fieldType, KeeMeta)
    self.assertIsSubclass(Pen.color.fieldType, KeeNum)
    self.assertIsInstance(Pen.color.fieldType.valueType, EZMeta)
    self.assertIsSubclass(Pen.color.fieldType.valueType, EZData)
    self.assertIsInstance(Pen.width, AttriBox)
    self.assertIsInstance(Pen.width.fieldType, type)
    self.assertIs(Pen.width.fieldType, int)

  def test_bad_init(self, ) -> None:
    """
    Testing that 'Pen' raises 'DispatchException' when instantiated with
    bad arguments.
    """
    with self.assertRaises(DispatchException) as context:
      _ = Pen('never', 'gonna', 'give', 'you', 'up')
    e = context.exception
    self.assertIs(e.dispatch, Pen.__init__)
    self.assertEqual(e.args, ('never', 'gonna', 'give', 'you', 'up'))

  def test_good_set(self, ) -> None:
    """
    Testing that 'Pen' objects can be set with type-accurate values.
    """
    pen = Pen(ColorNum.RED, 4)
    self.assertIs(pen.color, ColorNum.RED)
    for color in ColorNum:
      pen.color = color
      self.assertIs(pen.color, color)
    for width in range(1, 10):
      pen.width = width
      self.assertEqual(pen.width, width)

  def test_flex_init(self, ) -> None:
    """
    Tests that 'KeeBox' can resolve from different arguments besides the
    exact type.
    """

    redRGB = RGB(255, 0, 0)

    class SprayCan(BaseObject):
      indexColor = KeeBox[ColorNum](0)  # From index -> ColorNum.RED
      nameColor = KeeBox[ColorNum]('red')  # Case flex
      valueColor = KeeBox[ColorNum](redRGB)  # From value -> ColorNum.RED
      valueArgColor = KeeBox[ColorNum](255, 0, 0)
      badValueColor = KeeBox[ColorNum](69, 420, 1337)
      #  Does result in a valid 'RGB' object, but not a member of the
      #  'ColorNum' enumeration. Should raise 'KeeValueError' when trying
      #  to resolve.

    self.assertIsInstance(SprayCan.indexColor, KeeBox)
    self.assertIsInstance(SprayCan.indexColor.fieldType, KeeMeta)
    self.assertIsSubclass(SprayCan.indexColor.fieldType, KeeNum)
    self.assertIsInstance(SprayCan.indexColor.fieldType.valueType, EZMeta)
    self.assertIsSubclass(SprayCan.indexColor.fieldType.valueType, EZData)

    sprayCan = SprayCan()
    self.assertIs(sprayCan.indexColor, ColorNum.RED)
    self.assertIsInstance(sprayCan.indexColor.value, RGB)
    self.assertEqual(sprayCan.indexColor.value.r, 255)
    self.assertEqual(sprayCan.indexColor.value.g, 0)
    self.assertEqual(sprayCan.indexColor.value.b, 0)

    self.assertIs(sprayCan.nameColor, ColorNum.RED)
    self.assertIsInstance(sprayCan.nameColor.value, RGB)
    self.assertEqual(sprayCan.nameColor.value.r, 255)
    self.assertEqual(sprayCan.nameColor.value.g, 0)
    self.assertEqual(sprayCan.nameColor.value.b, 0)

    self.assertIs(sprayCan.valueColor, ColorNum.RED)
    self.assertIsInstance(sprayCan.valueColor.value, RGB)
    self.assertEqual(sprayCan.valueColor.value.r, 255)
    self.assertEqual(sprayCan.valueColor.value.g, 0)
    self.assertEqual(sprayCan.valueColor.value.b, 0)

    self.assertIs(sprayCan.valueArgColor, ColorNum.RED)
    self.assertIsInstance(sprayCan.valueArgColor.value, RGB)
    self.assertEqual(sprayCan.valueArgColor.value.r, 255)
    self.assertEqual(sprayCan.valueArgColor.value.g, 0)
    self.assertEqual(sprayCan.valueArgColor.value.b, 0)

    with self.assertRaises(KeeBoxValueError) as context:
      _ = sprayCan.badValueColor
    e = context.exception
    self.assertIs(e.desc, SprayCan.badValueColor)
    self.assertIs(e.num, ColorNum)
    self.assertEqual(e.value, RGB(69, 420, 1337))

  def test_pen(self, ) -> None:
    """
    Tests that 'Pen' objects can be instantiated and set as intended.
    """

    colorNumPen = Pen(ColorNum.GREEN)
    self.assertIs(colorNumPen.color, ColorNum.GREEN)
    intPen = Pen(1)
    self.assertIs(intPen.width, 1)
    thisPen = Pen(intPen, )
    self.assertIs(thisPen.color, intPen.color)
    blankPen = Pen()
    self.assertIs(blankPen.color, ColorNum.YELLOW)
    self.assertIs(blankPen.width, 1)
    for pen in (*Pen.rands(7), *Pen.rands(), Pen.rand()):
      self.assertIsInstance(pen, Pen)
      self.assertIsInstance(pen.color, ColorNum)
      self.assertIsInstance(pen.width, int)

  def test_gymnastics(self) -> None:
    """
    Covering edge cases
    """

    class Bar:
      foo = KeeBox[ColorNum](0)

    bar = Bar()
    with self.assertRaises(RecursionError):
      Bar.foo.__get__(bar, Bar, _recursion=True)

  def test_box_of_flags(self, ) -> None:
    """
    Tests that 'KeeBox' can be used to box up 'Flag' enumerations.
    """

    class EF(KeeFlags):  # ExampleFlags, but shortened
      A = KeeFlag()
      B = KeeFlag()
      C = KeeFlag()
      D = KeeFlag()
      E = KeeFlag()

    class Foo:
      bar = KeeBox[EF]('A', 'B', 'C')

    foo = Foo()
    self.assertIs(foo.bar, EF.A | EF.B | EF.C)

  def test_bad_box(self, ) -> None:
    """
    Tests that 'KeeBox' raises 'KeeBoxException' when given a field type
    that is not a 'KeeMeta' or 'KeeFlagsMeta'.
    """

    with self.assertRaises(TypeException) as context:
      class Foo:
        bar = KeeBox[int]('69')
    e = context.exception
    self.assertEqual(e.varName, 'fieldType')
    self.assertIs(e.actualObject, int)
    self.assertIs(e.actualType, type)
    self.assertIn(KeeMeta, e.expectedTypes)
    self.assertIn(KeeFlagsMeta, e.expectedTypes)

    class EF(KeeFlags):  # ExampleFlags, but shortened
      A = KeeFlag()
      B = KeeFlag()
      C = KeeFlag()
      D = KeeFlag()
      E = KeeFlag()

    class Foo:
      bar = KeeBox[EF]()

    setattr(Foo.bar, '__field_type__', int)
    with self.assertRaises(KeeBoxException) as context:
      foo = Foo()
      _ = foo.bar
    e = context.exception
    self.assertIs(e.box, Foo.bar)
    self.assertEqual(e.args, ())

  def test_str_field_type(self) -> None:
    """
    Tests the situation where the field type is instantiated with a string.
    """

    class IntNum(KeeNum):
      NUM_0 = Kee[int](69420_0)
      NUM_1 = Kee[int](69420_1)
      NUM_2 = Kee[int](69420_2)
      NUM_3 = Kee[int](69420_3)
      NUM_4 = Kee[int](69420_4)
      NUM_5 = Kee[int](69420_5)

    class Foo:
      bar = KeeBox[IntNum]('694203')
      ham = KeeBox[IntNum](694204)
      eggs = KeeBox[IntNum]()

    setattr(Foo.eggs, '__field_type__', str)
    foo = Foo()
    self.assertAlmostEqual(foo.bar, IntNum.NUM_3)
    self.assertAlmostEqual(foo.ham, IntNum.NUM_4)

    with self.assertRaises(KeeBoxException) as context:
      foo.eggs = 694206
    e = context.exception
    self.assertIs(e.box, Foo.eggs)
    self.assertEqual(e.args, ())
    self.assertEqual(repr(e), str(e))

    with self.assertRaises(RecursionError):
      Foo.bar.__set__(foo, lambda: None, _recursion=True)

    with self.assertRaises(KeeBoxValueError) as context:
      Foo.bar.__set__(foo, 69)
    e = context.exception
    self.assertIs(e.desc, Foo.bar)
    self.assertIs(e.num, IntNum)
    self.assertEqual(e.value, 69)
    self.assertEqual(repr(e), str(e))

  def test_floating_field(self) -> None:
    """
    Testing when 'KeeBox' is instantiated with arguments that *would*
    create an object belonging to the value type of the field enumeration,
    but where the object is not equal to the value type of any member of
    the enumeration.
    """

    class Constants(KeeNum):
      PI = Kee[float](pi)
      E = Kee[float](exp1)

    class Foo:
      bar = KeeBox[Constants]('PI')

    foo = Foo()
    with  self.assertRaises(KeeBoxValueError) as context:
      foo.bar = 69
    e = context.exception
    self.assertIs(e.desc, Foo.bar)
    self.assertIs(e.num, Constants)
    self.assertEqual(e.value, 69)
    self.assertEqual(repr(e), str(e))

    with self.assertRaises(KeeBoxValueError) as context:
      foo.bar = 0.557
    e = context.exception
    self.assertIs(e.desc, Foo.bar)
    self.assertIs(e.num, Constants)
    self.assertAlmostEqual(e.value, 0.557)
    self.assertEqual(repr(e), str(e))

    class Bad:
      bar = KeeBox[Constants]('never', 'gonna', 'give', 'you', 'up')

    with self.assertRaises(KeeBoxTypeError) as context:
      _ = Bad().bar
    e = context.exception
    self.assertIs(e.box, Bad.bar)
    self.assertEqual(e.args, ('never', 'gonna', 'give', 'you', 'up'))
    self.assertEqual(repr(e), str(e))

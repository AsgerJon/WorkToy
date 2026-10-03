"""
TestAttriBoxNumberDefault subclasses 'DescTest' and pins that a lone value
for a number field, one whose field type is 'bool', 'int', 'float' or
'complex', or a subclass keeping the constructor of one, goes through
'typeCast' and is refused when the lossless cast refuses it, by default
and by assignment alike. 'AttriBox[int](2.5)' used to default to '2',
'foo.n = (2.5,)' to store '2' where 'foo.n = 2.5' raised, and
'AttriBox[bool](2)' to default to 'True', since a default, and an
assigned tuple of one, reached the constructor, which rounds. Text fields
follow 'resolveText' already; a container or any other field type still
calls its constructor. 'FastBox' follows for its default, as it follows
the text rule.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from enum import IntEnum
from typing import TYPE_CHECKING

from worktoy.core.sentinels import THIS
from worktoy.desc import AttriBox, FastBox
from worktoy.mcls import BaseObject
from worktoy.waitaminute import TypeException

from . import DescTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class MyInt(int):
  """MyInt keeps the constructor of 'int'."""


class Level(IntEnum):
  """Level has a constructor of its own, which resolves a member."""

  LOW = 1
  HIGH = 2


class Rounding(AttriBox):
  """Rounding is an 'AttriBox' whose number fields round a value."""

  def resolveNumber(self, value: Any) -> Any:
    return round(value)


class Node(BaseObject):
  """Node turns into the 'int' 42, and holds a code built from itself."""

  code = AttriBox[int](THIS)

  def __int__(self) -> int:
    return 42


class TestAttriBoxNumberDefault(DescTest):
  """
  TestAttriBoxNumberDefault provides tests for lone values of number
  fields.
  """

  def test_lossy_default_refused(self) -> None:
    """A default the lossless cast refuses raises 'TypeException' on the
    first read, naming the field, the value and the field type."""

    class Pixel:
      n = AttriBox[int](2.5)
      flag = AttriBox[bool](2)

    pixel = Pixel()
    for name, value, fieldType in (('n', 2.5, int), ('flag', 2, bool)):
      with self.subTest(field=name):
        with self.assertRaises(TypeException) as context:
          _ = getattr(pixel, name)
        e = context.exception
        self.assertEqual(e.varName, name)
        self.assertEqual(e.actualObject, value)
        self.assertIn(fieldType, e.expectedTypes)

  def test_cast_default_kept(self) -> None:
    """A default the cast converts without loss is stored as the field
    type."""

    class Pixel:
      real = AttriBox[float](1)
      whole = AttriBox[int]('7')
      plane = AttriBox[complex](1)
      ratio = AttriBox[float]('0.5')
      flag = AttriBox[bool](1)

    pixel = Pixel()
    self.assertIs(type(pixel.real), float)
    self.assertEqual(pixel.real, 1.0)
    self.assertEqual(pixel.whole, 7)
    self.assertEqual(pixel.plane, 1 + 0j)
    self.assertEqual(pixel.ratio, 0.5)
    self.assertIs(pixel.flag, True)

  def test_assigned_tuple_of_one_refused(self) -> None:
    """An assigned tuple of one lossy value is refused as the value alone
    is, and the field keeps its value."""

    class Pixel:
      n = AttriBox[int](0)

    pixel = Pixel()
    with self.assertRaises(TypeException):
      pixel.n = (2.5,)
    with self.assertRaises(TypeException):
      pixel.n = 2.5
    self.assertEqual(pixel.n, 0)
    pixel.n = ('7',)
    self.assertEqual(pixel.n, 7)

  def test_several_arguments_build(self) -> None:
    """Several arguments, or keywords, still go to the constructor, by
    default and by an assigned tuple."""

    class Pixel:
      plane = AttriBox[complex](1, 2)
      whole = AttriBox[int]('ff', base=16)

    pixel = Pixel()
    self.assertEqual(pixel.plane, 1 + 2j)
    self.assertEqual(pixel.whole, 255)
    pixel.plane = 3, 4
    self.assertEqual(pixel.plane, 3 + 4j)

  def test_subclass_held_to_rule(self) -> None:
    """A subclass keeping the constructor of its builtin is held to the
    rule of the builtin, and the field holds an instance of the
    subclass."""

    class Pixel:
      lossy = AttriBox[MyInt](2.5)
      exact = AttriBox[MyInt](2.0)

    pixel = Pixel()
    with self.assertRaises(TypeException):
      _ = pixel.lossy
    self.assertIs(type(pixel.exact), MyInt)
    self.assertEqual(pixel.exact, 2)

  def test_own_constructor_trusted(self) -> None:
    """A subclass with a constructor of its own, such as an 'IntEnum',
    receives the default as given."""

    class Pixel:
      level = AttriBox[Level](2)

    self.assertIs(Pixel().level, Level.HIGH)

  def test_overflow_raised(self) -> None:
    """An 'int' too large for a 'float' raises the 'OverflowError' of the
    cast, as an assignment does."""

    class Pixel:
      real = AttriBox[float](10 ** 400)

    with self.assertRaises(OverflowError):
      _ = Pixel().real

  def test_sentinel_goes_to_constructor(self) -> None:
    """A contextual sentinel is still rebuilt through the constructor,
    which the cast would refuse."""
    self.assertEqual(Node().code, 42)

  def test_resolve_number_replaceable(self) -> None:
    """A subclass replacing 'resolveNumber' decides for its number
    fields, by default and by assignment."""

    class Pixel:
      n = Rounding[int](2.7)

    pixel = Pixel()
    self.assertEqual(pixel.n, 3)
    pixel.n = (1.2,)
    self.assertEqual(pixel.n, 1)

  def test_fast_box_follows(self) -> None:
    """The default of a 'FastBox' follows the same rule, for a subclass
    keeping the constructor of its builtin too."""

    class Pixel:
      lossy = FastBox[int](2.5)
      flag = FastBox[bool](2)
      narrow = FastBox[MyInt](2.5)
      real = FastBox[float](1)
      exact = FastBox[MyInt](2.0)
      level = FastBox[Level](2)

    pixel = Pixel()
    for name in ('lossy', 'flag', 'narrow'):
      with self.subTest(field=name):
        with self.assertRaises(TypeException) as context:
          _ = getattr(pixel, name)
        self.assertEqual(context.exception.varName, name)
    self.assertIs(type(pixel.real), float)
    self.assertIs(type(pixel.exact), MyInt)
    self.assertIs(pixel.level, Level.HIGH)

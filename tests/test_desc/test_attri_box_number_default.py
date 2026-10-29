"""
TestAttriBoxNumberDefault subclasses 'DescTest' and pins the two rules a
number field follows, one whose field type is 'bool', 'int', 'float' or
'complex'. An assigned value goes through 'typeCast' and is refused when
the lossless cast refuses it, so an assigned tuple is a tuple and is
refused. The field object of an 'AttriBox' is made by the constructor of
the field type from the arguments in the parentheses, a lone argument
included, so 'AttriBox[int](2.5)' holds 2.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core.sentinels import THIS
from worktoy.desc import AttriBox
from worktoy.mcls import BaseObject
from worktoy.waitaminute import TypeException
from worktoy.waitaminute.dispatch import TypeCastException

from . import DescTest


class MyInt(int):
  """MyInt keeps the constructor of 'int' and declares no '__cast_as__'."""


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

  def test_lone_default_holds_field_type(self) -> None:
    """This method tests that a lone number default holding a value of
    another type than the field type does not happen: 'float(1)',
    'complex(1)' and 'bool(1)' build it."""

    class Pixel:
      real = AttriBox[float](1)
      plane = AttriBox[complex](1)
      flag = AttriBox[bool](1)

    pixel = Pixel()
    self.assertIs(type(pixel.real), float)
    self.assertEqual(pixel.real, 1.0)
    self.assertEqual(pixel.plane, 1 + 0j)
    self.assertIs(pixel.flag, True)

  def test_assigned_tuple_refused(self) -> None:
    """An assigned tuple is a tuple, not an argument list, and is
    refused whatever it holds; the field keeps its value."""

    class Pixel:
      n = AttriBox[int](0)

    pixel = Pixel()
    for value in ((2.5,), (7,), 2.5):
      with self.subTest(value=repr(value)):
        with self.assertRaises(TypeException):
          pixel.n = value
    self.assertEqual(pixel.n, 0)

  def test_several_arguments_build(self) -> None:
    """Several arguments, or keywords, go to the constructor for the
    default; an assigned tuple does not."""

    class Pixel:
      plane = AttriBox[complex](1, 2)
      whole = AttriBox[int]('ff', base=16)

    pixel = Pixel()
    self.assertEqual(pixel.plane, 1 + 2j)
    self.assertEqual(pixel.whole, 255)
    with self.assertRaises(TypeException):
      pixel.plane = 3, 4
    self.assertEqual(pixel.plane, 1 + 2j)

  def test_sentinel_goes_to_constructor(self) -> None:
    """A contextual sentinel is still rebuilt through the constructor,
    which the cast would refuse."""
    self.assertEqual(Node().code, 42)

  def test_lone_default_goes_to_constructor(self) -> None:
    """This method tests that a lone number argument of an 'AttriBox' being
    cast, or refused by the cast, does not happen: the constructor of the
    field type makes the field object, so 'int(2.5)' gives 2."""

    class Pixel:
      slowLossy = AttriBox[int](2.5)
      slowFlag = AttriBox[bool](2)
      slowNarrow = AttriBox[MyInt](2.5)

    pixel = Pixel()
    self.assertEqual(pixel.slowLossy, 2)
    self.assertIs(pixel.slowFlag, True)
    self.assertIs(type(pixel.slowNarrow), MyInt)

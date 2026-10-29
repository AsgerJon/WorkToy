"""
TestFastBoxValue subclasses 'DescTest' and pins the one value a 'FastBox'
takes in its parentheses. '__call__' checks it at the class-body line: a
value of the field type is kept, any other goes through 'typeCast', which
converts only among the numbers and among the texts, without loss, and the
value, shared by every instance, must be hashable. Several arguments or a
keyword are refused there as well. Empty parentheses give each instance
'fieldType()' at its first read, and the constructor's own exceptions
pass through as they are.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import FastBox
from worktoy.waitaminute import TypeException
from worktoy.waitaminute.dispatch import TypeCastException

from . import DescTest


class MyInt(int):
  """MyInt subclasses 'int' and declares no '__cast_as__'."""


class Money:
  """Money converts a number through its '__cast_as__'."""

  def __init__(self, cents: int = 0) -> None:
    self.cents = cents

  @classmethod
  def __cast_as__(cls, value: object) -> object:
    if isinstance(value, int):
      return cls(value)
    return NotImplemented


class Odd:
  """Odd has a constructor returning something other than an 'Odd'."""

  def __new__(cls, *args) -> int:
    return 69


class Grumpy:
  """Grumpy refuses to be constructed."""

  def __init__(self) -> None:
    raise ValueError('no')


class TestFastBoxValue(DescTest):
  """
  TestFastBoxValue provides tests for the value of a 'FastBox'.
  """

  def test_value_of_field_type_kept(self) -> None:
    """This method tests that a value of the field type is not converted.
    A 'bool' for an 'int' field stays a 'bool'."""

    class Holder:
      count = FastBox[int](3)
      flag = FastBox[int](True)

    holder = Holder()
    self.assertEqual(holder.count, 3)
    self.assertIs(holder.flag, True)

  def test_lossless_cast(self) -> None:
    """This method tests that a value 'typeCast' converts without loss is
    not refused. It is converted once, at the class-body line."""

    class Holder:
      ratio = FastBox[float](1)
      unit = FastBox[str](b'cm')
      price = FastBox[Money](250)

    holder = Holder()
    self.assertIs(type(holder.ratio), float)
    self.assertEqual(holder.ratio, 1.0)
    self.assertEqual(holder.unit, 'cm')
    self.assertEqual(holder.price.cents, 250)

  def test_foreign_value_refused_at_call(self) -> None:
    """This method tests that a value neither of the field type nor
    converted by 'typeCast' does not wait for the first read. 'FastBox'
    raises 'TypeCastException' at its own '__call__'."""
    with self.assertRaises(TypeCastException):
      FastBox[int]('abc')
    with self.assertRaises(TypeCastException):
      FastBox[int](2.5)
    with self.assertRaises(TypeCastException):
      FastBox[MyInt](2)
    with self.assertRaises(TypeCastException):
      FastBox[list]('abc')

  def test_several_arguments_refused(self) -> None:
    """This method tests that several arguments or a keyword do not go to
    a constructor. 'FastBox' raises 'TypeError' at its '__call__'."""
    with self.assertRaises(TypeError):
      FastBox[tuple](1, 2)
    with self.assertRaises(TypeError):
      FastBox[int](value=1)

  def test_unhashable_value_refused(self) -> None:
    """This method tests that a value every instance would share although
    it cannot be hashed does not pass. 'FastBox' raises 'TypeError' at
    its '__call__', after a cast as well."""
    with self.assertRaises(TypeError):
      FastBox[list]([1, 2])
    with self.assertRaises(TypeError):
      FastBox[dict]({})
    with self.assertRaises(TypeError):
      FastBox[bytearray](b'x')

  def test_value_shared(self) -> None:
    """This method tests that the value is not copied per instance. Every
    instance holds the very object of the parentheses."""
    value = (1, 2)

    class Holder:
      pair = FastBox[tuple](value)

    first, second = Holder(), Holder()
    self.assertIs(first.pair, value)
    self.assertIs(second.pair, value)

  def test_empty_parentheses_new_per_instance(self) -> None:
    """This method tests that empty parentheses do not share one object.
    Each instance holds its own 'fieldType()', made at its first read."""

    class Holder:
      items = FastBox[list]()
      plain = FastBox[float]

    first, second = Holder(), Holder()
    self.assertEqual(first.items, [])
    self.assertIsNot(first.items, second.items)
    self.assertEqual(first.plain, 0.0)

  def test_constructor_raises_as_it_does(self) -> None:
    """This method tests that an exception of the field type's constructor
    is not replaced. It reaches the first read as it is."""

    class Holder:
      grumpy = FastBox[Grumpy]()

    with self.assertRaises(ValueError):
      _ = Holder().grumpy

  def test_constructor_result_must_be_field_type(self) -> None:
    """This method tests that 'fieldType()' returning something else does
    not reach the field. The read raises 'TypeException' naming the
    field and the object returned."""

    class Holder:
      odd = FastBox[Odd]()

    with self.assertRaises(TypeException) as context:
      _ = Holder().odd
    self.assertEqual(context.exception.varName, 'odd')
    self.assertEqual(context.exception.actualObject, 69)

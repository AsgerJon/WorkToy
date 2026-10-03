"""
TestAttriBoxBuiltinSubclass subclasses 'DescTest' from the
'tests.test_desc' package and pins how 'AttriBox' treats a field type
based on a builtin, such as a subclass of 'str' or 'int'. The field holds
an instance of the subclass. A subclass that keeps the constructor of
its builtin is held to the rule of that builtin, so an
'AttriBox[MyInt]' refuses '2.5' as an 'AttriBox[int]' does, where it used
to store '2'. A subclass with a constructor of its own is trusted, and
its constructor decides, as 'typeCast' and the overload dispatch decide.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from enum import IntEnum
from typing import TYPE_CHECKING

from worktoy.desc import AttriBox
from worktoy.waitaminute import TypeException

from . import DescTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class TestAttriBoxBuiltinSubclass(DescTest):
  """
  TestAttriBoxBuiltinSubclass provides tests for 'AttriBox' fields whose
  field type is based on a builtin.
  """

  def test_default_keeps_the_subclass(self) -> None:
    """A default given as a value of the builtin becomes an instance of
    the subclass."""

    class SomeStr(str):
      pass

    class Foo:
      bar = AttriBox[SomeStr]("""Never gonna give you up""")

    self.assertIsInstance(Foo().bar, Foo.bar.fieldType)
    self.assertEqual(Foo().bar, 'Never gonna give you up')

  def test_assignment_keeps_the_subclass(self) -> None:
    """A value the builtin's rule accepts is stored as an instance of the
    subclass."""

    class SomeStr(str):
      pass

    class SomeInt(int):
      pass

    class Foo:
      text = AttriBox[SomeStr](SomeStr(''))
      count = AttriBox[SomeInt](SomeInt(0))

    foo = Foo()
    foo.text = b'abc'
    foo.count = 2.0
    self.assertIs(type(foo.text), SomeStr)
    self.assertEqual(foo.text, 'abc')
    self.assertIs(type(foo.count), SomeInt)
    self.assertEqual(foo.count, 2)

  def test_lossy_assignment_refused(self) -> None:
    """A value the builtin's rule refuses raises 'TypeException', and the
    field keeps its value."""

    class SomeStr(str):
      pass

    class SomeInt(int):
      pass

    class Foo:
      text = AttriBox[SomeStr](SomeStr('x'))
      count = AttriBox[SomeInt](SomeInt(1))

    foo = Foo()
    for fieldName, value in (('text', None), ('count', 2.5)):
      with self.subTest(field=fieldName, value=repr(value)):
        with self.assertRaises(TypeException):
          setattr(foo, fieldName, value)
    self.assertEqual(foo.text, 'x')
    self.assertEqual(foo.count, 1)

  def test_int_enum_field(self) -> None:
    """An 'IntEnum' is based on 'int', so an integer or an integral float
    resolves to the member of that value, and anything else is
    refused."""

    class Level(IntEnum):
      LOW = 1
      HIGH = 2

    class Foo:
      level = AttriBox[Level](Level.LOW)

    foo = Foo()
    foo.level = 2
    self.assertIs(foo.level, Level.HIGH)
    foo.level = 1.0
    self.assertIs(foo.level, Level.LOW)
    for value in (2.5, 'HIGH', 3):
      with self.subTest(value=repr(value)):
        with self.assertRaises(TypeException):
          foo.level = value

  def test_own_constructor_trusted(self) -> None:
    """A subclass with a constructor of its own receives the value as
    given, for a text field and for a number, by default and by
    assignment."""

    class Upper(str):
      def __new__(cls, value: Any) -> Any:
        return str.__new__(cls, str(value).upper())

    class Celsius(float):
      def __new__(cls, value: Any) -> Any:
        return float.__new__(cls, value.rstrip('C'))

    class Foo:
      shout = AttriBox[Upper]('abc')
      temp = AttriBox[Celsius]('20C')

    foo = Foo()
    self.assertEqual(foo.shout, 'ABC')
    self.assertEqual(foo.temp, 20.0)
    foo.shout = 5
    foo.temp = '37C'
    self.assertIs(type(foo.shout), Upper)
    self.assertEqual(foo.shout, '5')
    self.assertIs(type(foo.temp), Celsius)
    self.assertEqual(foo.temp, 37.0)

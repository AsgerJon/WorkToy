"""
TestFieldBuiltinSubclass subclasses 'EZTest' from the 'tests.test_ezdata'
package and pins how an 'EZData' class casts a constructor argument or an
assignment to a field whose type is based on a builtin. A subclass that
keeps the constructor of its builtin is held to the rule of that builtin,
and the field holds an instance of the subclass: an 'EZField[MyInt]'
refuses '2.5' as an 'EZField[int]' does, where it used to store '2'. A
subclass with a constructor of its own is trusted, and its constructor
decides, as it does for an 'AttriBox'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.ezdata import EZData, EZField
from worktoy.waitaminute import TypeException

from . import EZTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class TestFieldBuiltinSubclass(EZTest):
  """
  TestFieldBuiltinSubclass provides tests for 'EZData' fields whose
  field type is based on a builtin.
  """

  def test_lossy_value_refused(self) -> None:
    """A value the builtin's rule refuses raises 'TypeException', as an
    argument and by assignment."""

    class MyInt(int):
      pass

    class Z(EZData):
      n = EZField[MyInt](MyInt(0))

    with self.assertRaises(TypeException):
      Z(2.5)
    z = Z()
    with self.assertRaises(TypeException):
      z.n = 2.5

  def test_cast_keeps_the_subclass(self) -> None:
    """A value the builtin's rule accepts is stored as an instance of the
    subclass."""

    class MyInt(int):
      pass

    class Z(EZData):
      n = EZField[MyInt](MyInt(0))

    z = Z(2.0)
    self.assertIs(type(z.n), MyInt)
    self.assertEqual(z.n, 2)
    z.n = '7'
    self.assertIs(type(z.n), MyInt)
    self.assertEqual(z.n, 7)

  def test_own_constructor_trusted(self) -> None:
    """A subclass with a constructor of its own receives the value as
    given, as an argument and by assignment."""

    class Celsius(float):
      def __new__(cls, value: Any) -> Any:
        if isinstance(value, str):
          value = value.rstrip('C')
        return float.__new__(cls, value)

    class Weather(EZData):
      temp = EZField[Celsius](Celsius(0))

    weather = Weather('20C')
    self.assertIs(type(weather.temp), Celsius)
    self.assertEqual(weather.temp, 20.0)
    weather.temp = '37C'
    self.assertEqual(weather.temp, 37.0)

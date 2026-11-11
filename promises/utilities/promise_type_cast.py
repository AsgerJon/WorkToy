"""
PromiseTypeCast promises 'typeCast' from 'worktoy.utilities'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from decimal import Decimal
from fractions import Fraction
from unittest import TestCase

from worktoy.utilities import typeCast
from worktoy.waitaminute.dispatch import TypeCastException, UnboundCastHook


class PromiseTypeCast(TestCase):
  """
  'typeCast(target, arg)' is the one conversion of 'worktoy', the one
  the boxes and the overloads ask. A value already of the target type
  comes back as it is, with one exception: when the target defines
  '__cast_as__' and the value's class is a strict subclass of the
  target, the hook is asked, so the target gets an instance of its own.
  Two closed families convert within themselves
  without loss: the numbers 'bool', 'int', 'float' and 'complex', and
  the text types 'str', 'bytes' and 'bytearray', as UTF-8. No string is
  ever parsed into a number and nothing else becomes text, and numbers
  of no family, such as 'Decimal' and 'Fraction', convert to none of
  them. Any other class converts only through a classmethod
  '__cast_as__' of its own, which returns an instance or
  'NotImplemented'. Everything else raises 'TypeCastException', a
  'TypeError', naming the target and the value. Source: the
  'typeCast' docstring and its examples, and the 1.1.0 changelog entry
  "A cast asks the target's hook about a member of a subclass".
  """

  def assertRefused(self, target: type, arg: object) -> TypeCastException:
    with self.assertRaises(TypeCastException) as context:
      typeCast(target, arg)
    e = context.exception
    self.assertIsInstance(e, TypeError)
    self.assertIs(e.type_, target)
    self.assertIs(e.arg, arg)
    return e

  def test_own_instance(self) -> None:
    names = ['Ada', 'Grace']
    self.assertIs(typeCast(list, names), names)
    self.assertIs(typeCast(int, True), True)

  def test_numbers(self) -> None:
    self.assertEqual(typeCast(int, 3.0), 3)
    self.assertIs(type(typeCast(int, 3.0)), int)
    self.assertEqual(typeCast(int, 3 + 0j), 3)
    self.assertEqual(typeCast(float, 3), 3.0)
    self.assertIs(type(typeCast(float, 3)), float)
    self.assertEqual(typeCast(float, 2 + 0j), 2.0)
    self.assertEqual(typeCast(complex, 3), 3 + 0j)
    self.assertEqual(typeCast(complex, 1.5), 1.5 + 0j)
    self.assertIs(typeCast(bool, 1), True)
    self.assertIs(typeCast(bool, 0.0), False)

  def test_lossy_numbers_refused(self) -> None:
    self.assertRefused(int, 3.5)
    self.assertRefused(int, 3 + 1j)
    self.assertRefused(float, 2 ** 53 + 1)
    self.assertRefused(float, 1 + 1j)
    self.assertRefused(bool, 2)

  def test_overflow_chained(self) -> None:
    e = self.assertRefused(float, 10 ** 400)
    self.assertIsInstance(e.__cause__, OverflowError)

  def test_no_string_parsed(self) -> None:
    self.assertRefused(int, '3')
    self.assertRefused(float, '1.5')

  def test_other_numbers_refused(self) -> None:
    self.assertRefused(int, Decimal(3))
    self.assertRefused(float, Fraction(1, 2))

  def test_text(self) -> None:
    self.assertEqual(typeCast(str, b'hello'), 'hello')
    self.assertEqual(typeCast(str, bytearray(b'hi')), 'hi')
    self.assertEqual(typeCast(bytes, 'hi'), b'hi')
    self.assertEqual(typeCast(bytes, bytearray(b'hi')), b'hi')
    self.assertEqual(typeCast(bytearray, b'hi'), bytearray(b'hi'))
    self.assertEqual(typeCast(bytearray, 'hi'), bytearray(b'hi'))

  def test_text_refused(self) -> None:
    self.assertRefused(str, 5)
    self.assertRefused(str, b'\xff')
    self.assertRefused(bytes, 5)

  def test_cast_hook(self) -> None:
    class Count(int):
      @classmethod
      def __cast_as__(cls, value):
        return cls(typeCast(int, value))

    count = typeCast(Count, 3.0)
    self.assertEqual(count, 3)
    self.assertIs(type(count), Count)

  def test_hook_refuses(self) -> None:
    class Even(int):
      @classmethod
      def __cast_as__(cls, value):
        if isinstance(value, int) and not value % 2:
          return cls(value)
        return NotImplemented

    self.assertEqual(typeCast(Even, 4), 4)
    self.assertRefused(Even, 5)

  def test_hook_result_not_an_instance(self) -> None:
    class Celsius(float):
      @classmethod
      def __cast_as__(cls, value):
        return float(value)

    self.assertRefused(Celsius, 20)

  def test_hook_asked_for_subclass_instance(self) -> None:
    class Celsius(float):
      @classmethod
      def __cast_as__(cls, value):
        return cls(typeCast(float, value))

    class Precise(Celsius):
      pass

    reading = Celsius(20.0)
    self.assertIs(typeCast(Celsius, reading), reading)
    converted = typeCast(Celsius, Precise(20.0))
    self.assertEqual(converted, 20.0)
    self.assertIs(type(converted), Celsius)

  def test_builtin_subclass_without_hook(self) -> None:
    class Meters(float):
      pass

    self.assertRefused(Meters, 3.0)
    self.assertRefused(Meters, 3)

  def test_unbound_hook(self) -> None:
    class Loose:
      def __cast_as__(cls, value):
        return cls()

    class Inheritor(Loose):
      pass

    with self.assertRaises(UnboundCastHook) as context:
      typeCast(Loose, 1)
    self.assertEqual(context.exception.className, 'Loose')
    self.assertIsNone(context.exception.targetName)
    with self.assertRaises(UnboundCastHook) as context:
      typeCast(Inheritor, 1)
    self.assertEqual(context.exception.className, 'Loose')
    self.assertEqual(context.exception.targetName, 'Inheritor')

  def test_containers_convert_nothing(self) -> None:
    self.assertRefused(list, (1, 2))
    self.assertRefused(tuple, [1, 2])

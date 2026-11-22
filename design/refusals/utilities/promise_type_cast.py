"""
RefusedTypeCast holds the refusals that belong with
'design.promises.utilities.promise_type_cast'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from decimal import Decimal
from fractions import Fraction
from unittest import TestCase

from worktoy.utilities import typeCast
from worktoy.waitaminute.dispatch import TypeCastException, UnboundCastHook


class RefusedTypeCast(TestCase):
  """
  Each of the following is refused, and the exception named is the one raised
  as of 1.2.3. Everything else raises 'TypeCastException', a 'TypeError',
  naming the target and the value. Source: the 'typeCast' docstring and its
  examples, and the 1.1.0 changelog entry "A cast asks the target's hook
  about a member of a subclass".
  """

  def test_unbound_hook_1(self) -> None:
    class Loose:
      def __cast_as__(cls, value):
        return cls()

    with self.assertRaises(Exception) as refused:
      typeCast(Loose, 1)
    self.assertIsInstance(refused.exception, UnboundCastHook)

  def test_unbound_hook_2(self) -> None:
    class Loose:
      def __cast_as__(cls, value):
        return cls()

    class Inheritor(Loose):
      pass

    with self.assertRaises(Exception) as refused:
      typeCast(Inheritor, 1)
    self.assertIsInstance(refused.exception, UnboundCastHook)

  def assertRefused(self, target: type, arg: object) -> None:
    """Asserts that 'typeCast' refuses 'arg' for 'target', as of 1.2.3 with
    'TypeCastException'."""
    with self.assertRaises(Exception) as refused:
      typeCast(target, arg)
    self.assertIsInstance(refused.exception, TypeCastException)

  def test_lossy_numbers_refused(self) -> None:
    self.assertRefused(int, 3.5)
    self.assertRefused(int, 3 + 1j)
    self.assertRefused(float, 2 ** 53 + 1)
    self.assertRefused(float, 1 + 1j)
    self.assertRefused(bool, 2)

  def test_overflow(self) -> None:
    self.assertRefused(float, 10 ** 400)

  def test_no_string_parsed(self) -> None:
    self.assertRefused(int, '3')
    self.assertRefused(float, '1.5')

  def test_other_numbers_refused(self) -> None:
    self.assertRefused(int, Decimal(3))
    self.assertRefused(float, Fraction(1, 2))

  def test_text_refused(self) -> None:
    self.assertRefused(str, 5)
    self.assertRefused(str, b'\xff')
    self.assertRefused(bytes, 5)

  def test_hook_refuses(self) -> None:
    class Even(int):
      @classmethod
      def __cast_as__(cls, value):
        if isinstance(value, int) and not value % 2:
          return cls(value)
        return NotImplemented

    self.assertRefused(Even, 5)

  def test_hook_result_not_an_instance(self) -> None:
    class Celsius(float):
      @classmethod
      def __cast_as__(cls, value):
        return float(value)

    self.assertRefused(Celsius, 20)

  def test_builtin_subclass_without_hook(self) -> None:
    class Meters(float):
      pass

    self.assertRefused(Meters, 3.0)
    self.assertRefused(Meters, 3)

  def test_containers_convert_nothing(self) -> None:
    self.assertRefused(list, (1, 2))
    self.assertRefused(tuple, [1, 2])

"""
TestTypeCastBool subclasses 'UtilitiesTest' and pins that 'typeCast' to
'bool' compares only numbers with 0 and 1. The cast used to look the
value up in '(True, False, 0, 1)', which asks the '__eq__' of the value,
so an '__eq__' answering 'True' to anything cast to 'True', and one that
raised escaped as its own exception, past the cast passes of an
overloaded method and so past its fallback.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from decimal import Decimal
from fractions import Fraction
from typing import TYPE_CHECKING

from worktoy.dispatch import overload
from worktoy.mcls import BaseObject
from worktoy.utilities import typeCast
from worktoy.waitaminute.dispatch import TypeCastException

from . import UtilitiesTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class AlwaysEqual:
  """AlwaysEqual claims to equal anything."""

  def __eq__(self, other: Any) -> bool:
    return True  # pragma: no cover

  __hash__ = object.__hash__


class RaisingEq:
  """RaisingEq refuses every comparison."""

  def __eq__(self, other: Any) -> bool:
    raise RuntimeError('no comparing')  # pragma: no cover

  __hash__ = object.__hash__


class Flag(BaseObject):
  """Flag overloads 'set' for a 'bool' and falls back for anything
  else."""

  @overload(bool)
  def set(self, value: bool) -> tuple:
    return 'bool', value

  @overload.fallback
  def set(self, *args) -> str:
    return 'fallback'


class TestTypeCastBool(UtilitiesTest):
  """
  TestTypeCastBool provides tests for 'typeCast' to 'bool'.
  """

  def test_always_equal_refused(self) -> None:
    """A value whose '__eq__' answers 'True' to anything is refused."""
    with self.assertRaises(TypeCastException):
      typeCast(bool, AlwaysEqual())

  def test_raising_eq_refused(self) -> None:
    """A value whose '__eq__' raises is refused with 'TypeCastException',
    its '__eq__' never asked."""
    with self.assertRaises(TypeCastException):
      typeCast(bool, RaisingEq())

  def test_numbers_zero_and_one(self) -> None:
    """A number equal to 0 or 1 casts to the 'bool' it equals."""
    for value in (0, 1, 0.0, 1.0, 1 + 0j, Fraction(1), Decimal(0), True):
      with self.subTest(value=value):
        self.assertIs(typeCast(bool, value), bool(value))

  def test_other_numbers_refused(self) -> None:
    """A number equal to neither 0 nor 1 is refused."""
    for value in (2, 0.5, -1, 1j):
      with self.subTest(value=value):
        with self.assertRaises(TypeCastException):
          typeCast(bool, value)

  def test_overload_reaches_fallback(self) -> None:
    """An overloaded method given such a value reaches its fallback
    instead of the 'bool' signature or the exception of '__eq__'."""
    flag = Flag()
    self.assertEqual(flag.set(AlwaysEqual()), 'fallback')
    self.assertEqual(flag.set(RaisingEq()), 'fallback')
    self.assertEqual(flag.set(1.0), ('bool', True))

"""
RefusedOverload holds the refusals that belong with
'design.promises.dispatch.promise_overload'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.desc import AttriBox
from worktoy.dispatch import overload
from worktoy.mcls import BaseObject
from worktoy.waitaminute.dispatch import DispatchException


class RefusedOverload(TestCase):
  """
  Each of the following is refused, and the exception named is the one raised
  as of 1.2.3. A call nothing accepts raises 'DispatchException', a
  'TypeError', holding the dispatcher, the positional arguments and the
  keywords. Source: the docstrings of 'overload' and 'Dispatcher', and the
  1.1.0 changelog entry "Keyword arguments pass through overload dispatch".
  """

  def test_lossless_conversion(self) -> None:
    class Counter(BaseObject):
      @overload(int)
      def count(self, value: int) -> int:
        return value

    with self.assertRaises(Exception) as refused:
      Counter().count(2.5)
    self.assertIsInstance(refused.exception, DispatchException)

  def test_cast_hook_converts(self) -> None:
    class Name:
      def __init__(self, text: str) -> None:
        self.text = text

      @classmethod
      def __cast_as__(cls, value):
        if isinstance(value, str):
          return cls(value)
        return NotImplemented

    class Badge(BaseObject):
      @overload(Name)
      def show(self, name: Name) -> str:
        return 'name %s' % name.text

    with self.assertRaises(Exception) as refused:
      Badge().show(7)
    self.assertIsInstance(refused.exception, DispatchException)

  def test_keyword_call_matches_no_positionals(self) -> None:
    class Money(BaseObject):
      amount = AttriBox[float](0.0)

      @overload(float)
      def __init__(self, amount: float) -> None:
        self.amount = amount

      @overload()
      def __init__(self) -> None:
        pass

    with self.assertRaises(Exception) as refused:
      Money(amount=2.5)
    self.assertIsInstance(refused.exception, TypeError)

  def test_default_by_position_is_matched(self) -> None:
    class Greeter(BaseObject):
      @overload(str)
      def greet(self, name: str, loud: bool = False) -> str:
        return name

    with self.assertRaises(Exception) as refused:
      Greeter().greet('ada', True)
    self.assertIsInstance(refused.exception, DispatchException)

  def test_nothing_accepts(self) -> None:
    class Greeter(BaseObject):
      @overload(str)
      def greet(self, name: str) -> str:
        return name

    with self.assertRaises(Exception) as refused:
      Greeter().greet(7, loud=True)
    self.assertIsInstance(refused.exception, DispatchException)

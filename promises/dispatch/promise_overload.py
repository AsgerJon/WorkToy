"""
PromiseOverload promises how '@overload' picks a declaration, from
'worktoy.dispatch'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.desc import AttriBox
from worktoy.dispatch import overload
from worktoy.mcls import BaseObject
from worktoy.waitaminute.dispatch import DispatchException


class PromiseOverload(TestCase):
  """
  In a 'BaseObject' class, a method may be declared once per signature
  with '@overload(...)', listing the classes of its positional arguments
  after 'self'. A call goes to the declaration its positional arguments
  match: by their exact classes, or as instances, a subclass instance
  matching its base, or, failing both, by a conversion that loses
  nothing, as an 'int' for a 'float' or '2.0' for an 'int', or that the
  '__cast_as__' hook of a declared class makes, as 'typeCast' does. An
  argument
  accepted as an instance arrives as it is, so 'True' reaches an 'int'
  declaration as 'True'. Keywords play no part in the choice and pass to
  the declaration chosen, so a call by keyword alone is matched as a call
  with no positional arguments, and a defaulted parameter passed by
  position counts as one more positional argument to match. A call
  nothing accepts raises 'DispatchException', a 'TypeError', holding the
  dispatcher, the positional arguments and the keywords. Source: the
  docstrings of 'overload' and 'Dispatcher', and the 1.1.0 changelog
  entry "Keyword arguments pass through overload dispatch".
  """

  def test_by_positional_classes(self) -> None:
    class Money(BaseObject):
      amount = AttriBox[float](0.0)
      currency = AttriBox[str]('EUR')

      @overload(float, str)
      def __init__(self, amount: float, currency: str) -> None:
        self.amount, self.currency = amount, currency

      @overload(float)
      def __init__(self, amount: float) -> None:
        self.amount = amount

      @overload()
      def __init__(self) -> None:
        pass

    usd = Money(2.5, 'USD')
    self.assertEqual((usd.amount, usd.currency), (2.5, 'USD'))
    self.assertEqual((Money(4.0).amount, Money(4.0).currency), (4.0, 'EUR'))
    self.assertEqual(Money().amount, 0.0)

  def test_subclass_instance(self) -> None:
    class Animal:
      pass

    class Dog(Animal):
      pass

    class Vet(BaseObject):
      @overload(Animal)
      def treat(self, animal: Animal) -> str:
        return 'treated'

    self.assertEqual(Vet().treat(Dog()), 'treated')

  def test_lossless_conversion(self) -> None:
    class Scale(BaseObject):
      @overload(float)
      def ratio(self, value: float) -> float:
        return value

      @overload(str)
      def ratio(self, value: str) -> str:
        return value

    class Counter(BaseObject):
      @overload(int)
      def count(self, value: int) -> int:
        return value

    self.assertEqual(Scale().ratio(3), 3.0)
    self.assertIs(type(Scale().ratio(3)), float)
    self.assertEqual(Counter().count(2.0), 2)
    self.assertIs(type(Counter().count(2.0)), int)
    with self.assertRaises(DispatchException):
      Counter().count(2.5)

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

    self.assertEqual(Badge().show('Ada'), 'name Ada')
    with self.assertRaises(DispatchException):
      Badge().show(7)

  def test_keywords_pass_through(self) -> None:
    class Greeter(BaseObject):
      @overload(str)
      def greet(self, name: str, loud: bool = False) -> str:
        return name.upper() if loud else name

    self.assertEqual(Greeter().greet('ada', loud=True), 'ADA')

  def test_keyword_call_matches_no_positionals(self) -> None:
    class Money(BaseObject):
      amount = AttriBox[float](0.0)

      @overload(float)
      def __init__(self, amount: float) -> None:
        self.amount = amount

      @overload()
      def __init__(self) -> None:
        pass

    with self.assertRaises(TypeError):
      Money(amount=2.5)

  def test_default_by_position_is_matched(self) -> None:
    class Greeter(BaseObject):
      @overload(str)
      def greet(self, name: str, loud: bool = False) -> str:
        return name

    with self.assertRaises(DispatchException):
      Greeter().greet('ada', True)

  def test_instance_arrives_unconverted(self) -> None:
    class Counter(BaseObject):
      @overload(int)
      def count(self, value: int) -> int:
        return value

    self.assertIs(Counter().count(True), True)

  def test_nothing_accepts(self) -> None:
    class Greeter(BaseObject):
      @overload(str)
      def greet(self, name: str) -> str:
        return name

    with self.assertRaises(DispatchException) as context:
      Greeter().greet(7, loud=True)
    e = context.exception
    self.assertIsInstance(e, TypeError)
    self.assertIs(e.dispatch, vars(Greeter)['greet'])
    self.assertEqual(e.posArgs, (7,))
    self.assertEqual(e.keyArgs, {'loud': True})

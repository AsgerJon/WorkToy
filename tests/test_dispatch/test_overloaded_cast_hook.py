"""
TestOverloadedCastHook tests 'typeCast' on a class whose '__cast_as__' is
an overloaded classmethod.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.dispatch import overload
from worktoy.mcls import BaseObject
from worktoy.utilities import typeCast, hasCastRule
from worktoy.waitaminute.dispatch import TypeCastException, UnboundCastHook
from worktoy.waitaminute.dispatch import DispatchException
from . import DispatchTest


class TestOverloadedCastHook(DispatchTest):
  """
  A class says how a value becomes one of its instances in a classmethod
  '__cast_as__', and a class that takes values of several types writes
  that hook once per type with 'overload'. The class then holds a
  'Dispatcher' at the name, not a 'classmethod', and 'typeCast' must
  take it for the hook it is. The tests pin the cast through each
  overload, the rule 'hasCastRule' reports, the subclass an inherited
  hook is bound to, the refusal of a value no overload accepts, that an
  error from inside an overload propagates, and that an overloaded hook
  without '@classmethod' is refused as a plain one is.
  """

  @staticmethod
  def _money() -> type:
    class Money(BaseObject):
      @overload(int)
      def __init__(self, cents: int) -> None:
        self.cents = cents

      @classmethod
      @overload(int)
      def fromCents(cls, cents: int) -> Money:
        return cls(cents)

      @classmethod
      @overload(str)
      def __cast_as__(cls, text: str) -> Money:
        return cls(int(text))

      @classmethod
      @overload(float)
      def __cast_as__(cls, amount: float) -> Money:
        return cls(round(amount * 100))

      @classmethod
      @overload(bytes)
      def __cast_as__(cls, raw: bytes) -> Money:
        return cls.fromCents(raw)

    return Money

  def test_cast_through_each_overload(self) -> None:
    Money = self._money()
    fromText = typeCast(Money, '250')
    self.assertIs(type(fromText), Money)
    self.assertEqual(fromText.cents, 250)
    fromAmount = typeCast(Money, 2.5)
    self.assertIs(type(fromAmount), Money)
    self.assertEqual(fromAmount.cents, 250)
    self.assertTrue(hasCastRule(Money))
    already = Money(7)
    self.assertIs(typeCast(Money, already), already)
    self.assertEqual(Money.fromCents(3).cents, 3)

  def test_inherited_hook_binds_the_subclass(self) -> None:
    Money = self._money()

    class Coin(Money):
      pass

    coin = typeCast(Coin, '5')
    self.assertIs(type(coin), Coin)
    self.assertEqual(coin.cents, 5)
    self.assertTrue(hasCastRule(Coin))

  def test_value_no_overload_accepts_refused(self) -> None:
    Money = self._money()
    with self.assertRaises(TypeCastException) as context:
      typeCast(Money, [1])
    self.assertIs(context.exception.type_, Money)
    self.assertEqual(context.exception.arg, [1])
    expected = "Unable to cast value [1] to type 'Money'!"
    self.assertEqual(str(context.exception), expected)

  def test_error_inside_an_overload_propagates(self) -> None:
    Money = self._money()
    with self.assertRaises(ValueError) as context:
      typeCast(Money, 'abc')
    self.assertIn("'abc'", str(context.exception))
    #  The 'bytes' overload calls another overloaded method, which has
    #  no overload for 'bytes': that failure is not the hook's own.
    with self.assertRaises(DispatchException) as context:
      typeCast(Money, b'5')
    self.assertIs(context.exception.dispatch, vars(Money)['fromCents'])
    self.assertIn("no overload of 'Money.fromCents' accepts",
                  str(context.exception))

  def test_overloaded_hook_without_classmethod_refused(self) -> None:
    class Loose(BaseObject):
      @overload(str)
      def __cast_as__(self, text: str) -> str:
        """Never runs: the hook is refused before it is called."""

    class Static(BaseObject):
      @staticmethod
      @overload(str)
      def __cast_as__(text: str) -> str:
        """Never runs: the hook is refused before it is called."""

    spec = """The class '%s' defines '__cast_as__' without the
    '@classmethod' decorator! 'typeCast' calls the hook on the class to
    make an instance, so the definition requires it."""
    for target in (Loose, Static):
      with self.subTest(target=target.__name__):
        expected = str.join(' ', (spec % target.__name__).split())
        with self.assertRaises(UnboundCastHook) as context:
          typeCast(target, 'x')
        self.assertEqual(str(context.exception), expected)
        with self.assertRaises(UnboundCastHook) as context:
          hasCastRule(target)
        self.assertEqual(str(context.exception), expected)

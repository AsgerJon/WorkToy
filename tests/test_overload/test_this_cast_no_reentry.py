"""
TestThisCastNoReentry subclasses 'OverloadTest' and pins that a call of
one argument no overload of a constructor takes is refused without the
cast passes calling the class on that argument. That call is the very
call being dispatched, so it nested until the recursion limit and
crashed Python 3.7 to 3.11 once a program had raised that limit. In a
call of several arguments, and outside a constructor, the cast to the
class is a call of its own and stays. A signature naming 'THIS' refuses
casts by default, so the overloads here ask for them with
'strict=False'; the copy constructor of 'Clause' does not, and is never
cast to.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import worktoy.dispatch._dispatcher as dispatcherFile
from worktoy.core.sentinels import ARGS, THIS
from worktoy.desc import AttriBox
from worktoy.dispatch import overload
from worktoy.lorem_ipsum import Clause
from worktoy.mcls import BaseObject
from worktoy.waitaminute.dispatch import DispatchException

from . import OverloadTest


class Money(BaseObject):
  """An amount in cents, with a copy constructor, a copy with a note, and
  an addition that takes another amount."""

  cents = AttriBox[int](0)
  note = AttriBox[str]('')

  @overload(int)
  def __init__(self, cents: int) -> None:
    self.cents = cents

  @overload(THIS, strict=False)
  def __init__(self, other: Money) -> None:
    self.cents = other.cents

  @overload(THIS, str, strict=False)
  def __init__(self, other: Money, note: str) -> None:
    self.cents = other.cents
    self.note = note

  @overload(THIS, strict=False)
  def __add__(self, other: Money) -> Money:
    return Money(self.cents + other.cents)


class Euro(Money):
  """An amount given in euros, inheriting the constructors of 'Money'."""

  @overload(float)
  def __init__(self, amount: float) -> None:
    self.cents = round(amount * 100)


class Wallet(BaseObject):
  """The total of any number of other wallets."""

  cents = AttriBox[int](0)

  @overload(ARGS[THIS], strict=False)
  def __init__(self, *others: Wallet) -> None:
    self.cents = sum(other.cents for other in others)


class Tab(BaseObject):
  """A bill in cents, or an earlier tab with more items added."""

  cents = AttriBox[int](0)

  @overload(int)
  def __init__(self, cents: int) -> None:
    self.cents = cents

  @overload(THIS, ARGS[int], strict=False)
  def __init__(self, base: Tab, *items: int) -> None:
    self.cents = base.cents + sum(items)


class TestThisCastNoReentry(OverloadTest):
  """
  TestThisCastNoReentry provides tests for the cast passes of a
  constructor with a 'THIS' overload.
  """

  def setUp(self) -> None:
    super().setUp()
    #  Each cast as the target and whether it may call the target.
    self.casts = []
    realTypeCast = dispatcherFile.typeCast

    def countingTypeCast(target: type, arg: object, **kwargs) -> object:
      allowInstantiation = kwargs.get('allowInstantiation', True)
      self.casts.append((target, allowInstantiation))
      return realTypeCast(target, arg, **kwargs)

    self.realTypeCast = realTypeCast
    dispatcherFile.typeCast = countingTypeCast

  def tearDown(self) -> None:
    dispatcherFile.typeCast = self.realTypeCast
    super().tearDown()

  def test_unmatched_call_never_calls_own_class(self) -> None:
    """'Money('abc')' is refused after one cast to 'int' and one to
    'Money' that may not call 'Money'."""
    with self.assertRaises(DispatchException):
      Money('abc')
    self.assertEqual(self.casts, [(int, True), (Money, False)])

  def test_library_copy_constructor(self) -> None:
    """'Clause('abc')' is refused without any cast to 'Clause', its copy
    constructor being strict."""
    with self.assertRaises(DispatchException):
      Clause('abc')
    self.assertNotIn(Clause, [target for target, _ in self.casts])

  def test_subclass_ends_in_parent(self) -> None:
    """'Euro('abc')' calls 'Money' on 'abc' once, through the inherited
    copy constructor, and the constructor of 'Money' refuses it without
    calling 'Money' again."""
    with self.assertRaises(DispatchException):
      Euro('abc')
    self.assertEqual(self.casts.count((Money, True)), 1)
    self.assertEqual(self.casts.count((Money, False)), 1)
    self.assertNotIn(Euro, [target for target, _ in self.casts])

  def test_variadic_inner_never_calls_own_class(self) -> None:
    """'Wallet('abc')' is refused after one cast to 'Wallet' that may not
    call 'Wallet', while wallets still add up."""
    with self.assertRaises(DispatchException):
      Wallet('abc')
    self.assertEqual(self.casts, [(Wallet, False)])
    self.assertEqual(Wallet(Wallet(), Wallet()).cents, 0)

  def test_variadic_prefix_ends_one_level_down(self) -> None:
    """'Tab('abc', 1)' calls 'Tab('abc')', a call of its own, and that
    one is refused after one cast to 'Tab' that may not call 'Tab'. A tab
    still takes an earlier tab and items."""
    with self.assertRaises(DispatchException):
      Tab('abc', 1)
    self.assertEqual(self.casts, [(Tab, True), (int, True), (Tab, False)])
    self.assertEqual(Tab(Tab(5), 1, 2).cents, 8)

  def test_copy_constructor_still_matches(self) -> None:
    """The copy constructor still takes an instance, of the class and of
    a subclass, without any cast."""
    self.assertEqual(Money(Money(5)).cents, 5)
    self.assertEqual(Euro(Money(5)).cents, 5)
    self.assertEqual(Money(Euro(2.5)).cents, 250)
    self.assertEqual(self.casts, [])

  def test_argument_among_several_still_cast(self) -> None:
    """'Money(5, 'tip')' casts 5 to 'Money' by calling 'Money(5)', a call
    of its own, and copies it with the note."""
    money = Money(5, 'tip')
    self.assertEqual((money.cents, money.note), (5, 'tip'))
    self.assertEqual(self.casts, [(Money, True)])

  def test_method_still_casts_to_own_class(self) -> None:
    """Outside the constructor the cast to the class stays a conversion:
    'Money(5) + 3' builds 'Money(3)' and adds it."""
    total = Money(5) + 3
    self.assertIsInstance(total, Money)
    self.assertEqual(total.cents, 8)
    self.assertEqual(self.casts, [(Money, True)])

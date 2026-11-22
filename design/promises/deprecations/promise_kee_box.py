"""
DeprecatedKeeBox holds the promise of 'KeeBox' from 'worktoy.keenum',
which ends at the next major update.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import warnings
from unittest import TestCase

from worktoy.desc import AttriBox
from worktoy.keenum import KeeBox, KeeNum, Kee
from worktoy.mcls import BaseObject

from ..keenum._file_access import FileAccess


class DeprecatedKeeBox(TestCase):
  """
  Deprecated in 1.2.0: 'KeeBox'.

  Why it ends: since the members of an enumeration are plain objects, an
  'AttriBox' over the enumeration declares the same field, and its
  parentheses read a lone number as assignment reads it, where those of a
  'KeeBox' read the same number as a position on declaration and as a value
  on assignment. An 'AttriBox' over an enumeration is promised in
  'design/promises/keenum/promise_enumeration.py' and
  'design/promises/keenum/promise_flags.py'.

  Promised in 1.1.0 and owed through 1.x: a 'KeeBox' is a box over an
  enumeration whose parentheses take what identifies a member: the member, a
  name in any case, the answer of '__class_resolve__', a position, a value,
  or the arguments the value is built from; over a flags class, flags by
  name, several of them or a tuple. A lone 'int' in range is a position,
  where the parentheses of an 'AttriBox' over the same enumeration call the
  class with it and so take it as a value. Assignment converts as the
  enumeration converts. Source: the 'KeeBox' docstring and its example, and
  the 1.1.0 changelog entry "A 'KeeBox' converts an assigned value as the
  enumeration does".
  """

  def setUp(self) -> None:
    silenced = warnings.catch_warnings()
    silenced.__enter__()
    self.addCleanup(silenced.__exit__, None, None, None)
    warnings.simplefilter('ignore')

  def makeCurrency(self) -> type:
    class Currency(KeeNum):
      EUR = Kee[complex](1, 2)
      USD = Kee[complex](3, 4)

    return Currency

  def test_parentheses(self) -> None:
    Currency = self.makeCurrency()

    class Wallet(BaseObject):
      byMember = KeeBox[Currency](Currency.USD)
      byName = KeeBox[Currency]('usd')
      byPosition = KeeBox[Currency](1)
      byValue = KeeBox[Currency](3 + 4j)
      byArguments = KeeBox[Currency](3, 4)
      access = KeeBox[FileAccess]('read', 'write')

    wallet = Wallet()
    for name in ('byMember', 'byName', 'byPosition', 'byValue',
                 'byArguments'):
      with self.subTest(name=name):
        self.assertIs(getattr(wallet, name), Currency.USD)
    self.assertIs(wallet.access, FileAccess.READ_WRITE)

  def test_int_is_a_position(self) -> None:
    class Rank(KeeNum):
      LOW = Kee[int](2)
      MID = Kee[int](5)
      HIGH = Kee[int](9)

    class Board(BaseObject):
      boxed = KeeBox[Rank](2)
      plain = AttriBox[Rank](2)

    board = Board()
    self.assertIs(board.boxed, Rank.HIGH)
    self.assertIs(board.plain, Rank.LOW)

  def test_assignment(self) -> None:
    Currency = self.makeCurrency()

    class Wallet(BaseObject):
      currency = KeeBox[Currency]('eur')

    wallet = Wallet()
    wallet.currency = 'usd'
    self.assertIs(wallet.currency, Currency.USD)

"""
RefusedKeeBox holds the refusals that belong with
'design.promises.deprecations.promise_kee_box'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import warnings
from unittest import TestCase

from worktoy.keenum import KeeBox, KeeNum, Kee
from worktoy.mcls import BaseObject
from worktoy.waitaminute import TypeException
from worktoy.waitaminute.keenum import KeeBoxValueError, KeeBoxTypeError


class RefusedKeeBox(TestCase):
  """
  Each of the following is refused, and the exception named is the one raised
  as of 1.2.3. A lone value no member holds raises 'KeeBoxValueError', and
  arguments the value type refuses raise 'KeeBoxTypeError', at the first
  read. An assigned value the enumeration does not convert raises
  'TypeException' naming the field. A subscript that is no enumeration raises
  'TypeException'. Source: the 'KeeBox' docstring and its example, and the
  1.1.0 changelog entry "A 'KeeBox' converts an assigned value as the
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

  def test_parentheses_refused_1(self) -> None:
    Currency = self.makeCurrency()

    class Wallet(BaseObject):
      unknown = KeeBox[Currency](9j)
      broken = KeeBox[Currency]('x', 'y', 'z')

    with self.assertRaises(Exception) as refused:
      _ = Wallet().unknown
    self.assertIsInstance(refused.exception, KeeBoxValueError)

  def test_parentheses_refused_2(self) -> None:
    Currency = self.makeCurrency()

    class Wallet(BaseObject):
      unknown = KeeBox[Currency](9j)
      broken = KeeBox[Currency]('x', 'y', 'z')

    with self.assertRaises(Exception) as refused:
      _ = Wallet().broken
    self.assertIsInstance(refused.exception, KeeBoxTypeError)

  def test_assignment(self) -> None:
    Currency = self.makeCurrency()

    class Wallet(BaseObject):
      currency = KeeBox[Currency]('eur')

    wallet = Wallet()
    wallet.currency = 'usd'
    with self.assertRaises(Exception) as refused:
      wallet.currency = 1
    self.assertIsInstance(refused.exception, TypeException)

  def test_subscript(self) -> None:
    with self.assertRaises(Exception) as refused:
      KeeBox[int]
    self.assertIsInstance(refused.exception, TypeException)

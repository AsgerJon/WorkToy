"""
RefusedDetails holds the refusals that belong with
'design.promises.ezdata.promise_details'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.core.sentinels import THIS
from worktoy.ezdata import EZData, EZField
from worktoy.waitaminute import TypeException
from worktoy.waitaminute.ezdata import IncompleteFieldException
from worktoy.waitaminute.ezdata import ReservedFieldError


class RefusedDetails(TestCase):
  """
  Each of the following is refused, and the exception named is the one raised
  as of 1.2.3. A bare 'None' has no type and raises
  'IncompleteFieldException'. An 'int' field declared as 'x = 0' refuses
  '0.5'. A default 'typeCast' does not convert, as 'EZField[int]('7')', is
  refused at the first instance. 'EZField[THIS]' raises 'TypeError'. A name
  the generated methods use, as 'replace', is no field name and raises
  'ReservedFieldError'. A subclass of a frozen class that does not declare
  'frozen=True' raises 'TypeError', and '__post_init__' cannot assign to a
  frozen instance. Source: the docstrings of 'EZData', 'EZField', 'EZSpace'
  and 'EZHook', and the 1.1.0 changelog.
  """

  def test_field_types_1(self) -> None:
    with self.assertRaises(Exception) as refused:
      class Node(EZData):
        parent = None
    self.assertIsInstance(refused.exception, IncompleteFieldException)

  def test_field_types_2(self) -> None:
    class Counter(EZData):
      count = 0

    with self.assertRaises(Exception) as refused:
      Counter().count = 0.5
    self.assertIsInstance(refused.exception, TypeException)

  def test_field_types_3(self) -> None:
    class Seven(EZData):
      number = EZField[int]('7')

    with self.assertRaises(Exception) as refused:
      Seven()
    self.assertIsInstance(refused.exception, TypeException)

  def test_field_types_4(self) -> None:
    with self.assertRaises(Exception) as refused:
      class Tree(EZData):
        child = EZField[THIS]()
    self.assertIsInstance(refused.exception, TypeError)

  def test_reserved_name_and_own_repr(self) -> None:
    with self.assertRaises(Exception) as refused:
      class Clash(EZData):
        replace = 1
    self.assertIsInstance(refused.exception, ReservedFieldError)

  def test_frozen_rules_1(self) -> None:
    class Frozen(EZData, frozen=True):
      a = 1
      b = 0

    with self.assertRaises(Exception) as refused:
      class Thawed(Frozen):
        c = 2
    self.assertIsInstance(refused.exception, TypeError)

  def test_frozen_rules_2(self) -> None:
    class Doubled(EZData, frozen=True):
      a = 1
      b = 0

      def __post_init__(self) -> None:
        self.b = 2 * self.a

    with self.assertRaises(Exception) as refused:
      Doubled(3)
    self.assertIsInstance(refused.exception, AttributeError)

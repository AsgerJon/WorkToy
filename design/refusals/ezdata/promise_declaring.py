"""
RefusedDeclaring holds the refusals that belong with
'design.promises.ezdata.promise_declaring'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.ezdata import EZData, EZField, fields
from worktoy.waitaminute.ezdata import IncompleteFieldException
from worktoy.waitaminute.ezdata import DuplicateError, ReservedMethodError
from worktoy.waitaminute.ezdata import ReservedAttributeError


class RefusedDeclaring(TestCase):
  """
  Each of the following is refused, and the exception named is the one raised
  as of 1.2.3. 'fields' of anything else raises 'TypeError'. As the class is
  created, 'EZField(1)' without a type and 'EZField[int]' without parentheses
  raise 'IncompleteFieldException', a field bound twice 'DuplicateError', a
  body defining a generated method such as '__init__' 'ReservedMethodError',
  and one binding an attribute EZData sets itself, such as '__kw_only__',
  'ReservedAttributeError'. Source: the docstrings of 'EZData', 'EZField',
  'EZSpace' and 'fields'.
  """

  def test_fields(self) -> None:
    with self.assertRaises(Exception) as refused:
      fields(3)
    self.assertIsInstance(refused.exception, TypeError)

  def test_refusals_1(self) -> None:
    with self.assertRaises(Exception) as refused:
      class Untyped(EZData):
        a = EZField(1)
    self.assertIsInstance(refused.exception, IncompleteFieldException)

  def test_refusals_2(self) -> None:
    with self.assertRaises(Exception) as refused:
      class Bare(EZData):
        a = EZField[int]
    self.assertIsInstance(refused.exception, IncompleteFieldException)

  def test_refusals_3(self) -> None:
    with self.assertRaises(Exception) as refused:
      class Twice(EZData):
        a = 1
        a = 2
    self.assertIsInstance(refused.exception, DuplicateError)

  def test_refusals_4(self) -> None:
    with self.assertRaises(Exception) as refused:
      class OwnInit(EZData):
        a = 1

        def __init__(self) -> None:
          pass
    self.assertIsInstance(refused.exception, ReservedMethodError)

  def test_refusals_5(self) -> None:
    with self.assertRaises(Exception) as refused:
      class OwnOption(EZData):
        __kw_only__ = True
    self.assertIsInstance(refused.exception, ReservedAttributeError)

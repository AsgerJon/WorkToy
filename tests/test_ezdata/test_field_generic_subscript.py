"""
TestFieldGenericSubscript subclasses 'EZTest' and pins that 'EZField'
refuses, at the subscript, anything that is not a class, with
'TypeException' naming 'fieldType'. Any subscript used to be stored, so
'EZField[list[int]]' built a class on Python 3.9 and 3.10 whose first
instance failed inside 'isinstance', and from 3.11 the class statement
failed with a message naming '__field_type__' rather than the field.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import sys
from numbers import Number
from typing import List, TypeVar

from worktoy.ezdata import EZData, EZField
from worktoy.waitaminute import TypeException

from . import EZTest

T = TypeVar('T')


class Pretender:
  """Pretender claims to be a class through '__class__', as 'list[int]'
  does on Python 3.9 and 3.10."""

  @property
  def __class__(self) -> type:
    return type


class TestFieldGenericSubscript(EZTest):
  """
  TestFieldGenericSubscript provides tests for the subscript of an
  'EZField'.
  """

  def test_typing_generic_refused(self) -> None:
    """A parametrized generic from 'typing' is refused."""
    with self.assertRaises(TypeException) as context:
      _ = EZField[List[int]]
    self.assertEqual(context.exception.varName, 'fieldType')
    self.assertEqual(context.exception.actualObject, List[int])

  def test_builtin_generic_refused(self) -> None:
    """A builtin parametrized generic is refused."""
    if sys.version_info < (3, 9):  # pragma: no cover (Python < 3.9)
      self.skipTest('builtin generics are not subscriptable before 3.9')
    with self.assertRaises(TypeException):
      _ = EZField[list[int]]

  def test_pretender_and_typevar_refused(self) -> None:
    """An object claiming to be a class through '__class__', and a
    'TypeVar', are refused."""
    self.assertIsInstance(Pretender(), type)
    for subscript in (Pretender(), T):
      with self.subTest(subscript=subscript):
        with self.assertRaises(TypeException):
          _ = EZField[subscript]

  def test_classes_accepted(self) -> None:
    """A plain class and an abstract base are accepted."""

    class Point(EZData):
      x = EZField[int](0)
      y = EZField[Number](0.5)

    self.assertEqual(Point(1).asTuple(), (1, 0.5))

"""
PromiseDeclaring promises how an 'EZData' class declares its fields,
from 'worktoy.ezdata'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.ezdata import EZData, EZField, fields
from worktoy.waitaminute.ezdata import IncompleteFieldException
from worktoy.waitaminute.ezdata import DuplicateError, ReservedMethodError
from worktoy.waitaminute.ezdata import ReservedAttributeError


class PromiseDeclaring(TestCase):
  """
  An 'EZData' class declares its fields in its body, in order, as
  'EZField[T](...)' or as a plain value whose type becomes the field
  type; an annotation alone declares nothing. A default is built anew
  for each instance, by calling the type with the arguments, so a
  mutable default is never shared and 'EZField[list]('abc')' holds the
  three letters. 'fields(cls)' and 'fields(instance)' give the fields in
  order, and anything else raises 'TypeError'. As the class is created,
  'EZField(1)' without a type and 'EZField[int]' without parentheses
  raise 'IncompleteFieldException', a field bound twice
  'DuplicateError', a body defining a generated method such as
  '__init__' 'ReservedMethodError', and one binding an attribute EZData
  sets itself, such as '__kw_only__', 'ReservedAttributeError'. Source:
  the docstrings of 'EZData', 'EZField', 'EZSpace' and 'fields'.
  """

  def test_fields(self) -> None:
    class Point(EZData):
      x = EZField[float](0.0)
      y = 0.0
      label: str

    self.assertEqual([f.fieldName for f in fields(Point)], ['x', 'y'])
    self.assertEqual([f.fieldName for f in fields(Point())], ['x', 'y'])
    self.assertIs(fields(Point)[1].fieldType, float)
    with self.assertRaises(TypeError):
      fields(3)

  def test_defaults(self) -> None:
    class Bag(EZData):
      items = EZField[list]()
      letters = EZField[list]('abc')

    first, second = Bag(), Bag()
    first.items.append('apple')
    self.assertEqual(second.items, [])
    self.assertEqual(first.letters, ['a', 'b', 'c'])

  def test_refusals(self) -> None:
    with self.assertRaises(IncompleteFieldException) as context:
      class Untyped(EZData):
        a = EZField(1)
    self.assertEqual(context.exception.fieldName, 'a')
    with self.assertRaises(IncompleteFieldException):
      class Bare(EZData):
        a = EZField[int]
    with self.assertRaises(DuplicateError) as context:
      class Twice(EZData):
        a = 1
        a = 2
    self.assertEqual(context.exception.fieldName, 'a')
    with self.assertRaises(ReservedMethodError) as context:
      class OwnInit(EZData):
        a = 1

        def __init__(self) -> None:
          pass
    self.assertEqual(context.exception.methodName, '__init__')
    with self.assertRaises(ReservedAttributeError) as context:
      class OwnOption(EZData):
        __kw_only__ = True
    self.assertEqual(context.exception.attributeName, '__kw_only__')

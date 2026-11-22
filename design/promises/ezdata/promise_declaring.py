"""
PromiseDeclaring promises how an 'EZData' class declares its fields,
from 'worktoy.ezdata'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.ezdata import EZData, EZField, fields


class PromiseDeclaring(TestCase):
  """
  An 'EZData' class declares its fields in its body, in order, as
  'EZField[T](...)' or as a plain value whose type becomes the field type; an
  annotation alone declares nothing. A default is built anew for each
  instance, so a mutable default is never shared. A lone value already of the
  field type is copied; a lone value of another type converts as 'typeCast'
  does when the field type is a number or a text, a subclass of one or a
  class with a '__cast_as__' hook; in every other case the type is called
  with the arguments, so 'EZField[list]('abc')' holds the three letters.
  'fields(cls)' and 'fields(instance)' give the fields in order. Source: the
  docstrings of 'EZData', 'EZField', 'EZSpace' and 'fields'.
  """

  def test_fields(self) -> None:
    class Point(EZData):
      x = EZField[float](0.0)
      y = 0.0
      label: str

    self.assertEqual([f.fieldName for f in fields(Point)], ['x', 'y'])
    self.assertEqual([f.fieldName for f in fields(Point())], ['x', 'y'])
    self.assertIs(fields(Point)[1].fieldType, float)

  def test_defaults(self) -> None:
    class Bag(EZData):
      items = EZField[list]()
      letters = EZField[list]('abc')
      tags = EZField[list](['new'])

    first, second = Bag(), Bag()
    first.items.append('apple')
    first.tags.append('used')
    self.assertEqual(second.items, [])
    self.assertEqual(second.tags, ['new'])
    self.assertEqual(first.letters, ['a', 'b', 'c'])

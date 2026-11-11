"""
PromiseParseKwargs promises 'Object.parseKwargs' from 'worktoy.core'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.core import Object
from worktoy.waitaminute import TypeException


class PromiseParseKwargs(TestCase):
  """
  'Object.parseKwargs(*namesAndTypes, **kwargs)' reads an option that
  goes by several names, as 'frozen' or 'readOnly'. The strings among
  the positional arguments are the names, and the classes the accepted
  types. It returns the value of the first name present, in the order
  the names were given, and the other keywords, a second synonym
  included, or 'None' and all the keywords when no name is present. A
  'float' accepts an 'int', a 'complex' accepts both, and a 'bool'
  passes as an 'int', but an 'int' is no 'bool'; the value comes back as
  given, not cast. A value of no accepted type raises
  'TypeException'. Source: the 'parseKwargs' docstring.
  """

  def test_synonyms(self) -> None:
    value, rest = Object.parseKwargs('frozen', 'readOnly', bool,
                                     readOnly=True, other=1)
    self.assertIs(value, True)
    self.assertEqual(rest, {'other': 1})

  def test_first_name_wins(self) -> None:
    value, rest = Object.parseKwargs('frozen', 'readOnly', bool,
                                     readOnly=False, frozen=True)
    self.assertIs(value, True)
    self.assertEqual(rest, {'readOnly': False})

  def test_bool_passes_as_int(self) -> None:
    value, _ = Object.parseKwargs('count', int, count=True)
    self.assertIs(value, True)
    with self.assertRaises(TypeException):
      Object.parseKwargs('flag', bool, flag=1)

  def test_absent(self) -> None:
    value, rest = Object.parseKwargs('frozen', bool, other=1)
    self.assertIsNone(value)
    self.assertEqual(rest, {'other': 1})

  def test_number_widening(self) -> None:
    value, rest = Object.parseKwargs('scale', float, scale=2)
    self.assertEqual(value, 2)
    self.assertIs(type(value), int)
    value, _ = Object.parseKwargs('shift', complex, shift=1.5)
    self.assertEqual(value, 1.5)

  def test_wrong_type(self) -> None:
    with self.assertRaises(TypeException) as context:
      Object.parseKwargs('scale', float, scale='2')
    e = context.exception
    self.assertEqual(e.varName, 'scale')
    self.assertEqual(e.actualObject, '2')
    self.assertIs(e.actualType, str)
    self.assertIn(float, e.expectedTypes)

"""
TestParseKwargs tests 'Object.parseKwargs' from 'worktoy.core'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core import Object
from worktoy.waitaminute import TypeException
from . import CoreTest


class TestParseKwargs(CoreTest):
  """
  An option given by keyword may go by several names, and must be read
  once, checked for its type and removed from the keywords passed on.
  'parseKwargs' takes the names and types in any order. The tests pin
  the first synonym winning, the removal, the refusal of a wrong type
  naming every accepted type, the widening of 'float' and 'complex' to
  the narrower numbers, 'bool' passing as 'int', and the two ways of
  finding nothing.
  """

  def test_first_name_taken_and_removed(self) -> None:
    value, rest = Object.parseKwargs(
        'frozen', 'readOnly', bool, frozen=True, readOnly=False, other=1)
    self.assertIs(value, True)
    self.assertEqual(rest, {'readOnly': False, 'other': 1})

  def test_second_synonym_found_when_first_absent(self) -> None:
    value, rest = Object.parseKwargs('frozen', 'readOnly', bool,
                                     readOnly=True)
    self.assertIs(value, True)
    self.assertEqual(rest, {})

  def test_names_and_types_in_any_order(self) -> None:
    value, rest = Object.parseKwargs(int, 'count', str, count='7')
    self.assertEqual(value, '7')
    self.assertEqual(rest, {})

  def test_no_names_given(self) -> None:
    given = {'a': 1}
    value, rest = Object.parseKwargs(int, **given)
    self.assertIsNone(value)
    self.assertEqual(rest, given)
    self.assertIsNot(rest, given)

  def test_no_name_present(self) -> None:
    value, rest = Object.parseKwargs('count', int, other=2)
    self.assertIsNone(value)
    self.assertEqual(rest, {'other': 2})

  def test_no_types_accepts_anything(self) -> None:
    value, rest = Object.parseKwargs('key', key=object)
    self.assertIs(value, object)
    self.assertEqual(rest, {})

  def test_unused_positional_ignored(self) -> None:
    value, rest = Object.parseKwargs('key', 5, int, key=1)
    self.assertEqual(value, 1)

  def test_wrong_type_refused(self) -> None:
    with self.assertRaises(TypeException) as context:
      Object.parseKwargs('count', int, count='7')
    self.assertEqual(context.exception.varName, 'count')
    self.assertEqual(context.exception.actualObject, '7')
    self.assertIs(context.exception.actualType, str)
    self.assertEqual(context.exception.expectedTypes, (int,))
    self.assertIn("'count'", str(context.exception))
    self.assertIn("'int'", str(context.exception))

  def test_float_admits_int(self) -> None:
    value, _ = Object.parseKwargs('x', float, x=2)
    self.assertEqual(value, 2)
    self.assertIs(type(value), int)
    with self.assertRaises(TypeException) as context:
      Object.parseKwargs('x', float, x='2')
    self.assertEqual(context.exception.varName, 'x')
    self.assertEqual(context.exception.actualObject, '2')
    self.assertIs(context.exception.actualType, str)
    self.assertEqual(context.exception.expectedTypes, (float, int))
    self.assertIn("'float' or 'int'", str(context.exception))

  def test_complex_admits_float_and_int(self) -> None:
    self.assertEqual(Object.parseKwargs('z', complex, z=1.5)[0], 1.5)
    self.assertEqual(Object.parseKwargs('z', complex, z=2)[0], 2)
    with self.assertRaises(TypeException) as context:
      Object.parseKwargs('z', complex, z='2')
    self.assertEqual(context.exception.varName, 'z')
    self.assertEqual(context.exception.actualObject, '2')
    self.assertIs(context.exception.actualType, str)
    self.assertEqual(context.exception.expectedTypes, (complex, float, int))
    self.assertIn("'complex', 'float' or 'int'", str(context.exception))

  def test_listed_numbers_not_repeated(self) -> None:
    with self.assertRaises(TypeException) as context:
      Object.parseKwargs('z', complex, float, z='2')
    self.assertEqual(context.exception.expectedTypes, (complex, float, int))
    self.assertEqual(context.exception.varName, 'z')
    self.assertIs(context.exception.actualType, str)
    self.assertIn("'complex', 'float' or 'int'", str(context.exception))
    with self.assertRaises(TypeException) as context:
      Object.parseKwargs('z', complex, int, z='2')
    self.assertEqual(context.exception.expectedTypes, (complex, int, float))
    self.assertEqual(context.exception.actualObject, '2')
    self.assertIn("'complex', 'int' or 'float'", str(context.exception))
    with self.assertRaises(TypeException) as context:
      Object.parseKwargs('x', float, int, x='2')
    self.assertEqual(context.exception.expectedTypes, (float, int))
    self.assertEqual(context.exception.varName, 'x')
    self.assertIn("'float' or 'int'", str(context.exception))

  def test_bool_passes_as_int(self) -> None:
    value, _ = Object.parseKwargs('n', int, n=True)
    self.assertIs(value, True)

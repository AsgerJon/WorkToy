"""
TestFastBoxDefaultRules subclasses 'DescTest' and pins that the default
a 'FastBox' builds follows the two rules 'AttriBox' applies to its own:
the value built must be an instance of the field type, and a builtin
container field type refuses a lone text argument rather than splitting
it into characters or integers. 'FastBox' used to store whatever the
field type returned, so 'FastBox[list]('abc')' defaulted to
'['a', 'b', 'c']'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import FastBox
from worktoy.waitaminute import TypeException

from . import DescTest


class Odd:
  """Odd has a constructor returning something other than an 'Odd'."""

  def __new__(cls, *args) -> int:
    return 69


class Holder:
  """Holder declares the boxes under test."""

  letters = FastBox[list]('abc')
  octets = FastBox[tuple](b'ab')
  chars = FastBox[set](bytearray(b'ab'))
  odd = FastBox[Odd]()
  numbers = FastBox[list]((1, 2))
  word = FastBox[str]('word')


class TestFastBoxDefaultRules(DescTest):
  """
  TestFastBoxDefaultRules provides tests for the rules the default of a
  'FastBox' follows.
  """

  def test_container_refuses_text(self) -> None:
    """A container field type refuses a lone 'str', 'bytes' or
    'bytearray' default with 'TypeException' naming the field."""
    for name in ('letters', 'octets', 'chars'):
      with self.subTest(name=name):
        with self.assertRaises(TypeException) as context:
          getattr(Holder(), name)
        self.assertEqual(context.exception.varName, name)

  def test_result_must_be_field_type(self) -> None:
    """A field type whose constructor returns something else raises
    'TypeException' naming the field and the value returned."""
    with self.assertRaises(TypeException) as context:
      _ = Holder().odd
    self.assertEqual(context.exception.varName, 'odd')
    self.assertEqual(context.exception.actualObject, 69)
    self.assertEqual(context.exception.expectedTypes, (Odd,))

  def test_container_converts_iterable(self) -> None:
    """A container field type still converts a lone iterable that is not
    text, and a text field type still takes text."""
    holder = Holder()
    self.assertEqual(holder.numbers, [1, 2])
    self.assertEqual(holder.word, 'word')

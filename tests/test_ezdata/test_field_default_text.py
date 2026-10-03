"""
TestFieldDefaultText subclasses 'EZTest' and pins that an 'EZField'
default follows the text rules of 'AttriBox'. A lone default for a text
type, 'str', 'bytes' or 'bytearray', goes through 'typeCast', as an
argument does, and a builtin container refuses a lone text default. The
default called the field type instead, so 'EZField[list]('abc')' gave
'['a', 'b', 'c']', 'EZField[str](5)' gave '5', and 'EZField[str](b'ab')'
gave "b'ab'", where the same value as an argument raised or gave 'ab'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.ezdata import EZData, EZField
from worktoy.waitaminute import TypeException

from . import EZTest


class Name(str):
  """Name is a 'str' that keeps the constructor of 'str'."""


class TestFieldDefaultText(EZTest):
  """
  TestFieldDefaultText provides tests for the text rules of an 'EZField'
  default.
  """

  def test_container_refuses_text(self) -> None:
    """A builtin container refuses a lone text default."""
    for type_ in (list, tuple, set, frozenset, dict):
      for text in ('abc', b'abc', bytearray(b'abc')):
        with self.subTest(fieldType=type_.__name__, text=text):
          class Holder(EZData):
            x = EZField[type_](text)
          with self.assertRaises(TypeException):
            Holder()

  def test_text_type_casts(self) -> None:
    """A text type casts a lone default as it casts an argument."""

    class Holder(EZData):
      name = EZField[str](b'ab')
      data = EZField[bytes]('ab')
      buffer = EZField[bytearray](b'ab')

    holder = Holder()
    self.assertEqual(holder.name, 'ab')
    self.assertEqual(holder.data, b'ab')
    self.assertEqual(holder.buffer, bytearray(b'ab'))
    self.assertIs(type(holder.buffer), bytearray)

  def test_text_subclass_casts(self) -> None:
    """A subclass of a text type casts a lone default as well."""

    class Holder(EZData):
      name = EZField[Name](b'ab')

    name = Holder().name
    self.assertEqual(name, 'ab')
    self.assertIs(type(name), Name)

  def test_text_type_refuses(self) -> None:
    """A text type refuses a lone default that is not text."""

    class Holder(EZData):
      name = EZField[str](5)

    with self.assertRaises(TypeException):
      Holder()

  def test_default_value_follows(self) -> None:
    """'defaultValue' builds the default by the same rules."""

    class Holder(EZData):
      name = EZField[str](b'ab')

    field, = Holder.fields
    self.assertEqual(field.defaultValue, 'ab')

  def test_container_from_iterable(self) -> None:
    """A container still takes a lone iterable that is not text."""

    class Holder(EZData):
      items = EZField[list]((1, 2))

    self.assertEqual(Holder().items, [1, 2])

  def test_constructor_for_several(self) -> None:
    """Several arguments, or keywords, still go to the constructor."""

    class Holder(EZData):
      name = EZField[str](b'\xe6', 'latin-1')
      word = EZField[str](b'\xe6', encoding='latin-1')

    holder = Holder()
    self.assertEqual(holder.name, '\xe6')
    self.assertEqual(holder.word, '\xe6')

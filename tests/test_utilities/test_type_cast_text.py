"""
TestTypeCastText subclasses 'UtilitiesTest' and pins how 'typeCast'
treats the three text types, 'str', 'bytes' and 'bytearray'. Their
constructors accept almost anything: 'str(x)' never fails, and 'bytes(5)'
gives five zero bytes. 'typeCast' therefore does not call them, but
converts between the three text types losslessly as UTF-8, and refuses
everything else with 'TypeCastException'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.utilities import typeCast
from worktoy.waitaminute.dispatch import TypeCastException

from . import UtilitiesTest


class TestTypeCastText(UtilitiesTest):
  """
  TestTypeCastText provides tests for 'typeCast' to 'str', 'bytes' and
  'bytearray'.
  """

  def test_bytes_from_text(self) -> None:
    """A 'str' is encoded as UTF-8 and a 'bytearray' copied into
    'bytes'."""
    cast = typeCast(bytes, 'blåbær')
    self.assertIs(type(cast), bytes)
    self.assertEqual(cast, 'blåbær'.encode('utf-8'))
    cast = typeCast(bytes, bytearray(b'abc'))
    self.assertIs(type(cast), bytes)
    self.assertEqual(cast, b'abc')

  def test_bytearray_from_text(self) -> None:
    """A 'str' is encoded as UTF-8 and a 'bytes' copied into a
    'bytearray'."""
    cast = typeCast(bytearray, 'blåbær')
    self.assertIs(type(cast), bytearray)
    self.assertEqual(cast, bytearray('blåbær'.encode('utf-8')))
    cast = typeCast(bytearray, b'abc')
    self.assertIs(type(cast), bytearray)
    self.assertEqual(cast, bytearray(b'abc'))

  def test_str_from_text(self) -> None:
    """A 'bytes' or a 'bytearray' is decoded as UTF-8."""
    self.assertEqual(typeCast(str, 'blåbær'.encode('utf-8')), 'blåbær')
    self.assertEqual(typeCast(str, bytearray(b'abc')), 'abc')

  def test_value_of_the_target_unchanged(self) -> None:
    """A value already of the target type is returned as it is."""
    data = b'abc'
    self.assertIs(typeCast(bytes, data), data)
    buffer = bytearray(b'abc')
    self.assertIs(typeCast(bytearray, buffer), buffer)

  def test_non_text_refused(self) -> None:
    """Anything but the three text types is refused, where the
    constructors would turn it into zero bytes, a byte string of its
    items, or its 'str' rendering."""
    values = (5, 0, None, 2.5, [65, 66], (65, 66), object())
    for target in (str, bytes, bytearray):
      for value in values:
        with self.subTest(target=target.__name__, value=repr(value)):
          with self.assertRaises(TypeCastException) as context:
            typeCast(target, value)
          self.assertIs(context.exception.type_, target)

  def test_unencodable_text_refused(self) -> None:
    """A 'str' that UTF-8 cannot encode, such as a lone surrogate, is
    refused, chained from the 'UnicodeEncodeError'."""
    for target in (bytes, bytearray):
      with self.subTest(target=target.__name__):
        with self.assertRaises(TypeCastException) as context:
          typeCast(target, '\ud800')
        cause = context.exception.__cause__
        self.assertIsInstance(cause, UnicodeEncodeError)

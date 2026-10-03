"""
TestFieldTextCast subclasses 'EZTest' from the 'tests.test_ezdata'
package and pins how an 'EZData' class casts a constructor argument or an
assignment to a 'bytes' or 'bytearray' field. The cast takes text alone,
converted as UTF-8, as it already did for a 'str' field, so an 'int' is
refused rather than stored as zero bytes.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.ezdata import EZData, EZField
from worktoy.waitaminute import TypeException

from . import EZTest


class TestFieldTextCast(EZTest):
  """
  TestFieldTextCast provides tests for 'bytes' and 'bytearray' fields of
  an 'EZData' class.
  """

  def test_non_text_refused(self) -> None:
    """An 'int' given to a 'bytes' or 'bytearray' field, as an argument
    or by assignment, raises 'TypeException'."""

    class Packet(EZData):
      data = EZField[bytes](b'')
      buffer = EZField[bytearray](bytearray())

    with self.assertRaises(TypeException):
      Packet(4)
    with self.assertRaises(TypeException):
      Packet(buffer=4)
    packet = Packet()
    with self.assertRaises(TypeException):
      packet.data = 4
    with self.assertRaises(TypeException):
      packet.buffer = None

  def test_text_converted(self) -> None:
    """A 'str' is encoded as UTF-8, and 'bytes' and 'bytearray' convert
    into each other."""

    class Packet(EZData):
      data = EZField[bytes](b'')
      buffer = EZField[bytearray](bytearray())

    packet = Packet('blåbær', b'abc')
    self.assertEqual(packet.data, 'blåbær'.encode('utf-8'))
    self.assertEqual(packet.buffer, bytearray(b'abc'))
    self.assertIs(type(packet.buffer), bytearray)
    packet.data = bytearray(b'xyz')
    self.assertIs(type(packet.data), bytes)

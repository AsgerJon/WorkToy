"""
TestUnpackBytearray subclasses 'UtilitiesTest' and pins that 'unpack'
keeps a 'bytearray' whole, as it keeps 'str' and 'bytes'. The boxes count
the three as text, but 'unpack' split a 'bytearray' into its integers.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.utilities import unpack
from worktoy.waitaminute import UnpackException

from . import UtilitiesTest


class TestUnpackBytearray(UtilitiesTest):
  """
  TestUnpackBytearray provides tests for 'bytearray' arguments to
  'unpack'.
  """

  def test_nested_kept_whole(self) -> None:
    """A 'bytearray' inside a list comes out whole."""
    data = bytearray(b'ab')
    self.assertEqual(unpack([data, 1]), (data, 1))

  def test_top_level_kept_whole(self) -> None:
    """A 'bytearray' next to an iterable is kept as one item."""
    data = bytearray(b'ab')
    self.assertEqual(unpack(data, [1, 2]), (data, 1, 2))

  def test_alone_is_no_iterable(self) -> None:
    """A 'bytearray' alone is no iterable to unpack, as 'bytes' is not."""
    with self.assertRaises(UnpackException):
      unpack(bytearray(b'ab'))

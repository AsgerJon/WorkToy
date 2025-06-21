"""
TestUnpack verifies correct behavior of the 'unpack' function.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.core import unpack
from worktoy.waitaminute import UnpackException

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Self, TypeAlias, Any


class TestUnpack(TestCase):
  """
  Unit tests for the 'unpack' function.
  """

  def test_no_arguments_strict(self) -> None:
    """ No arguments, strict=True should raise """
    with self.assertRaises(UnpackException):
      unpack(strict=True)

  def test_no_arguments_non_strict(self) -> None:
    """ No arguments, strict=False should return empty """
    result = unpack(strict=False)
    self.assertEqual(result, ())

  def test_flat_args(self) -> None:
    """ Simple flat arguments """
    result = unpack(1, 2, 3, strict=False)
    self.assertEqual(result, (1, 2, 3))

  def test_simple_iterable_unpack(self) -> None:
    """ Unpack a simple iterable """
    result = unpack(1, [2, 3], 4)
    self.assertEqual(result, (1, 2, 3, 4))

  def test_nested_iterable_unpack(self) -> None:
    """ Unpack nested iterable """
    result = unpack(1, [2, [3, 4]], 5)
    self.assertEqual(result, (1, 2, 3, 4, 5))

  def test_shallow_unpack(self) -> None:
    """ Shallow unpack should not recurse """
    result = unpack(1, [2, [3, 4]], 5, shallow=True)
    self.assertEqual(result, (1, 2, [3, 4], 5))

  def test_str_and_bytes_not_unpacked(self) -> None:
    """ str and bytes should remain atomic """
    result = unpack('abc', b'def', 1, [2, 3])
    self.assertEqual(result, ('abc', b'def', 1, 2, 3))

  def test_strict_no_iterable_violation(self) -> None:
    """ strict=True, no iterable present → raise """
    with self.assertRaises(UnpackException):
      unpack(1, 2, 3, strict=True)

  def test_strict_false_no_iterable(self) -> None:
    """ strict=False, no iterable present → return args """
    result = unpack(1, 2, 3, strict=False)
    self.assertEqual(result, (1, 2, 3))

  def test_generator_unpack(self) -> None:
    """ Unpack a generator expression """
    result = unpack((x for x in (1, 2, 3)))
    self.assertEqual(result, (1, 2, 3))

  def test_empty_iterable_unpack(self) -> None:
    """ Unpack an empty iterable """
    result = unpack([])
    self.assertEqual(result, ())

  def test_none_in_args(self) -> None:
    """ Test None in args """
    result = unpack(None, [None, None])
    self.assertEqual(result, (None, None, None))

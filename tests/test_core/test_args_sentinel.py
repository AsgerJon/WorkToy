"""
TestArgsSentinel subclasses 'CoreTest' and pins how instances of the
'ARGS' sentinel compare, hash, and render. Every 'ARGS[int]' subscript
builds a new instance. Two variadic signatures written the same way must
still compare equal, so instances compare by their inner type, and equal
instances hash alike.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest.mock import ANY

from worktoy.core.sentinels import ARGS
from . import CoreTest


class TestArgsSentinel(CoreTest):
  """
  TestArgsSentinel pins equality, hashing, and rendering of 'ARGS'
  instances.
  """

  def test_equal_by_inner_type(self) -> None:
    """
    Testing that two separate subscripts with the same inner type give
    distinct but equal instances, and that a different inner type gives
    an unequal one.
    """
    self.assertIsNot(ARGS[int], ARGS[int])
    self.assertEqual(ARGS[int], ARGS[int])
    self.assertNotEqual(ARGS[int], ARGS[str])

  def test_unequal_to_other_objects(self) -> None:
    """
    Testing that an instance equals neither its inner type nor a string
    spelling of itself.
    """
    self.assertNotEqual(ARGS[int], int)
    self.assertNotEqual(ARGS[int], 'ARGS[int]')

  def test_defers_to_other_operand(self) -> None:
    """
    Testing that an instance leaves the comparison with anything other
    than an 'ARGS' instance to the other operand, rather than deciding
    it. 'ANY' from 'unittest.mock' claims equality with everything, and
    it must be given the chance to.
    """
    self.assertTrue(ARGS[int] == ANY)

  def test_equal_instances_hash_alike(self) -> None:
    """
    Testing that equal instances hash alike, so that instances written
    separately collapse into a single entry of a set.
    """
    self.assertEqual(hash(ARGS[int]), hash(ARGS[int]))
    self.assertEqual(len({ARGS[int], ARGS[int], ARGS[str]}), 2)

  def test_str_repr(self) -> None:
    """
    Testing that both 'str' and 'repr' render the subscript that created
    the instance.
    """
    self.assertEqual(str(ARGS[int]), 'ARGS[int]')
    self.assertEqual(repr(ARGS[str]), 'ARGS[str]')

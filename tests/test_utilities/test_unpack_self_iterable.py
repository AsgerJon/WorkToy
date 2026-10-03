"""
TestUnpackSelfIterable subclasses 'UtilitiesTest' and pins that 'unpack'
keeps whole an item that yields itself when iterated, such as an
'ARGS[int]' or a list holding itself. It used to unpack such an item
again and again, until 'RecursionError'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core.sentinels import ARGS
from worktoy.utilities import unpack

from . import UtilitiesTest


class TestUnpackSelfIterable(UtilitiesTest):
  """
  TestUnpackSelfIterable provides tests for 'unpack' given iterables that
  yield themselves.
  """

  def test_args(self) -> None:
    """An 'ARGS' instance, which yields itself, is kept whole."""
    variadic = ARGS[int]
    self.assertEqual(unpack(variadic), (variadic,))
    self.assertEqual(unpack([1, variadic]), (1, variadic))

  def test_list_holding_itself(self) -> None:
    """A list holding itself keeps that entry whole."""
    loop = [1]
    loop.append(loop)
    self.assertEqual(unpack(loop), (1, loop))

  def test_nested_lists(self) -> None:
    """Ordinary nesting still flattens."""
    self.assertEqual(unpack([1, [2, [3]]]), (1, 2, 3))

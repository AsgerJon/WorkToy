"""
TestFieldUnhashableSet subclasses 'EZTest' from the 'tests.test_ezdata'
package and pins that assigning a value with an unhashable element to a
'set' field of an 'EZData' class raises 'TypeException' naming the
field, like every other refused assignment, instead of the bare
'TypeError' that used to escape from 'typeCast' past 'EZHook.castField'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.ezdata import EZData, EZField
from worktoy.waitaminute import TypeException

from . import EZTest


class Tagged(EZData):
  """Tagged holds a 'set' field for the assignment probes."""

  tags = EZField[set]()


class TestFieldUnhashableSet(EZTest):
  """
  TestFieldUnhashableSet provides tests for unhashable elements assigned
  to a 'set' field, by assignment and through the constructor.
  """

  def test_assignment_refused(self) -> None:
    """The assignment raises 'TypeException' naming the field, and the
    field keeps its value."""
    tagged = Tagged({1})
    with self.assertRaises(TypeException) as context:
      tagged.tags = [[1], [2]]
    self.assertEqual(context.exception.varName, 'tags')
    self.assertEqual(tagged.tags, {1})

  def test_constructor_refused(self) -> None:
    """The constructor casts the same way, so it refuses the value with
    'TypeException' as well."""
    with self.assertRaises(TypeException) as context:
      Tagged([[1], [2]])
    self.assertEqual(context.exception.varName, 'tags')

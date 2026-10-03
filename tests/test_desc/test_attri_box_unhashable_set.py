"""
TestAttriBoxUnhashableSet subclasses 'DescTest' from the 'tests.test_desc'
package and pins that assigning a value with an unhashable element to an
'AttriBox[set]' raises 'TypeException' naming the value, like every other
refused assignment, instead of the bare 'TypeError' that used to escape
from 'typeCast'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import AttriBox
from worktoy.waitaminute import TypeException

from . import DescTest


class TestAttriBoxUnhashableSet(DescTest):
  """
  TestAttriBoxUnhashableSet provides tests for unhashable elements
  assigned to 'set' and 'frozenset' fields.
  """

  def test_unhashable_element_refused(self) -> None:
    """The assignment raises 'TypeException' and the field keeps its
    value. Only a container is tried here: a dict the cast refuses
    falls back to the field-type constructor, which builds a set of the
    dict's keys, the lenient fallback item 30 of the 1.1 audit revisits."""

    class Foo:
      tags = AttriBox[set]({1})
      marks = AttriBox[frozenset]()

    foo = Foo()
    with self.assertRaises(TypeException) as context:
      foo.tags = [[1], [2]]
    self.assertEqual(context.exception.actualObject, [[1], [2]])
    self.assertEqual(foo.tags, {1})
    with self.assertRaises(TypeException):
      foo.marks = ([1],)
    self.assertEqual(foo.marks, frozenset())

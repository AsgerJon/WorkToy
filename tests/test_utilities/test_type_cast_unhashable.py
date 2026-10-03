"""
TestTypeCastUnhashable subclasses 'UtilitiesTest' from the
'tests.test_utilities' package and pins that 'typeCast' to 'set' or
'frozenset' refuses a value with an unhashable element by raising
'TypeCastException', as it does for every other failed cast. The
constructions used to run unguarded, so Python's own 'TypeError' escaped
instead, past every caller that catches 'TypeCastException'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.utilities import typeCast
from worktoy.waitaminute.dispatch import TypeCastException

from . import UtilitiesTest


class TestTypeCastUnhashable(UtilitiesTest):
  """
  TestTypeCastUnhashable provides tests for casts to 'set' and
  'frozenset' of values holding unhashable elements.
  """

  def test_container_with_unhashable_element(self) -> None:
    """A container holding an unhashable element is refused with
    'TypeCastException', chained from the 'TypeError' behind it."""
    for target in (set, frozenset):
      for value in ([[1], [2]], ([1],)):
        with self.subTest(target=target.__name__, value=value):
          with self.assertRaises(TypeCastException) as context:
            typeCast(target, value)
          e = context.exception
          self.assertIs(e.type_, target)
          self.assertIs(e.arg, value)
          self.assertIsInstance(e.__cause__, TypeError)

  def test_dict_with_unhashable_value(self) -> None:
    """A dict whose pairs hold an unhashable value is refused the same
    way, through the branch converting its items."""
    value = {'a': [1]}
    for target in (set, frozenset):
      with self.subTest(target=target.__name__):
        with self.assertRaises(TypeCastException) as context:
          typeCast(target, value)
        e = context.exception
        self.assertIs(e.type_, target)
        self.assertIs(e.arg, value)
        self.assertIsInstance(e.__cause__, TypeError)

  def test_hashable_elements_still_cast(self) -> None:
    """Containers and dicts with hashable elements still convert."""
    self.assertEqual(typeCast(set, [1, 2, 2]), {1, 2})
    self.assertEqual(typeCast(frozenset, (1, 2)), frozenset({1, 2}))
    self.assertEqual(typeCast(set, {'a': 1}), {('a', 1)})
    self.assertEqual(typeCast(list, {'a': 1}), [('a', 1)])

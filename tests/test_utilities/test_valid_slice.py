"""
TestValidSlice tests 'ValidSlice' from 'worktoy.utilities'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from types import SimpleNamespace

from worktoy.utilities import ValidSlice
from . import UtilitiesTest, Indexed, BadIndexed, RaisingIndexed


class TestValidSlice(UtilitiesTest):
  """
  'slice' accepts any components and fails only when used, so a class
  taking a slice must check it first. 'isinstance(s, ValidSlice)' is
  that check: true when every component is 'None', an 'int' or an
  object whose type has a callable '__index__', which is not called.
  The tests pin the docstring examples, each component position, the
  three ways a component fails, that the lookup is on the type, that
  the class cannot be instantiated, and its string forms.
  """

  def test_docstring_examples(self) -> None:
    self.assertFalse(isinstance(slice('not a slice'), ValidSlice))
    self.assertFalse(isinstance(slice(0, 10, 'step'), ValidSlice))
    self.assertTrue(isinstance(slice(1), ValidSlice))
    self.assertTrue(isinstance(slice(None, None, None), ValidSlice))

  def test_not_a_slice(self) -> None:
    for value in (5, 'x', None, (1, 2), range(3), [slice(1)]):
      with self.subTest(value=value):
        self.assertFalse(isinstance(value, ValidSlice))

  def test_int_and_bool_components(self) -> None:
    self.assertTrue(isinstance(slice(1, -5, 2), ValidSlice))
    self.assertTrue(isinstance(slice(True, False, True), ValidSlice))

  def test_indexed_components(self) -> None:
    self.assertEqual(range(5)[slice(Indexed(1), Indexed(3))], range(1, 3))
    self.assertTrue(isinstance(slice(Indexed(1)), ValidSlice))
    self.assertTrue(isinstance(slice(None, Indexed(2)), ValidSlice))
    self.assertTrue(isinstance(slice(0, 2, Indexed(1)), ValidSlice))
    self.assertTrue(isinstance(slice(Indexed(0), Indexed(2), Indexed(1)),
                               ValidSlice))

  def test_index_not_called(self) -> None:
    self.assertTrue(isinstance(slice(RaisingIndexed()), ValidSlice))
    with self.assertRaises(RuntimeError) as context:
      range(5)[slice(RaisingIndexed())]
    self.assertEqual(str(context.exception), '__index__ was called')

  def test_component_without_index(self) -> None:
    for value in ('x', 1.5, 2j, [1], object()):
      with self.subTest(value=value):
        self.assertFalse(isinstance(slice(value), ValidSlice))
        self.assertFalse(isinstance(slice(None, value), ValidSlice))
        self.assertFalse(isinstance(slice(None, None, value), ValidSlice))

  def test_component_with_uncallable_index(self) -> None:
    self.assertFalse(isinstance(slice(BadIndexed()), ValidSlice))
    self.assertFalse(isinstance(slice(0, BadIndexed()), ValidSlice))

  def test_index_looked_up_on_type(self) -> None:
    #  An '__index__' set on the instance alone does not count, as the
    #  interpreter itself looks special methods up on the type.
    value = SimpleNamespace(__index__=lambda: 1)
    self.assertFalse(isinstance(slice(value), ValidSlice))

  def test_first_bad_component_decides(self) -> None:
    self.assertFalse(isinstance(slice(Indexed(1), 'x', 1), ValidSlice))
    self.assertFalse(isinstance(slice('x', Indexed(1), 1), ValidSlice))

  def test_cannot_instantiate(self) -> None:
    with self.assertRaises(TypeError) as context:
      ValidSlice()
    self.assertIn('ValidSlice cannot be instantiated',
                  str(context.exception))
    with self.assertRaises(TypeError) as context:
      ValidSlice(1, 2, key=3)
    self.assertIn('ValidSlice cannot be instantiated',
                  str(context.exception))

  def test_str_and_repr(self) -> None:
    self.assertEqual(str(ValidSlice),
                     "<type 'ValidSlice' | slice object validator>")
    self.assertEqual(repr(ValidSlice), 'worktoy.utilities.ValidSlice')

  def test_random_int_slices_valid(self) -> None:
    self.randomInteger.size = 3
    for _ in range(10):
      start, stop, step = self.randomInteger.row
      with self.subTest(start=start, stop=stop, step=step):
        self.assertTrue(isinstance(slice(start, stop, step), ValidSlice))

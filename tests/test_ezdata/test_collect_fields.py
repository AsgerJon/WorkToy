"""Tests for ``collectFields``."""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.ezdata import collectFields
from . import EZTest
from ._factory_helpers import slot


class TestCollectFields(EZTest):

  def test_empty_inputs(self) -> None:
    self.assertEqual(collectFields({}, (), {}, 'C'), [])

  def test_inherited_only(self) -> None:
    parentSlot = slot('x', int, 1)

    class Parent:
      __slot_objects__ = (parentSlot,)

    fields = collectFields({}, (Parent,), {}, 'C')
    self.assertEqual(len(fields), 1)
    self.assertEqual(fields[0].name, 'x')
    self.assertEqual(fields[0].typeValue, int)
    self.assertEqual(fields[0].defaultValue, 1)

  def test_annotated_with_default(self) -> None:
    compiled = {'x': 5}
    fields = collectFields(compiled, (), {'x': int}, 'C')
    self.assertEqual(len(fields), 1)
    self.assertEqual(fields[0].defaultValue, 5)
    self.assertNotIn('x', compiled)

  def test_annotated_without_default(self) -> None:
    fields = collectFields({}, (), {'x': int}, 'C')
    self.assertEqual(len(fields), 1)
    self.assertIsNone(fields[0].defaultValue)

  def test_annotated_skips_dunder(self) -> None:
    fields = collectFields({}, (), {'__module__': str}, 'C')
    self.assertEqual(fields, [])

  def test_defaulted_no_annotation(self) -> None:
    compiled = {'x': 5}
    fields = collectFields(compiled, (), {}, 'C')
    self.assertEqual(len(fields), 1)
    self.assertEqual(fields[0].typeValue, int)
    self.assertNotIn('x', compiled)

  def test_defaulted_skips_non_candidates(self) -> None:
    def fn() -> int:
      return 0

    self.assertFalse(fn())

    compiled = {'x': 5, 'fn': fn, '__init__': lambda s: None}
    fields = collectFields(compiled, (), {}, 'C')
    names = [f.name for f in fields]
    self.assertEqual(names, ['x'])
    self.assertIn('fn', compiled)

  def test_redefining_inherited_via_annotation(self) -> None:
    parentSlot = slot('x', int, 1)

    class Parent:
      __slot_objects__ = (parentSlot,)

    fields = collectFields({'x': 'hello'}, (Parent,), {'x': str}, 'C')
    self.assertEqual(len(fields), 1)
    self.assertEqual(fields[0].typeValue, str)
    self.assertEqual(fields[0].defaultValue, 'hello')

  def test_redefining_inherited_via_default(self) -> None:
    parentSlot = slot('x', int, 1)

    class Parent:
      __slot_objects__ = (parentSlot,)

    compiled = {'x': 99}
    fields = collectFields(compiled, (Parent,), {}, 'C')
    self.assertEqual(len(fields), 1)
    self.assertEqual(fields[0].defaultValue, 99)

  def test_string_annotation_resolved(self) -> None:
    fields = collectFields({'x': 5}, (), {'x': 'int'}, 'C')
    self.assertEqual(len(fields), 1)
    self.assertIs(fields[0].typeValue, int)

  def test_unknown_string_annotation_falls_back_to_default_type(
      self
  ) -> None:
    fields = collectFields(
      {'x': 'hello'}, (), {'x': 'Optional[int]'}, 'C'
    )
    self.assertIs(fields[0].typeValue, str)

  def test_unknown_string_annotation_no_default_falls_back_to_object(
      self
  ) -> None:
    fields = collectFields({}, (), {'x': 'Optional[int]'}, 'C')
    self.assertIs(fields[0].typeValue, object)

  def test_duplicate_inherited_slot_name_keeps_first(self) -> None:
    s1 = slot('x', int, 1)
    s2 = slot('x', str, 'hello')

    class ParentA:
      __slot_objects__ = (s1,)

    class ParentB:
      __slot_objects__ = (s2,)

    fields = collectFields({}, (ParentA, ParentB), {}, 'C')
    self.assertEqual(len(fields), 1)
    self.assertEqual(fields[0].name, 'x')
    self.assertIs(fields[0].typeValue, int)
    self.assertEqual(fields[0].defaultValue, 1)

"""
TestFastBoxGeneric pins the generic subscript path of 'FastBox'. A
'TypeVar' subscript such as 'FastBox[T]' must reach the generic
machinery so 'class Sub(FastBox[T])' declares a generic subclass, while
a concrete subscript on the subclass still produces a working,
type-enforced descriptor, exactly as 'AttriBox' behaves.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TypeVar

from worktoy.desc import FastBox
from worktoy.waitaminute import TypeException
from . import DescTest

T = TypeVar('T')


class _SubBox(FastBox[T]):
  """A generic subclass of 'FastBox', whose creation exercises the
  'TypeVar' branch of '__class_getitem__'."""


class _Owner:
  """An owner using the generic subclass with a concrete subscript."""

  count = _SubBox[int](42)


class TestFastBoxGeneric(DescTest):
  """
  TestFastBoxGeneric pins generic subclassing of 'FastBox' and the
  typing of a concrete subscript on the resulting subclass.
  """

  def test_generic_subclass_creates(self) -> None:
    """The generic subclass exists and is a 'FastBox' subclass; merely
    reaching this assertion proves 'class Sub(FastBox[T])' created."""
    self.assertTrue(issubclass(_SubBox, FastBox))

  def test_concrete_subscript_is_descriptor(self) -> None:
    """A concrete subscript on the subclass yields a descriptor of the
    subclass, carrying the concrete field type."""
    self.assertIsInstance(_Owner.count, _SubBox)
    self.assertIs(_Owner.count.__field_type__, int)

  def test_concrete_subscript_value_contract(self) -> None:
    """The subclassed descriptor still lazily builds its default,
    accepts a write of the field type and rejects any other type."""
    owner = _Owner()
    self.assertEqual(owner.count, 42)
    owner.count = 69
    self.assertEqual(owner.count, 69)
    with self.assertRaises(TypeException) as context:
      owner.count = 'breh'
    e = context.exception
    self.assertEqual(e.varName, 'count')
    self.assertEqual(e.actualObject, 'breh')

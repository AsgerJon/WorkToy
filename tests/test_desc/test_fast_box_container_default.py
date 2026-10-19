"""
TestFastBoxContainerDefault subclasses 'DescTest' and pins how 'FastBox'
builds a default for a builtin container from several arguments: the
field type is called on the arguments first, and when that call is
refused and the field type is a builtin container, it is called once
more with the arguments as its one iterable, so 'FastBox[tuple](1, 2)'
holds '(1, 2)' as 'AttriBox' does. The default used to be built as
'fieldType(*args)' alone, so that declaration raised the raw 'TypeError'
of 'tuple' at the first read. A refused call on any other field type
raises 'TypeException' naming the field rather than being retried.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import FastBox
from worktoy.waitaminute import TypeException

from . import DescTest


class Pair:
  """Pair takes exactly two arguments."""

  def __init__(self, left: int, right: int) -> None:
    self.left, self.right = left, right


class Holder:
  """Holder declares the defaults under test."""

  pair = FastBox[tuple](1, 2)
  items = FastBox[list](1, 2, 3)
  unique = FastBox[set](1, 1, 2)
  frozen = FastBox[frozenset](3, 4)
  table = FastBox[dict](('a', 1), ('b', 2))
  whole = FastBox[tuple]((1, 2))
  empty = FastBox[tuple]()
  word = FastBox[str]('ab')
  good = FastBox[Pair](1, 2)


class TestFastBoxContainerDefault(DescTest):
  """
  TestFastBoxContainerDefault provides tests for container defaults of
  'FastBox'.
  """

  def test_several_arguments_are_the_elements(self) -> None:
    """Each builtin container takes several arguments as its elements."""
    holder = Holder()
    self.assertEqual(holder.pair, (1, 2))
    self.assertEqual(holder.items, [1, 2, 3])
    self.assertEqual(holder.unique, {1, 2})
    self.assertEqual(holder.frozen, frozenset((3, 4)))
    self.assertEqual(holder.table, {'a': 1, 'b': 2})

  def test_single_and_none_unchanged(self) -> None:
    """One argument is converted as a whole, none gives the empty
    container, and other field types build as before."""
    holder = Holder()
    self.assertEqual(holder.whole, (1, 2))
    self.assertEqual(holder.empty, ())
    self.assertEqual(holder.word, 'ab')
    self.assertEqual((holder.good.left, holder.good.right), (1, 2))

  def test_text_still_refused(self) -> None:
    """A lone string for a container is still refused, not split."""

    class Owner:
      letters = FastBox[list]('abc')

    with self.assertRaises(TypeException):
      _ = Owner().letters

  def test_other_types_not_retried(self) -> None:
    """A refused call on a field type that is no builtin container
    raises 'TypeException' naming the field, without a second call."""

    class Owner:
      triple = FastBox[Pair](1, 2, 3)
      text = FastBox[str](1, 2)

    with self.assertRaises(TypeException) as context:
      _ = Owner().triple
    self.assertEqual(context.exception.varName, 'triple')
    with self.assertRaises(TypeException):
      _ = Owner().text

  def test_container_refusing_twice(self) -> None:
    """A container refusing the arguments both ways names the field."""

    class Owner:
      table = FastBox[dict](1, 2)

    with self.assertRaises(TypeException) as context:
      _ = Owner().table
    self.assertEqual(context.exception.varName, 'table')

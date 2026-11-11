"""
PromiseBoxRefusals promises the box declarations 'worktoy.desc' refuses
as the class is created.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.desc import AttriBox
from worktoy.mcls import BaseObject
from worktoy.waitaminute.desc import MissingInstanceDict, SharedDescriptor


class PromiseBoxRefusals(TestCase):
  """
  As the class is created, an 'AttriBox' declared without parentheses
  raises 'TypeError', and one placed on a class whose instances have no
  '__dict__', as a class declaring '__slots__', raises
  'MissingInstanceDict'. One box placed on a second class raises
  'SharedDescriptor', while the same box bound to a second name in one
  body gives a second attribute of its own. Before Python 3.12 the
  interpreter wraps a refusal raised while it places the attributes of a
  class in a 'RuntimeError'. Source: the docstrings of 'AttriBox' and
  'BaseDescriptor'.
  """

  def unwrap(self, exception: BaseException) -> BaseException:
    return exception.__cause__ or exception

  def test_no_parentheses(self) -> None:
    with self.assertRaises((TypeError, RuntimeError)) as context:
      class Point(BaseObject):
        x = AttriBox[float]
    self.assertIsInstance(self.unwrap(context.exception), TypeError)

  def test_no_instance_dict(self) -> None:
    with self.assertRaises((MissingInstanceDict, RuntimeError)) as context:
      class Slotted:
        __slots__ = ('a',)
        x = AttriBox[int](0)
    refusal = self.unwrap(context.exception)
    self.assertIsInstance(refusal, MissingInstanceDict)
    self.assertEqual(refusal.ownerName, 'Slotted')
    self.assertEqual(refusal.fieldName, 'x')

  def test_second_class(self) -> None:
    box = AttriBox[int](0)

    class First(BaseObject):
      x = box

    with self.assertRaises((SharedDescriptor, RuntimeError)) as context:
      class Second(BaseObject):
        y = box
    refusal = self.unwrap(context.exception)
    self.assertIsInstance(refusal, SharedDescriptor)
    self.assertIs(refusal.desc, box)
    self.assertIs(refusal.owner, First)
    self.assertEqual(refusal.fieldName, 'x')
    self.assertEqual(refusal.newOwner.__name__, 'Second')
    self.assertEqual(refusal.newName, 'y')

  def test_second_name_in_one_body(self) -> None:
    class Pair(BaseObject):
      left = AttriBox[int](1)
      right = left

    pair = Pair()
    pair.left = 5
    self.assertEqual(pair.right, 1)

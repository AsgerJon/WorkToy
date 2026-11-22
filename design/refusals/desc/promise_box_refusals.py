"""
RefusedBoxRefusals holds the refusals that belong with
'design.promises.desc.promise_box_refusals'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.desc import AttriBox
from worktoy.mcls import BaseObject
from worktoy.waitaminute.desc import MissingInstanceDict, SharedDescriptor


class RefusedBoxRefusals(TestCase):
  """
  Each of the following is refused, and the exception named is the one raised
  as of 1.2.3. As the class is created, an 'AttriBox' declared without
  parentheses raises 'TypeError', and one placed on a class whose instances
  have no '__dict__', as a class declaring '__slots__', raises
  'MissingInstanceDict'. One box placed on a second class raises
  'SharedDescriptor'. Before Python 3.12 the interpreter wraps a refusal
  raised while it places the attributes of a class in a 'RuntimeError'.
  Source: the docstrings of 'AttriBox' and 'BaseDescriptor'.
  """

  def test_no_parentheses(self) -> None:
    with self.assertRaises(Exception) as refused:
      class Point(BaseObject):
        x = AttriBox[float]
    self.assertIsInstance(refused.exception, (TypeError, RuntimeError))

  def test_no_instance_dict(self) -> None:
    with self.assertRaises(Exception) as refused:
      class Slotted:
        __slots__ = ('a',)
        x = AttriBox[int](0)
    self.assertIsInstance(
        refused.exception, (MissingInstanceDict, RuntimeError),
    )

  def test_second_class(self) -> None:
    box = AttriBox[int](0)

    class First(BaseObject):
      x = box

    with self.assertRaises(Exception) as refused:
      class Second(BaseObject):
        y = box
    self.assertIsInstance(
        refused.exception, (SharedDescriptor, RuntimeError),
    )

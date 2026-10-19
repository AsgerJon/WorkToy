"""
TestAttriBoxCopy tests that copying an 'AttriBox' gives the box itself,
shallow and deep, so a copy of an object the box created still names the
box declared on the class.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from copy import copy, deepcopy

from worktoy.desc import AttriBox
from worktoy.mcls import BaseObject

from . import DescTest


class Part:
  """Part is the field type the box builds."""


class Holder(BaseObject):
  """Holder declares one box."""

  part = AttriBox[Part]()


class TestAttriBoxCopy(DescTest):
  """
  TestAttriBoxCopy tests that 'copy.copy' and 'copy.deepcopy' of a box
  return the box, directly and when reached through the tags of an object
  the box created.
  """

  def test_copy_is_the_box(self) -> None:
    """A shallow copy of a box is the box."""
    box = Holder.__dict__['part']
    self.assertIs(copy(box), box)

  def test_deepcopy_is_the_box(self) -> None:
    """A deep copy of a box is the box."""
    box = Holder.__dict__['part']
    self.assertIs(deepcopy(box), box)

  def test_copied_object_keeps_its_box(self) -> None:
    """A deep copy of an object the box created still names the box on
    the class through its '__field_box__' tag."""
    holder = Holder()
    part = holder.part
    self.assertIs(part.__field_box__, Holder.__dict__['part'])
    self.assertIs(deepcopy(part).__field_box__, Holder.__dict__['part'])

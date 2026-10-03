"""
TestAttriBoxNoneDefault subclasses 'DescTest' and pins that a lone
default already of the field type is copied even when it is 'None', as
in 'AttriBox[object](None)'. '_resolve' used 'None' to mean that nothing
was built yet, so a copied 'None' went on to 'object(None)' and was
refused with a message saying 'None' is not an 'object'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import AttriBox
from worktoy.mcls import BaseObject

from . import DescTest


class Holder(BaseObject):
  """Holder declares boxes whose default is 'None'."""

  anything = AttriBox[object](None)
  nothing = AttriBox[type(None)](None)


class TestAttriBoxNoneDefault(DescTest):
  """
  TestAttriBoxNoneDefault provides tests for a 'None' default.
  """

  def test_object_field(self) -> None:
    """An 'AttriBox[object]' defaults to 'None'."""
    self.assertIsNone(Holder().anything)

  def test_none_type_field(self) -> None:
    """An 'AttriBox' of the type of 'None' defaults to 'None'."""
    self.assertIsNone(Holder().nothing)

  def test_assignment(self) -> None:
    """An 'AttriBox[object]' takes 'None' and other values."""
    holder = Holder()
    holder.anything = 7
    self.assertEqual(holder.anything, 7)
    holder.anything = None
    self.assertIsNone(holder.anything)

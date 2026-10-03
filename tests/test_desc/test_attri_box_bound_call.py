"""
TestAttriBoxBoundCall subclasses 'DescTest' and pins that a box placed on a
class refuses to be called again. Reading a box through its class gives the
box, and calling it, as in 'Holder.n(99)', captured a new default for
every instance that had not yet read the field.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import AttriBox
from worktoy.mcls import BaseObject

from . import DescTest


class Holder(BaseObject):
  """Holder declares an 'int' box."""
  n = AttriBox[int](0)


class TestAttriBoxBoundCall(DescTest):
  """
  TestAttriBoxBoundCall provides tests for calling a box after its class
  exists.
  """

  def test_call_refused(self) -> None:
    """Calling the box through its class raises 'TypeError'."""
    with self.assertRaises(TypeError):
      Holder.n(99)

  def test_default_kept(self) -> None:
    """The refused call leaves the default as declared."""
    try:
      Holder.n(99)
    except TypeError:
      pass
    self.assertEqual(Holder().n, 0)

  def test_call_before_class(self) -> None:
    """A box called again before its class exists keeps the last call."""
    box = AttriBox[int](1)
    box(2)

    class Later(BaseObject):
      """Later declares the box called twice."""
      n = box

    self.assertEqual(Later().n, 2)

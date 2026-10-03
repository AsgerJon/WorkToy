"""
TestAttriBoxNoRoot subclasses 'DescTest' and pins that no keyword lets
an 'AttriBox' store a value of the wrong type. '__instance_set__' honoured
an undocumented '_root' keyword, which nothing passed, and stored any
value given with it unchecked.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import AttriBox
from worktoy.mcls import BaseObject
from worktoy.waitaminute import TypeException

from . import DescTest


class Holder(BaseObject):
  """Holder declares an 'int' box."""

  n = AttriBox[int](0)


class TestAttriBoxNoRoot(DescTest):
  """
  TestAttriBoxNoRoot provides tests for the '_root' keyword of
  'AttriBox.__instance_set__'.
  """

  def test_root_checked(self) -> None:
    """A value given with '_root' is cast as any other."""
    holder = Holder()
    box = Holder.__dict__['n']
    with self.assertRaises(TypeException):
      box.__set__(holder, 'junk', _root=True)
    box.__set__(holder, 3.0, _root=True)
    self.assertEqual(holder.n, 3)
    self.assertIs(type(holder.n), int)

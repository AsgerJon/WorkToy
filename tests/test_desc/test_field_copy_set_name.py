"""
TestFieldCopySetName subclasses 'DescTest' and pins that 'Field(other)'
copies the 'setName' callbacks of 'other' along with every other group
of callbacks. The copy used to leave them out, so a copied field placed
on a class never called them.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import Field
from worktoy.mcls import BaseObject

from . import DescTest


class TestFieldCopySetName(DescTest):
  """
  TestFieldCopySetName provides tests for the 'setName' callbacks of a
  copied 'Field'.
  """

  def test_copy_keeps_set_name(self) -> None:
    """The copy carries the 'setName' callbacks of the original."""
    calls = []

    class Foo(BaseObject):
      x = Field()

      @classmethod
      @x.setName
      def _setNameX(cls, desc: Field) -> None:
        calls.append((cls.__name__, desc.getFieldName()))

    copied = Field(Foo.x)
    self.assertEqual(copied._getSetNameKeys(), ('_setNameX',))

    class Bar(Foo):
      y = copied

    self.assertEqual(calls, [('Foo', 'x'), ('Bar', 'y')])

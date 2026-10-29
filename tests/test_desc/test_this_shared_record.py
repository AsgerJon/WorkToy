"""
TestThisSharedRecord pins that 'THIS[GrandParent].x' is 'THIS[Parent].x'
for an 'x' that 'Parent' inherits from 'GrandParent': one reference with
one clone, so a class body may name either parent, or both, and the
subclass takes one 'x' carrying every decoration, set up and named once.
Two references used to make two records that were both placed, so the
'setName' callbacks ran twice.

The decorations use the subscripted decorator form, syntax only from
Python 3.9 on (PEP 614), which '_this_shared_helpers.py' holds and this
module imports on 3.9 and later alone.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import sys
from typing import TYPE_CHECKING
from unittest import skipIf

from worktoy.core.sentinels import THIS
from worktoy.desc import AttriBox
from worktoy.mcls import BaseObject

from . import DescTest

if sys.version_info >= (3, 9):
  from ._this_shared_helpers import bothParents

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class TestThisSharedRecord(DescTest):
  """
  TestThisSharedRecord provides tests for 'THIS' naming a parent and a
  base of it in one class body.
  """

  def setUp(self) -> None:
    """Fresh classes for each test, since 'THIS' installs its hook on the
    classes it records on."""
    named = []

    class GrandParent(BaseObject):
      x = AttriBox[int](0)

      @classmethod
      @x.setName
      def _named(cls, desc: Any) -> None:
        named.append(cls.__name__)

    class Parent(GrandParent):
      y = AttriBox[int](0)

    del named[:]
    self.named = named
    self.GrandParent, self.Parent = GrandParent, Parent

  def test_same_reference(self) -> None:
    """'THIS[GrandParent].x' is 'THIS[Parent].x', in either order, and
    the subclass names its 'x' once."""
    GrandParent, Parent = self.GrandParent, self.Parent

    class First(Parent):
      same = THIS[GrandParent].x is THIS[Parent].x

    class Second(Parent):
      same = THIS[Parent].x is THIS[GrandParent].x

    self.assertTrue(First.same)
    self.assertTrue(Second.same)
    self.assertEqual(self.named, ['First', 'Second'])

  @skipIf(sys.version_info < (3, 9), 'decorator subscripts need 3.9')
  def test_both_parents_decorate_one_clone(self) -> None:
    """Decorations through either parent land on the one 'x' the subclass
    takes, named once; a descriptor of each parent is placed once."""
    seen = []
    Child = bothParents(self.GrandParent, self.Parent, seen)
    self.assertEqual(self.named, ['Child'])
    child = Child()
    child.x = 1
    child.y = 2
    self.assertEqual(seen, ['first', 'second', 'y'])

  @skipIf(sys.version_info < (3, 9), 'decorator subscripts need 3.9')
  def test_parents_untouched(self) -> None:
    """The parents keep their own descriptors and hold no record once the
    subclass exists."""
    GrandParent, Parent, seen = self.GrandParent, self.Parent, []
    Child = bothParents(GrandParent, Parent, seen)
    self.assertIsNot(Child.__dict__['x'], GrandParent.__dict__['x'])
    self.assertNotIn('__new_descriptors__', GrandParent.__dict__)
    self.assertNotIn('__new_descriptors__', Parent.__dict__)
    GrandParent().x = 5
    Parent().y = 6
    self.assertEqual(seen, [])

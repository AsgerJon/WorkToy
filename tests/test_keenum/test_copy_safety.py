"""
TestCopySafety pins that 'KeeNum' and 'KeeFlags' members survive 'copy'
and 'deepcopy' as themselves. A member is a singleton whose equality is
identity (for 'KeeNum') or owner-and-index (for 'KeeFlags'), so a copy
that produced a fresh instance would compare unequal to every canonical
member and vanish from any member-keyed mapping. The members therefore
return themselves from '__copy__' and '__deepcopy__', the same defence
the standard library 'enum' applies to its members.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from copy import copy, deepcopy

from worktoy.desc import AttriBox, FixBox
from worktoy.keenum import KeeNum, Kee, KeeFlags, KeeFlag
from worktoy.mcls import BaseObject
from . import KeeTest


class Color(KeeNum):
  """Color is a small value enumeration used by the copy probes."""

  RED = Kee[int](1)
  GREEN = Kee[int](2)


class Perm(KeeFlags):
  """Perm is a small bitmask-flag enumeration used by the copy probes."""

  READ = KeeFlag()
  WRITE = KeeFlag()


class TestCopySafety(KeeTest):
  """
  TestCopySafety provides tests for the copy and deep-copy identity of
  'KeeNum' and 'KeeFlags' members.
  """

  def test_keenum_copy_is_member(self) -> None:
    """A shallow copy of a 'KeeNum' member is the member itself."""
    self.assertIs(copy(Color.RED), Color.RED)

  def test_keenum_deepcopy_is_member(self) -> None:
    """A deep copy of a 'KeeNum' member is the member itself."""
    self.assertIs(deepcopy(Color.GREEN), Color.GREEN)

  def test_keenum_deepcopy_equal_and_dict_key(self) -> None:
    """A deep-copied 'KeeNum' member still compares equal to the
    canonical member and resolves the same mapping entry."""
    members = {Color.RED: 'red', Color.GREEN: 'green'}
    cloned = deepcopy(Color.RED)
    self.assertEqual(cloned, Color.RED)
    self.assertEqual(members[cloned], 'red')

  def test_keenum_deepcopy_inside_container(self) -> None:
    """A 'KeeNum' member carried inside a deep-copied container survives
    as the canonical member."""
    config = {'color': Color.RED}
    self.assertEqual(deepcopy(config)['color'], Color.RED)
    self.assertIs(deepcopy(config)['color'], Color.RED)

  def test_keeflags_copy_is_member(self) -> None:
    """A shallow copy of a 'KeeFlags' member is the member itself."""
    self.assertIs(copy(Perm.READ), Perm.READ)

  def test_keeflags_deepcopy_is_member(self) -> None:
    """A deep copy of a 'KeeFlags' member is the member itself, keeping
    'is' checks such as 'member is cls.NULL' intact."""
    self.assertIs(deepcopy(Perm.NULL), Perm.NULL)
    self.assertIs(deepcopy(Perm.READ), Perm.READ)

  def test_attribox_keenum_default_is_member(self) -> None:
    """An 'AttriBox' default of a 'KeeNum' member resolves to the
    canonical member rather than a deep-copied clone, so the stored
    value compares equal and identical to the declared member."""

    class Widget(BaseObject):
      color = AttriBox[Color](Color.RED)

    widget = Widget()
    self.assertIs(widget.color, Color.RED)
    self.assertEqual(widget.color, Color.RED)

  def test_fixbox_keenum_default_is_member(self) -> None:
    """A 'FixBox' default of a 'KeeNum' member resolves to the canonical
    member as well."""

    class Widget(BaseObject):
      color = FixBox[Color](Color.GREEN)

    widget = Widget()
    self.assertIs(widget.color, Color.GREEN)
    self.assertEqual(widget.color, Color.GREEN)

  def test_attribox_keeflags_default_is_member(self) -> None:
    """An 'AttriBox' default of a 'KeeFlags' member resolves to the
    canonical member, so identity checks against it hold."""

    class Widget(BaseObject):
      mode = AttriBox[Perm](Perm.READ)

    widget = Widget()
    self.assertIs(widget.mode, Perm.READ)
    self.assertEqual(widget.mode, Perm.READ)

"""
TestBoxOwnerSetattr subclasses 'DescTest' from the 'tests.test_desc'
package and pins that a box keeps its storage to itself when the owning
class defines a '__setattr__' refusing private names. The boxes used to
write their storage with 'setattr', which runs the owner's '__setattr__',
so such an owner refused the lazily built default on the first read, and
every assignment and deletion after it. The boxes now write their storage
with 'object.__setattr__', as they already read it with
'object.__getattribute__'. An assignment to the field itself still passes
the owner's '__setattr__' first, which admits the public field name here.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.desc import AttriBox, FixBox
from worktoy.keenum import KeeNum, Kee, KeeBox
from worktoy.mcls import BaseObject
from worktoy.waitaminute import MissingVariable
from worktoy.waitaminute.desc import WriteOnceError

from . import DescTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class Color(KeeNum):
  """Color is the enumeration behind the 'KeeBox' field below."""

  RED = Kee[str]('red')
  BLUE = Kee[str]('blue')


class Guarded(BaseObject):
  """Guarded is an owner whose '__setattr__' refuses every private name.
  Its own '__init__' keeps 'Object.__init__' out of these tests."""

  bar = AttriBox[int](7)
  fixed = FixBox[int](7)
  color = KeeBox[Color]('RED')

  def __init__(self, ) -> None:
    pass

  def __setattr__(self, key: str, value: Any) -> None:
    if key.startswith('_'):
      raise AttributeError('private name: %s' % key)
    object.__setattr__(self, key, value)


class TestBoxOwnerSetattr(DescTest):
  """
  TestBoxOwnerSetattr provides tests for boxes on an owner whose
  '__setattr__' refuses every private name.
  """

  def test_owner_refuses_private_names(self) -> None:
    """The owner does refuse a private name, which is what used to stop
    the boxes from storing anything."""
    with self.assertRaises(AttributeError):
      Guarded()._private = 1

  def test_attri_box_builds_default(self) -> None:
    """'AttriBox' builds and stores its default on the first read."""
    self.assertEqual(Guarded().bar, 7)

  def test_attri_box_assignment(self) -> None:
    """An assignment through the public field name is stored."""
    owner = Guarded()
    owner.bar = 9
    self.assertEqual(owner.bar, 9)

  def test_attri_box_deletion(self) -> None:
    """A deletion is stored, and the next read raises
    'MissingVariable'."""
    owner = Guarded()
    del owner.bar
    with self.assertRaises(MissingVariable):
      _ = owner.bar

  def test_fix_box_builds_default(self) -> None:
    """'FixBox' builds its default, and the read consumes its one write,
    so a later assignment raises 'WriteOnceError'."""
    owner = Guarded()
    self.assertEqual(owner.fixed, 7)
    with self.assertRaises(WriteOnceError):
      owner.fixed = 9

  def test_fix_box_assignment(self) -> None:
    """A 'FixBox' assigned before its first read holds the value."""
    owner = Guarded()
    owner.fixed = 9
    self.assertEqual(owner.fixed, 9)

  def test_kee_box_builds_default(self) -> None:
    """'KeeBox' resolves and stores its default member."""
    self.assertIs(Guarded().color, Color.RED)

  def test_kee_box_assignment(self) -> None:
    """A 'KeeBox' assignment resolves and stores the member."""
    owner = Guarded()
    owner.color = 'blue'
    self.assertIs(owner.color, Color.BLUE)

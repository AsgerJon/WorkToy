"""
TestKeeBoxSlotsOwner subclasses 'KeeTest' and pins that a 'KeeBox' on an
owner whose instances have no '__dict__', a class declaring '__slots__'
without one, refuses every access with 'MissingInstanceDict' naming the
owner and the field, as 'AttriBox' does. 'KeeBox' used to store with
'object.__setattr__' directly, so the bare 'AttributeError' of the failed
store escaped, which the attribute protocol reads as the attribute being
absent.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import KeeNum, Kee, KeeFlags, KeeFlag, KeeBox
from worktoy.waitaminute.desc import MissingInstanceDict
from . import KeeTest


class Color(KeeNum):
  """Color is a small value enumeration boxed by the owners below."""

  RED = Kee[int](1)
  GREEN = Kee[int](2)


class Perm(KeeFlags):
  """Perm is a small flags enumeration boxed by the owners below."""

  READ = KeeFlag()
  WRITE = KeeFlag()


class Slotted:
  """Slotted declares slots and no instance dict."""

  __slots__ = ('a',)

  color = KeeBox[Color]('RED')
  perm = KeeBox[Perm]('READ')


class WithDict:
  """WithDict declares slots including an instance dict."""

  __slots__ = ('a', '__dict__')

  color = KeeBox[Color]('RED')
  perm = KeeBox[Perm]('READ')


class TestKeeBoxSlotsOwner(KeeTest):
  """
  TestKeeBoxSlotsOwner provides tests for a 'KeeBox' on a slots-only
  owner.
  """

  def test_read_refused(self) -> None:
    """A read raises, naming the owner and the field."""
    with self.assertRaises(MissingInstanceDict) as context:
      _ = Slotted().color
    e = context.exception
    self.assertEqual(e.ownerName, 'Slotted')
    self.assertEqual(e.fieldName, 'color')
    self.assertIn("'Slotted.color'", str(e))
    self.assertIsInstance(e, TypeError)
    with self.assertRaises(MissingInstanceDict) as context:
      _ = Slotted().perm
    self.assertEqual(context.exception.fieldName, 'perm')

  def test_write_refused(self) -> None:
    """A write raises the same, whether the value is a member already
    or an identifier the box resolves first."""
    slotted = Slotted()
    with self.assertRaises(MissingInstanceDict):
      slotted.color = Color.GREEN
    with self.assertRaises(MissingInstanceDict):
      slotted.color = 'GREEN'
    with self.assertRaises(MissingInstanceDict):
      slotted.perm = Perm.WRITE
    with self.assertRaises(MissingInstanceDict):
      slotted.perm = 'write'

  def test_delete_refused(self) -> None:
    """A delete raises the same."""
    slotted = Slotted()
    with self.assertRaises(MissingInstanceDict):
      del slotted.color

  def test_not_mistaken_for_absence(self) -> None:
    """'hasattr' does not answer 'False'; the refusal propagates."""
    with self.assertRaises(MissingInstanceDict):
      hasattr(Slotted(), 'color')

  def test_dict_slot_works(self) -> None:
    """An owner whose slots include '__dict__' holds the field as any
    other."""
    owner = WithDict()
    self.assertIs(owner.color, Color.RED)
    owner.color = 'GREEN'
    self.assertIs(owner.color, Color.GREEN)
    self.assertIs(owner.perm, Perm.READ)
    owner.perm = 'read', 'write'
    self.assertIs(owner.perm, Perm.READ_WRITE)

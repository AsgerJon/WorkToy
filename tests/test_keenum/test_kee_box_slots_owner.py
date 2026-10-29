"""
TestKeeBoxSlotsOwner subclasses 'KeeTest' and pins that a 'KeeBox'
refuses an owner whose instances have no '__dict__', a class declaring
'__slots__' without one, with 'MissingInstanceDict' naming the owner and
the field as the class is created, as 'AttriBox' does. A box installed on
such a class with 'setattr' afterwards is refused the same way at every
access. 'KeeBox' used to store with 'object.__setattr__' directly, so the
bare 'AttributeError' of the failed store escaped, which the attribute
protocol reads as the attribute being absent.
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


class WithDict:
  """WithDict declares slots including an instance dict."""

  __slots__ = ('a', '__dict__')

  color = KeeBox[Color]('RED')
  perm = KeeBox[Perm]('READ')


def _slotted() -> type:
  """A slots-only class holding the boxes of 'WithDict', set on it after
  it exists, so it never received '__set_name__'."""

  class Slotted:
    __slots__ = ('a',)

  setattr(Slotted, 'color', WithDict.__dict__['color'])
  setattr(Slotted, 'perm', WithDict.__dict__['perm'])
  return Slotted


class TestKeeBoxSlotsOwner(KeeTest):
  """
  TestKeeBoxSlotsOwner provides tests for a 'KeeBox' on a slots-only
  owner.
  """

  def test_class_refused(self) -> None:
    """The class statement raises, naming the owner and the field."""
    with self.assertRaises((MissingInstanceDict, RuntimeError)) as context:
      class Slotted:
        __slots__ = ('a',)
        color = KeeBox[Color]('RED')
    e = context.exception
    if not isinstance(e, MissingInstanceDict):  # pragma: no cover (< 3.12)
      e = e.__cause__
    self.assertIsInstance(e, MissingInstanceDict)
    self.assertEqual(e.ownerName, 'Slotted')
    self.assertEqual(e.fieldName, 'color')
    self.assertIn("'Slotted.color'", str(e))

  def test_installed_later_refused(self) -> None:
    """A box set on a slots-only class after it exists refuses a read, a
    write of a member or of an identifier, and a deletion, and 'hasattr'
    does not answer 'False'."""
    slotted = _slotted()()
    with self.assertRaises(MissingInstanceDict):
      _ = slotted.color
    with self.assertRaises(MissingInstanceDict):
      _ = slotted.perm
    with self.assertRaises(MissingInstanceDict):
      slotted.color = Color.GREEN
    with self.assertRaises(MissingInstanceDict):
      slotted.color = 'GREEN'
    with self.assertRaises(MissingInstanceDict):
      slotted.perm = 'write'
    with self.assertRaises(MissingInstanceDict):
      del slotted.color
    with self.assertRaises(MissingInstanceDict):
      hasattr(slotted, 'color')

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

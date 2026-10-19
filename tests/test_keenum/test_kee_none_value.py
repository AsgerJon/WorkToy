"""
TestKeeNoneValue subclasses 'KeeTest' and pins that a member whose value
is 'None' builds and behaves as any other member. 'Kee' used to read
'None' as the marker of a value not yet built, so 'Kee[object](None)'
rebuilt the value on every read and the class statement failed with a
bare 'RecursionError'. The value now carries a built flag beside it.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import KeeNum, Kee
from . import KeeTest


class Maybe(KeeNum):
  """Maybe enumerates an absent value beside present ones."""

  NOTHING = Kee[object](None)
  SOMETHING = Kee[object](1)
  ANYTHING = Kee[object]('any')


class TestKeeNoneValue(KeeTest):
  """
  TestKeeNoneValue provides tests for a member whose value is 'None'.
  """

  def test_value_is_none(self) -> None:
    """The member value reads as 'None', on every read."""
    self.assertIsNone(Maybe.NOTHING.value)
    self.assertIsNone(Maybe.NOTHING.value)
    self.assertEqual(Maybe.SOMETHING.value, 1)
    self.assertEqual(Maybe.ANYTHING.value, 'any')

  def test_kee_alone(self) -> None:
    """A 'Kee' holding 'None' builds its value once and keeps it."""
    kee = Kee[object](None)
    self.assertIsNone(kee.getValue())
    self.assertIsNone(kee.getValue())

  def test_member_behaves(self) -> None:
    """Name, index, hash, equality and text are those of a member."""
    member = Maybe.NOTHING
    self.assertEqual(member.name, 'NOTHING')
    self.assertEqual(member.index, 0)
    self.assertEqual(hash(member), hash(Maybe.NOTHING))
    self.assertEqual(member, Maybe.NOTHING)
    self.assertNotEqual(member, Maybe.SOMETHING)
    self.assertEqual(str(member), 'Maybe.NOTHING')
    self.assertEqual(len(Maybe), 3)
    self.assertEqual([m.name for m in Maybe], ['NOTHING', 'SOMETHING',
                                               'ANYTHING'])

  def test_lookup_by_none(self) -> None:
    """The member resolves from its value, 'None', as any value does."""
    self.assertIs(Maybe(None), Maybe.NOTHING)
    self.assertIs(Maybe[None], Maybe.NOTHING)
    self.assertIs(Maybe.fromValue(None), Maybe.NOTHING)
    self.assertIs(Maybe(1), Maybe.SOMETHING)
    self.assertIn(Maybe.NOTHING, Maybe)

  def test_subclass_keeps_none(self) -> None:
    """A derived enumeration inherits the member with its 'None' value."""

    class More(Maybe):
      """More adds a member to 'Maybe'."""

      EVERYTHING = Kee[object](2)

    self.assertIsNone(More.NOTHING.value)
    self.assertIs(More(None), More.NOTHING)
    self.assertEqual(len(More), 4)

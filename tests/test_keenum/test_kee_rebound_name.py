"""
TestKeeReboundName subclasses 'KeeTest' and pins that a 'KeeNum' class
body may not bind a member name twice, once to a 'Kee' and once to a
plain value, in either order. The member used to win silently: the
namespace routed the 'Kee' to the enumeration and stored the plain value
as an attribute, which the member then replaced. The second binding now
raises 'KeeMemberNameError', as a 'KeeFlags' body binding a member name
does.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import KeeNum, Kee
from worktoy.waitaminute.keenum import KeeMemberNameError, KeeDuplicate
from . import KeeTest


class Base(KeeNum):
  """Base declares a member a subclass below tries to rebind."""

  RED = Kee[int](1)


class TestKeeReboundName(KeeTest):
  """
  TestKeeReboundName provides tests for a member name bound twice in a
  'KeeNum' class body.
  """

  def test_plain_after_member_refused(self) -> None:
    """A plain value bound to a member name raises, naming both."""
    with self.assertRaises(KeeMemberNameError) as context:
      class Color(KeeNum):  # noqa: F841
        RED = Kee[int](1)
        RED = 'plain'  # noqa: F811
    e = context.exception
    self.assertEqual(e.clsName, 'Color')
    self.assertEqual(e.memberName, 'RED')
    self.assertIn("'Color'", str(e))
    self.assertIn("'RED'", str(e))
    self.assertIsInstance(e, SyntaxError)
    self.assertEqual(e.msg, str(e))

  def test_member_after_plain_refused(self) -> None:
    """A member bound to a name a plain value holds raises the same."""
    with self.assertRaises(KeeMemberNameError) as context:
      class Color(KeeNum):  # noqa: F841
        RED = 'plain'
        RED = Kee[int](1)  # noqa: F811
    e = context.exception
    self.assertEqual(e.clsName, 'Color')
    self.assertEqual(e.memberName, 'RED')

  def test_inherited_member_refused(self) -> None:
    """A plain value bound to the name of an inherited member raises."""
    with self.assertRaises(KeeMemberNameError) as context:
      class More(Base):  # noqa: F841
        RED = 'plain'
    self.assertEqual(context.exception.memberName, 'RED')

  def test_member_twice_still_duplicate(self) -> None:
    """Two members of one name still raise 'KeeDuplicate', as before."""
    with self.assertRaises(KeeDuplicate):
      class Color(KeeNum):  # noqa: F841
        RED = Kee[int](1)
        RED = Kee[int](2)  # noqa: F811

  def test_other_names_unaffected(self) -> None:
    """A plain attribute of another name, rebound or not, is kept."""

    class Color(KeeNum):
      """Color mixes members and plain attributes."""

      RED = Kee[int](1)
      label = 'first'
      label = 'second'  # noqa: F811
      GREEN = Kee[int](2)

    self.assertEqual(Color.label, 'second')
    self.assertEqual([m.name for m in Color], ['RED', 'GREEN'])
    self.assertIs(Color.RED, Color['RED'])

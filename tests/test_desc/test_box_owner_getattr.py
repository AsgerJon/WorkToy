"""
TestBoxOwnerGetattr subclasses 'DescTest' from the 'tests.test_desc'
package and pins that a box builds its default even when the owning class
defines a '__getattr__' answering every name. 'AttriBox' and 'KeeBox'
used to read their storage with 'getattr', and took an 'AttributeError'
to mean the default was not built yet. Such an owner never raises one,
so the default was never built and the read returned whatever
'__getattr__' gave. The boxes now read their storage with
'object.__getattribute__', which a '__getattr__' cannot answer, as
'FixBox' already did for its write-once check.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.desc import AttriBox, FixBox
from worktoy.keenum import KeeNum, Kee, KeeBox
from worktoy.waitaminute.desc import WriteOnceError

from . import DescTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class Color(KeeNum):
  """Color is the enumeration behind the 'KeeBox' field below."""

  RED = Kee[str]('red')
  BLUE = Kee[str]('blue')


class Lenient:
  """Lenient is an owner whose '__getattr__' answers every name."""

  bar = AttriBox[int](7)
  fixed = FixBox[int](7)
  color = KeeBox[Color]('RED')

  def __getattr__(self, key: str) -> Any:
    return 'junk'


class TestBoxOwnerGetattr(DescTest):
  """
  TestBoxOwnerGetattr provides tests for boxes on an owner whose
  '__getattr__' answers every name.
  """

  def test_owner_answers_every_name(self) -> None:
    """The owner does answer names it does not have, which is what used
    to hide the missing storage from the boxes."""
    self.assertEqual(Lenient().nothingHere, 'junk')

  def test_attri_box_builds_default(self) -> None:
    """'AttriBox' builds its default and then holds assigned values."""
    owner = Lenient()
    self.assertEqual(owner.bar, 7)
    owner.bar = 9
    self.assertEqual(owner.bar, 9)

  def test_fix_box_builds_default(self) -> None:
    """'FixBox' builds its default, and the read consumes its one write,
    so a later assignment raises 'WriteOnceError'."""
    owner = Lenient()
    self.assertEqual(owner.fixed, 7)
    with self.assertRaises(WriteOnceError):
      owner.fixed = 9

  def test_kee_box_builds_default(self) -> None:
    """'KeeBox' resolves its default to the member rather than returning
    what '__getattr__' gave."""
    owner = Lenient()
    self.assertIs(owner.color, Color.RED)
    owner.color = 'blue'
    self.assertIs(owner.color, Color.BLUE)

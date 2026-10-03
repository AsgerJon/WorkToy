"""
TestKeeBoxKeywords subclasses 'KeeTest' and pins that the keyword
arguments captured for the default of a 'KeeBox' build the default
alone. An assigned value is resolved from that value only; it used to
be resolved with the keywords of the default as well, so assigning
'10' to a box declared as 'KeeBox[Num]('10', base=16)' read it in base
16 and stored the wrong member.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import KeeNum, Kee, KeeBox
from worktoy.mcls import BaseObject

from . import KeeTest


class Num(KeeNum):
  """Num holds members whose values differ between base 10 and 16."""

  TEN = Kee[int](10)
  SIXTEEN = Kee[int](16)


class Holder(BaseObject):
  """Holder declares a box whose default is read in base 16."""

  n = KeeBox[Num]('10', base=16)


class TestKeeBoxKeywords(KeeTest):
  """
  TestKeeBoxKeywords provides tests for the keyword arguments of a
  'KeeBox' default.
  """

  def test_default_uses_keywords(self) -> None:
    """The default is built with the captured keywords."""
    self.assertIs(Holder().n, Num.SIXTEEN)

  def test_assignment_ignores_default_keywords(self) -> None:
    """An assigned value is resolved without the keywords of the
    default."""
    holder = Holder()
    holder.n = '10'
    self.assertIs(holder.n, Num.TEN)

  def test_other_instance_keeps_default(self) -> None:
    """An assignment on one instance leaves the default of another as it
    was."""
    first, second = Holder(), Holder()
    first.n = '10'
    self.assertIs(second.n, Num.SIXTEEN)

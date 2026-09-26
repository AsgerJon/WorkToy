"""
TestKeeBoxMemberDefault subclasses 'KeeTest' from the 'tests.test_keenum'
package and pins that a 'KeeBox' default given as a member of the field
enumeration resolves to exactly that member. The assignment path checks
for a member before anything else, and the default path must agree with
it. Resolving the member through its value type instead turns it into
something else first: an 'int' enumeration reads the member as its
index and matches that against the values, landing on another member,
while other value types fail to resolve it at all.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import KeeNum, Kee, KeeFlags, KeeFlag, KeeBox

from . import KeeTest
from .examples import ColorNum, RGB


class Slot(KeeNum):
  """Slot has 'int' values that differ from the member indices, so a
  member read as its index matches the value of another member."""

  LEFT = Kee[int](2)
  CENTER = Kee[int](0)
  RIGHT = Kee[int](1)


class Greeting(KeeNum):
  """Greeting has 'str' values that spell the names of the other members,
  so a member resolved through its value lands on the other member."""

  HELLO = Kee[str]('world')
  WORLD = Kee[str]('hello')


class Perm(KeeFlags):
  """Perm declares three single-bit flags."""

  READ = KeeFlag()
  WRITE = KeeFlag()
  EXECUTE = KeeFlag()


class TestKeeBoxMemberDefault(KeeTest):
  """
  TestKeeBoxMemberDefault provides tests for 'KeeBox' defaults given as
  members of the field enumeration.
  """

  def test_int_valued_member(self) -> None:
    """
    Every member of 'Slot' given as the default comes back as itself,
    although its index equals the value of another member.
    """
    for member in Slot:
      with self.subTest(member=member.name):
        class Holder:
          slot = KeeBox[Slot](member)

        self.assertIs(Holder().slot, member)

  def test_str_valued_member(self) -> None:
    """
    Every member of 'Greeting' given as the default comes back as itself.
    """
    for member in Greeting:
      with self.subTest(member=member.name):
        class Holder:
          greeting = KeeBox[Greeting](member)

        self.assertIs(Holder().greeting, member)

  def test_flag_member(self) -> None:
    """
    A single flag member, or 'NULL', given as the default of a box over
    a 'KeeFlags' class comes back as itself.
    """
    for member in (Perm.NULL, Perm.READ, Perm.WRITE, Perm.EXECUTE):
      with self.subTest(member=member.name):
        class Holder:
          mode = KeeBox[Perm](member)

        self.assertIs(Holder().mode, member)

  def test_flag_members_as_arguments(self) -> None:
    """
    Several flag members given as arguments combine into the member
    holding all of them, just as several flag names do, and names and
    members may be mixed.
    """

    class Holder:
      both = KeeBox[Perm](Perm.READ, Perm.WRITE)
      mixed = KeeBox[Perm]('READ', Perm.EXECUTE)

    holder = Holder()
    self.assertIs(holder.both, Perm.READ | Perm.WRITE)
    self.assertIs(holder.mixed, Perm.READ | Perm.EXECUTE)

  def test_assignment_agrees(self) -> None:
    """
    Assigning a member stores that member, which is the behaviour the
    default path has to match.
    """

    class Holder:
      slot = KeeBox[Slot](Slot.CENTER)

    holder = Holder()
    for member in Slot:
      holder.slot = member
      self.assertIs(holder.slot, member)

  def test_value_is_not_compared_as_member(self) -> None:
    """
    Deciding whether an argument is a member must not compare a value
    with the members through the value's own '__eq__'. 'RGB' compares
    colour channels and fails on anything else, yet an 'RGB' value given
    as the default or assigned still resolves to the member holding it.
    """

    class Holder:
      color = KeeBox[ColorNum](RGB(255, 0, 0))

    holder = Holder()
    self.assertIs(holder.color, ColorNum.RED)
    holder.color = RGB(0, 255, 0)
    self.assertIs(holder.color, ColorNum.GREEN)

"""
TestKeeBoxCombinedFlags subclasses 'KeeTest' from the 'tests.test_keenum'
package and pins that a 'KeeBox' over a 'KeeFlags' class resolves every
identifier the flags class itself accepts by subscript, combined members
included. Building the result from the plain names of the resolved
members fails for a combined member, whose name 'READ_WRITE' joins the
names of its flags rather than listing them, so no member matches. The
flag names in another order, such as 'write_read', must work as well,
since subscripting the flags class ignores both case and order.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import KeeFlags, KeeFlag, KeeBox

from . import KeeTest


class Perm(KeeFlags):
  """Perm declares three single-bit flags."""

  READ = KeeFlag()
  WRITE = KeeFlag()
  EXECUTE = KeeFlag()


#  Every identifier below names 'Perm.READ_WRITE' by subscript: the
#  canonical name, the same in lower case, the flag names in another
#  order, the index, and the member itself.
IDENTIFIERS = ('READ_WRITE', 'read_write', 'write_read', 3, Perm.READ_WRITE)


class TestKeeBoxCombinedFlags(KeeTest):
  """
  TestKeeBoxCombinedFlags provides tests for 'KeeBox' over 'KeeFlags'
  classes resolving combined members.
  """

  def test_identifiers_name_the_member(self) -> None:
    """
    The subscript of 'Perm' resolves every identifier in 'IDENTIFIERS' to
    'Perm.READ_WRITE', which the tests below hold 'KeeBox' to.
    """
    for identifier in IDENTIFIERS:
      with self.subTest(identifier=identifier):
        self.assertIs(Perm[identifier], Perm.READ_WRITE)

  def test_default_matches_subscript(self) -> None:
    """
    A default given as any of the identifiers resolves to the member the
    subscript gives.
    """
    for identifier in IDENTIFIERS:
      with self.subTest(identifier=identifier):
        class Holder:
          mode = KeeBox[Perm](identifier)

        self.assertIs(Holder().mode, Perm[identifier])

  def test_assignment_matches_subscript(self) -> None:
    """
    Assigning any of the identifiers stores the member the subscript
    gives.
    """
    for identifier in IDENTIFIERS:
      with self.subTest(identifier=identifier):
        class Holder:
          mode = KeeBox[Perm]('EXECUTE')

        holder = Holder()
        holder.mode = identifier
        self.assertIs(holder.mode, Perm[identifier])

  def test_combined_member_with_more_flags(self) -> None:
    """
    A combined member given together with a further flag, as arguments
    or as an assigned tuple, resolves to the member holding all of them.
    """

    class Holder:
      mode = KeeBox[Perm](Perm.READ_WRITE, 'EXECUTE')

    everything = Perm.READ | Perm.WRITE | Perm.EXECUTE
    holder = Holder()
    self.assertIs(holder.mode, everything)
    holder.mode = 'READ'
    self.assertIs(holder.mode, Perm.READ)
    holder.mode = ('READ_WRITE', 'EXECUTE')
    self.assertIs(holder.mode, everything)

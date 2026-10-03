"""
TestClassBodyDel subclasses 'MCLSTest' and pins what 'del' does in the
class body of a worktoy class. Deleting a name bound to an ordinary value
removes it, as in a plain class, so a later read in the class body finds
the module scope instead. The namespace used to remove the name from
itself only, while its shadow space kept answering reads with the
deleted value. Deleting a name a namespace hook claimed raises
'ClaimedName' as the class is created, since the hook has registered the
value already; it used to raise a 'NameError' saying the name was not
defined, which the interpreter makes of any exception a deletion raises.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.dispatch import overload
from worktoy.ezdata import EZData, EZField
from worktoy.keenum import KeeNum, Kee
from worktoy.mcls import BaseObject
from worktoy.waitaminute.meta import ClaimedName

from .. import MCLSTest

#  Module-level name the class bodies below shadow and then delete.
tmp = 'GLOBAL'


class TestClassBodyDel(MCLSTest):
  """
  TestClassBodyDel provides tests for 'del' in a worktoy class body.
  """

  def test_deleted_name_reads_global(self) -> None:
    """After 'del', the class body reads the name from the module
    scope."""

    class Foo(BaseObject):
      tmp = 'LOCAL'
      del tmp
      seen = tmp

    self.assertEqual(Foo.seen, 'GLOBAL')
    self.assertNotIn('tmp', Foo.__dict__)

  def test_never_bound_raises_name_error(self) -> None:
    """Deleting a name the class body never bound raises 'NameError', as
    in a plain class, and so does deleting a name a second time."""
    with self.assertRaises(NameError):
      class Foo(BaseObject):
        del tmp
    with self.assertRaises(NameError):
      class Bar(BaseObject):
        tmp = 'LOCAL'
        del tmp
        del tmp

  def test_rebound_after_delete(self) -> None:
    """A name deleted and bound again holds the new value."""

    class Foo(BaseObject):
      tmp = 'FIRST'
      del tmp
      tmp = 'SECOND'

    self.assertEqual(Foo.tmp, 'SECOND')

  def test_claimed_overload_refused(self) -> None:
    """Deleting an overloaded name raises 'ClaimedName'."""
    with self.assertRaises(ClaimedName) as context:
      class Foo(BaseObject):
        @overload(int)
        def foo(self, x: int) -> int:
          return x  # pragma: no cover

        del foo
    e = context.exception
    self.assertEqual(e.className, 'Foo')
    self.assertEqual(e.keyName, 'foo')
    self.assertIn("'foo'", str(e))
    self.assertEqual(str(e), repr(e))
    self.assertEqual(e.msg, str(e))

  def test_claimed_field_refused(self) -> None:
    """Deleting the name of an 'EZField' raises 'ClaimedName'."""
    with self.assertRaises(ClaimedName):
      class Foo(EZData):
        x = EZField[int](0)
        del x

  def test_claimed_member_refused(self) -> None:
    """Deleting the name of a 'Kee' member raises 'ClaimedName', also
    after an earlier plain binding of the same name."""
    with self.assertRaises(ClaimedName):
      class Foo(KeeNum):
        A = 'plain'
        A = Kee[int](1)
        del A

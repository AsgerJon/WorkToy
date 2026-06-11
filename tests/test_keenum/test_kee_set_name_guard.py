"""
TestKeeSetNameGuard tests that 'Kee' and 'KeeFlag' reject declaration in
the class body of any class not built by their respective metaclasses.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.keenum import Kee, KeeNum, KeeMeta, KeeFlag, KeeFlags
from worktoy.keenum import KeeFlagsMeta
from worktoy.mcls import BaseObject
from worktoy.waitaminute import TypeException

from . import KeeTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class TestKeeSetNameGuard(KeeTest):
  """
  TestKeeSetNameGuard tests the '__set_name__' guard on 'Kee' and
  'KeeFlag'. Inside a proper enumeration class body the space hooks
  claim these objects before the namespace stores them, so the
  interpreter-driven '__set_name__' never fires there. It fires exactly
  when one of them lands in a foreign class body, and the guard then
  raises 'TypeException' naming the metaclass the owner should have.
  """

  def _unwrap(self, exception: BaseException) -> Any:
    """
    On Python 3.7 through 3.11 the interpreter wraps an exception
    raised from '__set_name__' in a 'RuntimeError', with the original
    attached as both '__cause__' and '__context__'; from Python 3.12
    onward it propagates unchanged. This helper returns the underlying
    'TypeException' either way, reading it off '__cause__' when
    wrapped.
    """
    if isinstance(exception, TypeException):
      return exception
    return exception.__cause__  # pragma: no cover (Python < 3.12)

  def test_kee_in_plain_class(self) -> None:
    """
    A 'Kee' in a plain class body raises 'TypeException' naming
    'KeeMeta' as the expected owner metaclass.
    """
    with self.assertRaises((TypeException, RuntimeError)) as context:
      class Foo:
        BAR = Kee[int](69)
    e = self._unwrap(context.exception)
    self.assertIsInstance(e, TypeException)
    self.assertEqual(e.varName, 'owner')
    self.assertIn(KeeMeta, e.expectedTypes)

  def test_kee_in_base_object_class(self) -> None:
    """
    A 'Kee' in a 'BaseObject' class body raises the same way: the
    'BaseSpace' hooks do not claim 'Kee' objects either.
    """
    with self.assertRaises((TypeException, RuntimeError)) as context:
      class Foo(BaseObject):
        BAR = Kee[int](69)
    e = self._unwrap(context.exception)
    self.assertIsInstance(e, TypeException)
    self.assertEqual(e.varName, 'owner')
    self.assertIn(KeeMeta, e.expectedTypes)

  def test_kee_in_kee_flags_class(self) -> None:
    """
    A 'Kee' in a 'KeeFlags' class body raises as well: the flags space
    claims only 'KeeFlag' objects.
    """
    with self.assertRaises((TypeException, RuntimeError)) as context:
      class Foo(KeeFlags):
        A = KeeFlag()
        BAR = Kee[int](69)
    e = self._unwrap(context.exception)
    self.assertIsInstance(e, TypeException)
    self.assertEqual(e.varName, 'owner')
    self.assertIn(KeeMeta, e.expectedTypes)

  def test_kee_flag_in_plain_class(self) -> None:
    """
    A 'KeeFlag' in a plain class body raises 'TypeException' naming
    'KeeFlagsMeta' as the expected owner metaclass.
    """
    with self.assertRaises((TypeException, RuntimeError)) as context:
      class Foo:
        BAR = KeeFlag()
    e = self._unwrap(context.exception)
    self.assertIsInstance(e, TypeException)
    self.assertEqual(e.varName, 'owner')
    self.assertIn(KeeFlagsMeta, e.expectedTypes)

  def test_kee_flag_in_kee_num_class(self) -> None:
    """
    A 'KeeFlag' in a 'KeeNum' class body raises as well: the num space
    claims only 'Kee' objects.
    """
    with self.assertRaises((TypeException, RuntimeError)) as context:
      class Foo(KeeNum):
        A = Kee[int](1)
        BAR = KeeFlag()
    e = self._unwrap(context.exception)
    self.assertIsInstance(e, TypeException)
    self.assertEqual(e.varName, 'owner')
    self.assertIn(KeeFlagsMeta, e.expectedTypes)

  def test_kee_set_name_accepts_kee_meta_owner(self) -> None:
    """
    Called directly with an owner built by 'KeeMeta', the guard stands
    down and the ordinary 'AttriBox' registration runs.
    """

    class WeekDay(KeeNum):
      MONDAY = Kee[str]('Mandag')

    kee = Kee[int](69)
    kee.__set_name__(WeekDay, 'EXTRA')
    self.assertIs(kee.getFieldOwner(), WeekDay)
    self.assertEqual(kee.getFieldName(), 'EXTRA')

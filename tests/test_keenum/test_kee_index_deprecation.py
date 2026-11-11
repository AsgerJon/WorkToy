"""
TestKeeIndexDeprecation tests the deprecation notice of the 'index' of
a member of an enumeration and of a 'Kee' from 'worktoy.keenum'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import sys
import warnings

from worktoy.keenum import Kee, KeeNum, KeeFlags
from worktoy.waitaminute import DeprecatedPromise
from . import KeenumTest, WeekDay, Permission, Extended

HERE = sys._getframe().f_code.co_filename

MEMBER = """The position belongs to the enumeration, not to the member:
'Day[x]' gives the member at position 'x', and iterating 'Day' gives
its members in order."""

DECLARATION = """The position belongs to the enumeration, not to the
declaration of a member: 'Day[x]' gives the member at position 'x'."""

MASK = """The bit mask belongs to the class, not to the member: 'Flags[x]'
gives the member of mask 'x', and iterating 'Flags' gives its members in
the order of their masks."""


class TestKeeIndexDeprecation(KeenumTest):
  """
  The 'index' of a member is deprecated, and with it 'int(member)', a
  member used as an index, and the 'index' and 'int()' of a 'Kee'. Each
  still answers as before, and gives a 'DeprecatedPromise' at the line
  that asked. The same holds for the members of a flags class, whose
  index is the bit mask in the class that built the member. Building,
  resolving and iterating an enumeration or a flags class gives no
  notice. The tests pin each notice, its feature, its text and its
  line, and the silence of the work of the classes themselves.
  """

  def assertNotice(self, log: list, feature: str, text: str) -> None:
    """The log holds one 'DeprecatedPromise' for 'feature', worded with
    'text', given at the line recorded on the test as 'line'."""
    self.assertEqual(len(log), 1)
    entry = log[0]
    self.assertIs(entry.category, DeprecatedPromise)
    self.assertEqual(entry.filename, HERE)
    self.assertEqual(entry.lineno, self.line)
    self.assertEqual(entry.message.feature, feature)
    self.assertEqual(entry.message.description, str.join(' ', text.split()))

  def test_member_index(self) -> None:
    with warnings.catch_warnings(record=True) as log:
      warnings.simplefilter('always')
      self.line = sys._getframe().f_lineno + 1
      index = WeekDay.WEDNESDAY.index
    self.assertEqual(index, 2)
    self.assertNotice(log, 'worktoy.keenum.KeeBase.index', MEMBER)
    expected = """Deprecation alert: 'worktoy.keenum.KeeBase.index' is no
    longer a promised feature beginning with the next major update."""
    self.assertIn(str.join(' ', expected.split()), str(log[0].message))

  def test_member_int(self) -> None:
    with warnings.catch_warnings(record=True) as log:
      warnings.simplefilter('always')
      self.line = sys._getframe().f_lineno + 1
      index = int(WeekDay.WEDNESDAY)
    self.assertEqual(index, 2)
    self.assertNotice(log, 'worktoy.keenum.KeeBase.__int__', MEMBER)

  def test_member_as_an_index(self) -> None:
    with warnings.catch_warnings(record=True) as log:
      warnings.simplefilter('always')
      self.line = sys._getframe().f_lineno + 1
      letter = ['a', 'b', 'c'][WeekDay.WEDNESDAY]
    self.assertEqual(letter, 'c')
    self.assertNotice(log, 'worktoy.keenum.KeeBase.__index__', MEMBER)

  def test_kee_index(self) -> None:
    kee = Kee[int](1)
    with warnings.catch_warnings(record=True) as log:
      warnings.simplefilter('always')
      self.line = sys._getframe().f_lineno + 1
      kee.index = 3
    self.assertNotice(log, 'worktoy.keenum.Kee.index', DECLARATION)
    with warnings.catch_warnings(record=True) as log:
      warnings.simplefilter('always')
      self.line = sys._getframe().f_lineno + 1
      index = kee.index
    self.assertEqual(index, 3)
    self.assertNotice(log, 'worktoy.keenum.Kee.index', DECLARATION)
    with warnings.catch_warnings(record=True) as log:
      warnings.simplefilter('always')
      self.line = sys._getframe().f_lineno + 1
      index = int(kee)
    self.assertEqual(index, 3)
    self.assertNotice(log, 'worktoy.keenum.Kee.__int__', DECLARATION)

  def test_the_enumeration_itself_is_silent(self) -> None:
    with warnings.catch_warnings(record=True) as log:
      warnings.simplefilter('always')

      class Local(KeeNum):
        A = Kee[int](1)
        B = Kee[int](2)

      class Sub(Local):
        C = Kee[int](3)

      self.assertIs(Local[1], Local.B)
      self.assertIs(Local(2), Local.B)
      self.assertIs(Local.fromValue(1), Local.A)
      self.assertEqual([*Sub], [Local.A, Local.B, Sub.C])
      self.assertIn(Sub.C, Local)
      self.assertIs(Sub.A.kee, Local.A.kee)
    self.assertEqual(log, [])

  def test_flags_member_index(self) -> None:
    with warnings.catch_warnings(record=True) as log:
      warnings.simplefilter('always')
      self.line = sys._getframe().f_lineno + 1
      index = Permission.READ_WRITE.index
    self.assertEqual(index, 3)
    self.assertNotice(log, 'worktoy.keenum.KeeFlags.index', MASK)
    with warnings.catch_warnings(record=True) as log:
      warnings.simplefilter('always')
      self.line = sys._getframe().f_lineno + 1
      index = int(Extended.READ_OWN)
    self.assertEqual(index, 9)
    self.assertNotice(log, 'worktoy.keenum.KeeFlags.__int__', MASK)
    with warnings.catch_warnings(record=True) as log:
      warnings.simplefilter('always')
      self.line = sys._getframe().f_lineno + 1
      letter = 'abcd'[Extended.WRITE]
    self.assertEqual(letter, 'c')
    self.assertNotice(log, 'worktoy.keenum.KeeFlags.__index__', MASK)
    with self.assertWarns(DeprecatedPromise):
      masks = [int(flag) for flag in Extended.flags]
    self.assertEqual(masks, [1, 2, 4, 8])

  def test_flags_class_itself_is_silent(self) -> None:
    with warnings.catch_warnings(record=True) as log:
      warnings.simplefilter('always')

      class Local(KeeFlags):
        A = Kee[str]()
        B = Kee[str]()

      class Sub(Local):
        C = Kee[str]()

      self.assertIs(Local[3], Local.A_B)
      self.assertIs(Local('a', 'b'), Local.A_B)
      self.assertIs(Local.A | Sub.C, Sub.A_C)
      self.assertIs(~Sub.A_C, Sub.B)
      self.assertEqual(len([*Sub]), 8)
      self.assertIn(Sub.C, Local)
    self.assertEqual(log, [])

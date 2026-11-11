"""
TestKeeBoxDeprecation tests the deprecation notice of 'KeeBox' from
'worktoy.keenum'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import sys
import warnings

from worktoy.keenum import KeeBox
from worktoy.mcls import BaseObject
from worktoy.waitaminute import DeprecatedPromise, TypeException
from . import KeenumTest, WeekDay, Permission

HERE = sys._getframe().f_code.co_filename


class TestKeeBoxDeprecation(KeenumTest):
  """
  'KeeBox' is deprecated: it works as it did, and every subscript of
  it gives a 'DeprecatedPromise' at the line that wrote the subscript.
  The tests pin the notice, its feature, its text and its line, one
  notice for each subscript, the box still reading its member, and the
  notice given before a subscript is refused.
  """

  def test_each_subscript_gives_the_notice(self) -> None:
    with warnings.catch_warnings(record=True) as log:
      warnings.simplefilter('always')
      line = sys._getframe().f_lineno + 3

      class Shift(BaseObject):
        day = KeeBox[WeekDay]('tuesday')
        access = KeeBox[Permission]('read', 'exec')

    self.assertEqual(len(log), 2)
    for offset, entry in enumerate(log):
      self.assertIs(entry.category, DeprecatedPromise)
      self.assertIsInstance(entry.message, FutureWarning)
      self.assertEqual(entry.filename, HERE)
      self.assertEqual(entry.lineno, line + offset)
      self.assertIs(entry.message.feature, KeeBox)
      self.assertEqual(entry.message.description, """Declare the field
        with 'AttriBox' instead, giving the member itself as the
        default.""".replace('\n        ', ' '))
    expected = """Deprecation alert: 'worktoy.keenum.KeeBox' is no longer
    a promised feature beginning with the next major update. Declare
    the field with 'AttriBox' instead, giving the member itself as the
    default."""
    self.assertEqual(str(log[0].message), str.join(' ', expected.split()))
    shift = Shift()
    self.assertIs(shift.day, WeekDay.TUESDAY)
    self.assertIs(shift.access, Permission.READ_EXEC)

  def test_notice_before_a_refusal(self) -> None:
    with self.assertWarns(DeprecatedPromise) as context:
      with self.assertRaises(TypeException) as refusal:
        line = sys._getframe().f_lineno + 1
        KeeBox[int]
    self.assertEqual(refusal.exception.varName, 'fieldType')
    self.assertIs(refusal.exception.actualObject, int)
    self.assertEqual(context.filename, HERE)
    self.assertEqual(context.lineno, line)

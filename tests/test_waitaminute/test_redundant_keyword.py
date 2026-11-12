"""
TestRedundantKeyword tests 'RedundantKeyword' from 'worktoy.waitaminute'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import sys

from worktoy.utilities import joinWords
from worktoy.waitaminute import WorkToyWarning, RedundantKeyword
from . import WaitaminuteTest

HERE = sys._getframe().f_code.co_filename


class TestRedundantKeyword(WaitaminuteTest):
  """
  'RedundantKeyword' is given where a function received a keyword it
  does not read and went on without it: a 'UserWarning' naming the
  function, the keyword, and the keywords the function does read. It
  keeps all three. The tests pin the bases and the slots, the text for
  one keyword read, for several and for none, and the line the warning
  lands on.
  """

  def test_bases_and_slots(self) -> None:
    self.assertEqual(RedundantKeyword.__bases__,
      (WorkToyWarning, UserWarning))
    self.assertEqual(RedundantKeyword.__slots__,
      ('receiver', 'keyword', 'options'))

  def test_text(self) -> None:
    warning = RedundantKeyword(joinWords, 'seperator', 'sep')
    self.assertIs(warning.receiver, joinWords)
    self.assertEqual(warning.keyword, 'seperator')
    self.assertEqual(warning.options, ('sep',))
    expected = """'worktoy.utilities.joinWords' received the keyword
    'seperator', which it does not read, and went on without it! It
    reads: 'sep'."""
    self.assertEqual(str(warning), str.join(' ', expected.split()))
    self.assertEqual(repr(warning), str(warning))

  def test_text_of_several_options(self) -> None:
    warning = RedundantKeyword('paint', 'colour', 'color', 'size')
    self.assertEqual(warning.receiver, 'paint')
    self.assertEqual(warning.options, ('color', 'size'))
    expected = """'paint' received the keyword 'colour', which it does
    not read, and went on without it! It reads: 'color', 'size'."""
    self.assertEqual(str(warning), str.join(' ', expected.split()))

  def test_text_without_options(self) -> None:
    warning = RedundantKeyword('paint', 'colour')
    self.assertEqual(warning.options, ())
    expected = """'paint' received the keyword 'colour', which it does
    not read, and went on without it! It reads no keyword."""
    self.assertEqual(str(warning), str.join(' ', expected.split()))

  def test_given_as_a_user_warning(self) -> None:
    warning = RedundantKeyword(joinWords, 'seperator', 'sep')
    with self.assertWarns(UserWarning) as context:
      line = sys._getframe().f_lineno + 1
      warning.warn()
    self.assertIs(context.warning, warning)
    self.assertEqual(context.filename, HERE)
    self.assertEqual(context.lineno, line)

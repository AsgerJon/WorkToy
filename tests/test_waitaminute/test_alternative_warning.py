"""
TestAlternativeWarning tests 'AlternativeWarning' from
'worktoy.waitaminute'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import sys

from worktoy.waitaminute import WorkToyWarning, AlternativeWarning
from . import WaitaminuteTest, Till

HERE = sys._getframe().f_code.co_filename
#  The name of this folder as a package: 'tests.test_waitaminute' under
#  pytest, 'test_waitaminute' when 'unittest' discovers from 'tests'.
HOME = __name__.rsplit('.', 1)[0]


class TestAlternativeWarning(WaitaminuteTest):
  """
  'AlternativeWarning' is given where a promised behaviour has a better
  way beside it: a 'UserWarning' naming the behaviour, what to use
  instead and why. It keeps all three. The tests pin the bases and the
  slots, the text for things handed over as themselves and as names,
  and the line the warning lands on.
  """

  def test_bases_and_slots(self) -> None:
    self.assertEqual(AlternativeWarning.__bases__,
      (WorkToyWarning, UserWarning))
    self.assertEqual(AlternativeWarning.__slots__,
      ('behaviour', 'alternative', 'reason'))

  def test_text(self) -> None:
    reason = 'the till already keeps the sum'
    warning = AlternativeWarning(Till.recount, Till.cash, reason)
    self.assertIs(warning.behaviour, Till.recount)
    self.assertIs(warning.alternative, Till.cash)
    self.assertEqual(warning.reason, reason)
    expected = """Although '%s.Till.recount' is promised to function,
    use '%s.Till.cash' instead, because the till already keeps the
    sum!""" % (HOME, HOME)
    self.assertEqual(str(warning), str.join(' ', expected.split()))
    self.assertEqual(repr(warning), str(warning))

  def test_text_from_names(self) -> None:
    warning = AlternativeWarning('shop.recount', 'shop.cash', 'it is less')
    expected = """Although 'shop.recount' is promised to function, use
    'shop.cash' instead, because it is less!"""
    self.assertEqual(str(warning), str.join(' ', expected.split()))

  def test_given_as_a_user_warning(self) -> None:
    warning = AlternativeWarning('shop.recount', 'shop.cash', 'it is less')
    with self.assertWarns(UserWarning) as context:
      line = sys._getframe().f_lineno + 1
      warning.warn()
    self.assertIs(context.warning, warning)
    self.assertEqual(context.filename, HERE)
    self.assertEqual(context.lineno, line)

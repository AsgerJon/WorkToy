"""
TestRiskWarning tests 'RiskWarning' from 'worktoy.waitaminute'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import sys

from worktoy.waitaminute import WorkToyWarning, RiskWarning
from . import WaitaminuteTest

HERE = sys._getframe().f_code.co_filename


class TestRiskWarning(WaitaminuteTest):
  """
  'RiskWarning' is given where an object received at a name is carried
  out as promised and is still risky: a 'RuntimeWarning' naming the
  name, the object and its type, and the risk. It keeps all three. The
  tests pin the bases and the slots, the text, the cut of a long
  object, and the line the warning lands on.
  """

  def test_bases_and_slots(self) -> None:
    self.assertEqual(RiskWarning.__bases__,
      (WorkToyWarning, RuntimeWarning))
    self.assertEqual(RiskWarning.__slots__,
      ('varName', 'actualObject', 'risk'))

  def test_text(self) -> None:
    warning = RiskWarning('price', -5, 'a till that pays the customer')
    self.assertEqual(warning.varName, 'price')
    self.assertEqual(warning.actualObject, -5)
    self.assertEqual(warning.risk, 'a till that pays the customer')
    expected = """Received object at name 'price': -5 of type 'int'.
    This is promised to function correctly, but risks a till that pays
    the customer!"""
    self.assertEqual(str(warning), str.join(' ', expected.split()))
    self.assertEqual(repr(warning), str(warning))

  def test_long_object_is_cut(self) -> None:
    fits = 'x' * 48  # shown in 50 characters, quotes included
    warning = RiskWarning('note', fits, 'a full page')
    self.assertIn(""": %s of type 'str'""" % repr(fits), str(warning))
    long = 'x' * 49  # shown in 51 characters
    warning = RiskWarning('note', long, 'a full page')
    self.assertIs(warning.actualObject, long)
    cut = """%s...""" % repr(long)[:47]
    self.assertEqual(len(cut), 50)
    self.assertIn(""": %s of type 'str'""" % cut, str(warning))
    self.assertNotIn(repr(long), str(warning))

  def test_given_as_a_runtime_warning(self) -> None:
    warning = RiskWarning('price', -5, 'a loss')
    with self.assertWarns(RuntimeWarning) as context:
      line = sys._getframe().f_lineno + 1
      warning.warn()
    self.assertIs(context.warning, warning)
    self.assertEqual(context.filename, HERE)
    self.assertEqual(context.lineno, line)

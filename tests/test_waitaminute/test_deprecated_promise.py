"""
TestDeprecatedPromise tests 'DeprecatedPromise' from
'worktoy.waitaminute'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import sys
import warnings

from worktoy.waitaminute import WorkToyWarning, DeprecatedPromise
from . import WaitaminuteTest, Till

HERE = sys._getframe().f_code.co_filename


class TestDeprecatedPromise(WaitaminuteTest):
  """
  'DeprecatedPromise' is the deprecation notice of worktoy and of the
  projects built upon it: a 'FutureWarning' saying that a feature is no
  longer promised from the next major update, followed by whatever the
  author wrote for that one deprecation. It keeps the feature and the
  description. The tests pin the bases and the slots, the text with and
  without a description, a feature handed over as itself and as a
  dotted name, and the line the notice lands on.
  """

  def test_bases_and_slots(self) -> None:
    self.assertEqual(DeprecatedPromise.__bases__,
      (WorkToyWarning, FutureWarning))
    self.assertEqual(DeprecatedPromise.__slots__,
      ('feature', 'description'))

  def test_with_a_description(self) -> None:
    info = "Use 'Till.cash' instead."
    warning = DeprecatedPromise(Till.recount, info)
    self.assertIs(warning.feature, Till.recount)
    self.assertEqual(warning.description, info)
    expected = """Deprecation alert: 'tests.test_waitaminute.Till.recount'
    is no longer a promised feature beginning with the next major
    update. Use 'Till.cash' instead."""
    self.assertEqual(str(warning), str.join(' ', expected.split()))
    self.assertEqual(repr(warning), str(warning))

  def test_without_a_description(self) -> None:
    warning = DeprecatedPromise('shop.Till.ring')
    self.assertEqual(warning.feature, 'shop.Till.ring')
    self.assertEqual(warning.description, '')
    expected = """Deprecation alert: 'shop.Till.ring' is no longer a
    promised feature beginning with the next major update."""
    self.assertEqual(str(warning), str.join(' ', expected.split()))
    self.assertEqual(repr(warning), str(warning))

  def test_given_as_a_future_warning(self) -> None:
    warning = DeprecatedPromise('shop.Till.ring')
    with self.assertWarns(FutureWarning) as context:
      line = sys._getframe().f_lineno + 1
      warning.warn()
    self.assertIs(context.warning, warning)
    self.assertEqual(context.filename, HERE)
    self.assertEqual(context.lineno, line)
    with warnings.catch_warnings():
      warnings.simplefilter('error')
      with self.assertRaises(DeprecatedPromise):
        warning.warn()

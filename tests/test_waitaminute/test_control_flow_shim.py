"""
TestControlFlowShim tests the deprecation notice of
'worktoy.waitaminute.control_flow'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import sys
import warnings

from worktoy.core import control_flow as newHome
from worktoy.waitaminute import DeprecatedPromise
from worktoy.waitaminute import control_flow as oldHome
from worktoy.waitaminute.meta import ControlClassError
from . import WaitaminuteTest

HERE = sys._getframe().f_code.co_filename


class TestControlFlowShim(WaitaminuteTest):
  """
  The names of 'worktoy.waitaminute.control_flow' moved, and the old
  package hands each of them out from its new home with a
  'DeprecatedPromise' at the line that asked. The tests pin the notice
  for each of the five names, its feature, its description and its
  line, at an attribute read and at an import statement, and that a
  name the package never had is refused without a notice.
  """

  def test_signals(self) -> None:
    for name in ('ControlSpace', 'MetaFlow', 'ControlFlow', 'SkipSet'):
      with self.subTest(name=name):
        with self.assertWarns(DeprecatedPromise) as context:
          line = sys._getframe().f_lineno + 1
          found = getattr(oldHome, name)
        self.assertIs(found, getattr(newHome, name))
        self.assertEqual(context.filename, HERE)
        self.assertEqual(context.lineno, line)
        warning = context.warning
        self.assertEqual(warning.feature,
          """worktoy.waitaminute.control_flow.%s""" % name)
        self.assertEqual(warning.description,
          "Import it from 'worktoy.core.control_flow', where it lives now.")

  def test_control_class_error(self) -> None:
    with self.assertWarns(DeprecatedPromise) as context:
      line = sys._getframe().f_lineno + 1
      found = oldHome.ControlClassError
    self.assertIs(found, ControlClassError)
    #  A name put together at run time is the same name.
    built = str.join('', ['Control', 'Class', 'Error'])
    with self.assertWarns(DeprecatedPromise):
      self.assertIs(getattr(oldHome, built), ControlClassError)
    self.assertEqual(context.filename, HERE)
    self.assertEqual(context.lineno, line)
    warning = context.warning
    self.assertEqual(warning.feature,
      'worktoy.waitaminute.control_flow.ControlClassError')
    self.assertEqual(warning.description,
      "Import it from 'worktoy.waitaminute.meta', where it lives now.")
    expected = """Deprecation alert:
    'worktoy.waitaminute.control_flow.ControlClassError' is no longer a
    promised feature beginning with the next major update. Import it
    from 'worktoy.waitaminute.meta', where it lives now."""
    self.assertEqual(str(warning), str.join(' ', expected.split()))

  def test_import_statement(self) -> None:
    with warnings.catch_warnings(record=True) as log:
      warnings.simplefilter('always')
      line = sys._getframe().f_lineno + 1
      from worktoy.waitaminute.control_flow import SkipSet
    self.assertIs(SkipSet, newHome.SkipSet)
    self.assertTrue(log)
    for entry in log:
      self.assertIsInstance(entry.message, DeprecatedPromise)
      self.assertEqual(entry.filename, HERE)
      self.assertEqual(entry.lineno, line)

  def test_unknown_name(self) -> None:
    with warnings.catch_warnings(record=True) as log:
      warnings.simplefilter('always')
      with self.assertRaises(AttributeError) as context:
        _ = oldHome.nothing
      #  A name sorting before every name of the package.
      with self.assertRaises(AttributeError) as early:
        _ = oldHome.Absent
    self.assertEqual(log, [])
    text = str(context.exception)
    self.assertIn("'worktoy.waitaminute.control_flow'", text)
    self.assertIn("'nothing'", text)
    self.assertIn("'Absent'", str(early.exception))

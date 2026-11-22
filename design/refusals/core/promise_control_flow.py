"""
RefusedControlFlow holds the refusals that belong with
'design.promises.core.promise_control_flow'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.core.control_flow import ControlFlow
from worktoy.waitaminute.meta import ControlClassError


class RefusedControlFlow(TestCase):
  """
  Each of the following is refused, and the exception named is the one raised
  as of 1.2.3. Any other name in the body of a signal, a method, a class
  attribute or '__namespace__', raises 'ControlClassError' naming it. Source:
  the docstrings of the 'control_flow' package, 'ControlFlow', 'SkipSet',
  'MetaFlow' and 'ControlSpace', and the 1.1.0 changelog entry "A
  control-flow signal body may not bind __namespace__".
  """

  def test_body_refused(self) -> None:
    for badKey in ('method', 'count', '__namespace__'):
      with self.subTest(badKey=badKey):
        with self.assertRaises(Exception) as refused:
          if badKey == 'method':
            class Bad(ControlFlow):
              def method(self) -> None:
                pass
          elif badKey == 'count':
            class Bad(ControlFlow):
              count = 3
          else:
            class Bad(ControlFlow):
              __namespace__ = None
        self.assertIsInstance(refused.exception, ControlClassError)

"""
TestControlFlowSuper subclasses 'WaitAMinuteTest' and pins that a
'ControlFlow' subclass may use 'super()' in its '__str__'. 'super()'
makes the interpreter bind '__classcell__' in the class body, and on
Python 3.14 '__classdictcell__' as well, and 'ControlSpace' refused both
as attributes the class may not have.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.waitaminute.control_flow import ControlFlow, ControlClassError

from . import WaitAMinuteTest


class TestControlFlowSuper(WaitAMinuteTest):
  """
  TestControlFlowSuper provides tests for 'super()' in a 'ControlFlow'
  subclass.
  """

  def test_super_in_str(self) -> None:
    """'__str__' may call 'super()'."""

    class Halt(ControlFlow):
      def __str__(self) -> str:
        return 'halt: %s' % super().__str__()

    self.assertEqual(str(Halt()), 'halt: %s' % str(Halt))

  def test_other_attributes_refused(self) -> None:
    """Any other method is still refused."""
    with self.assertRaises(ControlClassError):
      class Halt(ControlFlow):
        def run(self) -> None:
          pass  # pragma: no cover

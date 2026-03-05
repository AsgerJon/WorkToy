"""
TestControlFlow tests the 'worktoy.waitaminute.control_flow' package.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from tests.test_waitaminute import WaitAMinuteTest
from worktoy.waitaminute import VariableNotNone
from worktoy.waitaminute.control_flow import ControlClassError, ControlFlow
from worktoy.waitaminute.control_flow import ControlSpace, SkipSet

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class ChillOut(ControlFlow):
  """Just a chill control flow."""


class TestControlFlow(WaitAMinuteTest):
  """
  TestControlFlow tests the 'worktoy.waitaminute.control_flow' package.
  """

  def test_not_white_listed(self, ) -> None:
    """
    Tests that 'ControlClassError' is raised when trying to create a
    control flow class with banned attributes.
    """

    with self.assertRaises(ControlClassError) as context:
      class BadFlow(ControlFlow):

        def __reduce__(self, ) -> Any:
          """Imagine using pickling..."""
    e = context.exception
    self.assertEqual(e.badKey, '__reduce__')
    self.assertIsInstance(e.space, ControlSpace)

  def test_not_on_exception(self, ) -> None:
    """
    Tests that 'ControlClassError' is raised when trying to create a
    control flow class with banned attributes, even if it doesn't inherit
    from 'Exception'.
    """

    with self.assertRaises(ControlClassError) as context:
      class BadFlow(ControlFlow):
        def breh(self) -> None:
          """Just a random method."""
    e = context.exception
    self.assertEqual(e.badKey, 'breh')
    self.assertIsInstance(e.space, ControlSpace)

  def test_duplicate_root_flow(self) -> None:
    """
    Tests that a second control flow class created with keyword argument
    '_root=True' raises a 'VariableNotNone'. The 'MetaFlow' metaclass
    should have only one root control flow class.
    """
    with self.assertRaises(VariableNotNone) as context:
      class BadFlow(ControlFlow, _root=True):
        """Trying to make a second root control flow."""
    e = context.exception
    self.assertEqual(e.name, '__root_cls__')
    self.assertIs(e.value, ControlFlow)

  def test_meta_flow(self) -> None:
    """
    Tests that 'MetaFlow' is properly setting up the control flow classes.
    """

    self.assertEqual(str(ChillOut), '<ControlFlow: ChillOut>')
    self.assertEqual(str(ControlFlow), '<ControlFlow: [Root]>')
    for cls in (ChillOut, ControlFlow, SkipSet):
      try:
        raise cls
      except cls as e:
        self.assertEqual(str(cls), str(e))

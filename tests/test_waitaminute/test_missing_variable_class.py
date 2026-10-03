"""
TestMissingVariableClass subclasses 'WaitAMinuteTest' and pins that a
'MissingVariable' raised for a class names that class. It named the type
of the instance it was given, which for a class is its metaclass, so
reading 'BaseObject.nope' reported "Missing 'BaseMeta.nope'!".
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.mcls import BaseObject
from worktoy.waitaminute import MissingVariable

from . import WaitAMinuteTest


class Plain(BaseObject):
  """Plain is a class with no attribute named 'nope'."""


class TestMissingVariableClass(WaitAMinuteTest):
  """
  TestMissingVariableClass provides tests for the owner a
  'MissingVariable' names.
  """

  def test_class_attribute_names_class(self) -> None:
    """A miss on a class names the class, not its metaclass."""
    with self.assertRaises(MissingVariable) as context:
      _ = Plain.nope
    message = str(context.exception)
    self.assertIn("'Plain.nope'", message)
    self.assertNotIn('BaseMeta', message)

  def test_instance_names_its_type(self) -> None:
    """A miss on an instance still names the type of the instance."""
    exception = MissingVariable(Plain(), 'nope', int)
    self.assertIn("'Plain.nope: int'", str(exception))

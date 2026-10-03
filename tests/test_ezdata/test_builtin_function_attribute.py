"""
TestBuiltinFunctionAttribute subclasses 'EZTest' and pins that a builtin
function bound in an EZData class body stays a class attribute, as a
function written in Python does, rather than becoming a field. 'EZHook'
let only Python functions through, so 'helper = len' made a field of
'len', which then showed up in the fields, the constructor, 'asDict' and
the 'repr'. A callable instance of an ordinary class is a value and
still becomes a field.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.ezdata import EZData, EZField

from . import EZTest


class Doubler:
  """Doubler is a callable class, whose instances are values."""

  def __call__(self, x: int) -> int:
    return x * 2  # pragma: no cover


class Tool(EZData):
  """Tool binds a builtin function and a callable instance."""

  helper = len
  method = [].append
  doubler = Doubler()
  x = EZField[int](0)


class TestBuiltinFunctionAttribute(EZTest):
  """
  TestBuiltinFunctionAttribute provides tests for a builtin function in
  an EZData class body.
  """

  def test_builtin_not_a_field(self) -> None:
    """Builtin functions and methods are not fields."""
    self.assertEqual([f.fieldName for f in Tool.fields], ['doubler', 'x'])
    self.assertEqual(Tool().asDict().keys(), {'doubler', 'x'})

  def test_builtin_is_class_attribute(self) -> None:
    """A builtin function stays a class attribute, called as given."""
    self.assertIs(Tool.helper, len)
    self.assertEqual(Tool().helper('abc'), 3)

  def test_constructor(self) -> None:
    """The constructor takes the fields alone."""
    tool = Tool(Doubler(), 5)
    self.assertEqual(tool.x, 5)

"""
TestUnnamedExpectedType subclasses 'WaitAMinuteTest' and pins that
'TypeException' and 'MissingVariable' render an expected type that has
no '__name__', by its 'str', as 'KeeTypeException' already did. Both used
to read '__name__' off every expected type, so a 'typing' alias such as
'typing.Callable', which lacks the attribute on Python 3.7 to 3.9, made
their own 'str' raise 'AttributeError'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import Callable

from worktoy.waitaminute import TypeException, MissingVariable

from . import WaitAMinuteTest


class Unnamed:
  """Unnamed stands for an expected type without '__name__'."""

  def __str__(self) -> str:
    return 'Unnamed'


class TestUnnamedExpectedType(WaitAMinuteTest):
  """
  TestUnnamedExpectedType provides tests for rendering an expected type
  without '__name__'.
  """

  def test_type_exception(self) -> None:
    """'TypeException' renders the expected type by its 'str'."""
    info = str(TypeException('func', 3, Unnamed(), int))
    self.assertIn("'Unnamed'", info)
    self.assertIn("'int'", info)

  def test_missing_variable_single(self) -> None:
    """'MissingVariable' renders a single expected type by its 'str'."""
    info = str(MissingVariable(object(), 'func', Unnamed()))
    self.assertIn('func: Unnamed', info)

  def test_missing_variable_several(self) -> None:
    """'MissingVariable' renders several expected types, named or not."""
    info = str(MissingVariable(object(), 'func', int, Unnamed()))
    self.assertIn('Union[int, Unnamed]', info)

  def test_typing_callable(self) -> None:
    """'typing.Callable' renders on every version."""
    self.assertIn('Callable', str(TypeException('func', 3, Callable)))
    self.assertIn('Callable', str(MissingVariable(object(), 'f', Callable)))

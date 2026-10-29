"""
TestInheritedExactPrecedence subclasses 'OverloadTest' and pins that the
match of a subclass wins over an inherited one, whichever dispatch pass
finds it. An override broader than the inherited signature takes the
calls the inherited signature matches exactly as well: with
'@overload(int)' inherited and '@overload(object)' declared, 'f(1)'
reaches the subclass. The inherited signature used to keep the calls it
matched exactly, so the override took 'f(True)' but not 'f(1)'. A call
the subclass does not accept still reaches the inherited overload.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core.sentinels import ARGS
from worktoy.dispatch import overload
from worktoy.mcls import BaseObject
from . import OverloadTest


class Parent(BaseObject):
  """Parent declares an overload taking an 'int'."""

  @overload(int)
  def f(self, x: int) -> str:
    return 'parent int'


class Broad(Parent):
  """Broad adds an override taking any object."""

  @overload(object)
  def f(self, x: object) -> str:
    return 'broad object'


class Narrow(Parent):
  """Narrow adds an overload the 'int' calls do not match."""

  @overload(str)
  def f(self, x: str) -> str:
    return 'narrow str'


class Variadic(Parent):
  """Variadic adds a variadic signature accepting a lone 'int'."""

  @overload(ARGS[int])
  def f(self, *xs: int) -> str:
    return 'variadic'


class Deeper(Broad):
  """Deeper declares nothing and inherits both overloads."""


class TestInheritedExactPrecedence(OverloadTest):
  """
  TestInheritedExactPrecedence provides tests for an inherited exact
  signature beside a broader override in a subclass.
  """

  def test_subclass_takes_exact_call(self) -> None:
    """A call the inherited signature matches exactly goes to the
    broader override of the subclass."""
    self.assertEqual(Broad().f(1), 'broad object')

  def test_subclass_takes_other_calls(self) -> None:
    """The override takes the calls no signature matches exactly, a
    subclass of 'int' included."""
    self.assertEqual(Broad().f(True), 'broad object')
    self.assertEqual(Broad().f(2.5), 'broad object')

  def test_unmatched_call_reaches_parent(self) -> None:
    """A call the subclass does not accept still reaches the inherited
    overload."""
    self.assertEqual(Narrow().f(1), 'parent int')
    self.assertEqual(Narrow().f('a'), 'narrow str')

  def test_variadic_takes_exact_call(self) -> None:
    """A variadic signature of the subclass takes the call as well."""
    self.assertEqual(Variadic().f(1), 'variadic')
    self.assertEqual(Variadic().f(True), 'variadic')

  def test_nearest_class_wins(self) -> None:
    """A class inheriting both sends the call to the nearer one."""
    self.assertEqual(Deeper().f(1), 'broad object')

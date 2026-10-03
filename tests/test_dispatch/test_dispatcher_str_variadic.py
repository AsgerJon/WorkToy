"""
TestDispatcherStrVariadic subclasses 'DispatcherTest' and pins that the
'str()' of a 'Dispatcher' shows a variadic declaration as itself, as the
message of 'DispatchException' does, and nothing the class body did not
write. It used to list the six concrete signatures that
'@overload(str, ARGS[int])' was expanded into for short calls and leave
out the declaration itself; no such expansion exists any more.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core.sentinels import ARGS
from worktoy.dispatch import overload
from worktoy.mcls import BaseObject

from . import DispatcherTest


class Owner(BaseObject):
  """Owner overloads 'f' with a variadic and a concrete signature."""

  @overload(str, ARGS[int])
  def f(self, *args) -> None:
    """The variadic declaration."""

  @overload(float)
  def f(self, value: float) -> None:
    """The concrete declaration."""


class TestDispatcherStrVariadic(DispatcherTest):
  """
  TestDispatcherStrVariadic provides tests for the 'str()' of a
  'Dispatcher' holding a variadic signature.
  """

  def test_declaration_shown(self) -> None:
    """The variadic declaration is listed as written."""
    text = str(Owner.__dict__['f'])
    self.assertIn('<TypeSig: [str, ARGS[int]]>', text)
    self.assertIn('<TypeSig: [float]>', text)

  def test_expansions_hidden(self) -> None:
    """No signature the class body did not write is listed."""
    text = str(Owner.__dict__['f'])
    self.assertNotIn('<TypeSig: [str]>', text)
    self.assertNotIn('<TypeSig: [str, int]>', text)

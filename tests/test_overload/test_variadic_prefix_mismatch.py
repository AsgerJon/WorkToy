"""
TestVariadicPrefixMismatch subclasses 'OverloadTest' and pins that two
variadic declarations whose prefixes differ at a shared position share no
call, so a class may declare both, and each receives the calls its prefix
opens. 'BaseSpace.sharedCall' answers None for such a pair as soon as the
prefixes differ, before it looks at what follows the shorter prefix.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core.sentinels import ARGS
from worktoy.dispatch import overload, TypeSig
from worktoy.mcls import BaseObject, BaseSpace

from . import OverloadTest


class Mismatched(BaseObject):
  """Mismatched declares two variadics of one inner type whose prefixes
  differ in their first entry."""

  @overload(int, ARGS[str])
  def f(self, n: int, *words: str) -> str:
    return 'counted'

  @overload(str, ARGS[str])
  def f(self, label: str, *words: str) -> str:
    return 'labelled'


class TestVariadicPrefixMismatch(OverloadTest):
  """
  TestVariadicPrefixMismatch provides tests for two variadic declarations
  whose prefixes differ at a shared position.
  """

  def test_class_builds_and_dispatches(self) -> None:
    """The pair shares no call, so the class builds, and each declaration
    takes the calls its prefix opens, with or without trailing words."""
    self.assertEqual(Mismatched().f(1, 'a', 'b'), 'counted')
    self.assertEqual(Mismatched().f(1), 'counted')
    self.assertEqual(Mismatched().f('x', 'a'), 'labelled')
    self.assertEqual(Mismatched().f('x'), 'labelled')

  def test_shared_call_is_none(self) -> None:
    """'sharedCall' answers None as soon as the prefixes differ, in either
    order of the pair."""
    first = TypeSig(int, ARGS[str])
    second = TypeSig(str, ARGS[str])
    self.assertIsNone(BaseSpace.sharedCall(first, second))
    self.assertIsNone(BaseSpace.sharedCall(second, first))

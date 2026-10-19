"""
TestVariadicLatestWins subclasses 'OverloadTest' and pins that two
variadic declarations accepting one call by exact type are no conflict:
the most recent declaration of the nearest class takes the call, within
one class body as across a subclass. Such a pair in one body used to be
refused at class creation with 'VariadicOverlap', a decision reversed on
2026-10-19. An explicit declaration of the call still takes it, by exact
type, wherever it stands.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core.sentinels import ARGS
from worktoy.dispatch import overload
from worktoy.mcls import BaseObject

from . import OverloadTest


class Tab(BaseObject):
  """Tab declares two variadics sharing the call 'f(1)'."""

  @overload(int, ARGS[int])
  def f(self, head: int, *tail: int) -> str:
    return 'ints'

  @overload(int, ARGS[str])
  def f(self, head: int, *tail: str) -> str:
    return 'strs'


class Triple(Tab):
  """Triple adds a third, so the newest of the nearest class wins."""

  @overload(int, ARGS[float])
  def f(self, head: int, *tail: float) -> str:
    return 'floats'


class Settled(Tab):
  """Settled declares the shared call explicitly."""

  @overload(int)
  def f(self, head: int) -> str:
    return 'explicit'


class TestVariadicLatestWins(OverloadTest):
  """
  TestVariadicLatestWins provides tests for variadic declarations sharing
  a call.
  """

  def test_latest_in_body_wins(self) -> None:
    """The class builds, the later declaration takes the shared call,
    and the tails still decide the longer calls."""
    tab = Tab()
    self.assertEqual(tab.f(1), 'strs')
    self.assertEqual(tab.f(1, 2), 'ints')
    self.assertEqual(tab.f(1, 'a'), 'strs')

  def test_nearest_class_wins(self) -> None:
    """A subclass declaration is the most recent of all."""
    triple = Triple()
    self.assertEqual(triple.f(1), 'floats')
    self.assertEqual(triple.f(1, 2.5), 'floats')
    self.assertEqual(triple.f(1, 2), 'ints')
    self.assertEqual(triple.f(1, 'a'), 'strs')

  def test_explicit_still_takes_the_call(self) -> None:
    """An explicit declaration of the shared call takes it by exact
    type ahead of every variadic."""
    settled = Settled()
    self.assertEqual(settled.f(1), 'explicit')
    self.assertEqual(settled.f(1, 2), 'ints')

  def test_isinstance_pass_agrees(self) -> None:
    """A call reaching the variadics through 'isinstance' alone, a
    'bool' head here, goes to the most recent as well."""
    self.assertEqual(Tab().f(True), 'strs')
    self.assertEqual(Triple().f(True), 'floats')

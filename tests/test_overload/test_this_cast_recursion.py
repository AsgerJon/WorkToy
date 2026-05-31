"""
TestTHISCastRecursion subclasses 'OverloadTest' and validates the
behaviour of the dangerous re-entrant recursion failure mode when having
an overloaded constructor that takes 'THIS' as argument.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import time

from worktoy.utilities.combinatorics import Arrangements
from worktoy.waitaminute.dispatch import DispatchException
from . import OverloadTest
from worktoy.core.sentinels import THIS
from worktoy.dispatch import overload
from worktoy.mcls import BaseObject


class Foo(BaseObject):
  """Minimal class exposing a THIS overload on the constructor."""

  slots = ('timeVal',)

  @overload(THIS, THIS, THIS)
  @overload(THIS, str)
  def __init__(self, *_) -> None:
    """Construct a Foo instance from an existing Foo instance and a
    message."""
    self.timeVal = time.perf_counter_ns() % (2 ** 20)

  @overload(THIS)
  def __init__(self, *_) -> None:
    """Copy-construct from an existing Foo instance."""
    self.timeVal = time.perf_counter_ns() % (2 ** 20)

  @overload()
  def __init__(self) -> None:
    """Construct an empty Foo instance."""
    self.timeVal = time.perf_counter_ns() % (2 ** 20)


class Bar(Foo):
  """Subclass used to confirm legitimate subclass copy-construction."""


class TestThisCastRecursion(OverloadTest):
  """Probe the THIS casting-tier recursion behaviour from many angles."""

  def setUp(self) -> None:
    super().setUp()
    self.testArgs = (
      object,
      object(),
      69,
      '420',
      """You feel lucky, punk?"""
    )
    self.perms = (*Arrangements(*self.testArgs, ), ())

  def test_permutations(self, ) -> None:
    """
    This method tests all the permutations of the test arguments in the
    constructor of both Foo and Bar. Those that succeed are allowed to,
    but only 'DispatchException' should be raised.
    """
    for cls in (Foo, Bar):
      for args in self.perms:
        try:
          instance = cls(*args)
        except DispatchException as dispatchException:
          with self.assertRaises(DispatchException):
            raise dispatchException
        else:
          self.assertIsInstance(instance, cls)

  def test_init(self, ) -> None:
    """
    This method covers instantiation of the 'Foo' class.
    """
    emptyFoos = [Foo() for _ in 'foo']
    oneFoos = [Foo(foo) for foo in emptyFoos]
    bar = 'never', 'gonna', 'give'
    strFoos = [Foo(foo, s) for foo, s in zip(oneFoos, bar)]
    bar = 'you', 'up', 'never'
    allFoos = [Foo(*emptyFoos, ) for _ in bar]
    foos = (*emptyFoos, *oneFoos, *strFoos, *allFoos)
    for foo in foos:
      self.assertIsInstance(foo, Foo)

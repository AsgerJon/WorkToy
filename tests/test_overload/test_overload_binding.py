"""
TestOverloadBinding subclasses 'OverloadTest' and pins that an overloaded
method always binds to the object it is read from, under the class that
object currently has. A copy of an instance must run its overloaded
methods against the copy, and an instance whose class is replaced must
run the overloaded methods of its new class.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from copy import copy, deepcopy

from worktoy.desc import AttriBox
from worktoy.dispatch import overload
from worktoy.mcls import BaseObject
from . import OverloadTest


class Counter(BaseObject):
  """Counter keeps a running count that its overloaded 'bump' raises by
  the given step. Each call changes the state of the instance it runs
  against, which exposes the case where a call runs against the wrong
  instance."""

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Public Variables
  count = AttriBox[int](0)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload(int)
  def bump(self, step: int) -> int:
    self.count += step
    return self.count


class Countdown(BaseObject):
  """Countdown shares the layout of 'Counter', but its overloaded 'bump'
  lowers the count instead. An instance of 'Counter' can therefore be
  given this class in place of its own, after which 'bump' must count
  down."""

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Public Variables
  count = AttriBox[int](0)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload(int)
  def bump(self, step: int) -> int:
    self.count -= step
    return self.count


class TestOverloadBinding(OverloadTest):
  """
  TestOverloadBinding pins that overloaded methods bind to the instance
  and class they are read through, even after an earlier call on another
  instance or under another class.
  """

  def test_copy_runs_against_copy(self) -> None:
    """
    Testing that an overloaded call on a shallow copy changes the copy
    and leaves the original alone. The original is called once before
    copying, so anything it keeps from that call is copied along with
    it.
    """
    original = Counter()
    original.bump(1)
    duplicate = copy(original)
    self.assertEqual(duplicate.bump(10), 11)
    self.assertEqual(original.count, 1)
    self.assertEqual(duplicate.count, 11)

  def test_deepcopy_runs_against_copy(self) -> None:
    """
    Testing the same through a deep copy. This already holds, since a
    deep copy also copies anything the original holds on to, but it
    must keep holding whatever the fix for the shallow copy turns out
    to be.
    """
    original = Counter()
    original.bump(1)
    duplicate = deepcopy(original)
    self.assertEqual(duplicate.bump(10), 11)
    self.assertEqual(original.count, 1)
    self.assertEqual(duplicate.count, 11)

  def test_new_class_runs_its_own_overload(self) -> None:
    """
    Testing that an instance given a new class runs the overloaded
    method of that class. The instance is called once under its
    original class first, so anything it keeps from that call is still
    present after the class is replaced.
    """
    counter = Counter()
    self.assertEqual(counter.bump(1), 1)
    counter.__class__ = Countdown
    self.assertEqual(counter.bump(1), 0)

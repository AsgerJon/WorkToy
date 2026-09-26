"""
TestOverloadFootprint subclasses 'OverloadTest' and pins that calling an
overloaded method leaves nothing behind on the instance. An overloaded
method reads like any plain method: each access builds a fresh bound
method, and nothing is stored on the instance. A stored bound method
would add an entry to the instance dictionary. It would also make the
instance refer to itself, so that it outlives its last reference until
the garbage collector happens to run.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import gc
import weakref

from worktoy.dispatch import overload
from worktoy.mcls import BaseObject
from . import OverloadTest


class Greeter(BaseObject):
  """Greeter has an overloaded 'greet' that reads no state and writes
  none, so any change to the instance after a call comes from the
  dispatch machinery itself."""

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload(str)
  def greet(self, name: str) -> str:
    return 'hello %s' % name


class TestOverloadFootprint(OverloadTest):
  """
  TestOverloadFootprint pins that an overloaded call neither adds to the
  instance dictionary nor keeps the instance alive.
  """

  def test_call_leaves_instance_dict_alone(self) -> None:
    """
    Testing that the instance dictionary holds the same entries after
    an overloaded call as before it.
    """
    greeter = Greeter()
    before = {**vars(greeter), }
    self.assertEqual(greeter.greet('world'), 'hello world')
    self.assertEqual(vars(greeter), before)

  def test_instance_freed_without_collector(self) -> None:
    """
    Testing that an instance is freed as soon as its last reference is
    deleted, both before and after it has made an overloaded call. The
    garbage collector is switched off for the duration, so only
    reference counting can free the instance, and a reference cycle
    keeps it alive. The instance that never made a call shows that the
    class itself creates no cycle.
    """
    gc.disable()
    try:
      idle = Greeter()
      idleRef = weakref.ref(idle)
      del idle
      called = Greeter()
      calledRef = weakref.ref(called)
      called.greet('world')
      del called
      self.assertIsNone(idleRef())
      self.assertIsNone(calledRef())
    finally:
      gc.enable()

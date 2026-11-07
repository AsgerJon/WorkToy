"""
TestObjectThreads tests that the frames of 'Object' from 'worktoy.core'
are kept apart between threads.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import threading
from concurrent.futures import ThreadPoolExecutor
from typing import TYPE_CHECKING

from worktoy.core import Object
from . import CoreTest, SlowInstance, SlowHook

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Callable

#  Threads reading at once, and reads made by each.
_THREADS = 8
_READS = 50


class TestObjectThreads(CoreTest):
  """
  The frames of an access belong to the thread making it, even when many
  threads read through the same descriptor at once. The tests pin that
  each read sees its own instance, that no pop meets an empty or foreign
  stack, that two threads reading the same instance at once are not
  taken for a recursive read, and that a new thread starts without the
  frames of the thread starting it. A thread pool carries what each
  thread saw, and any exception, back to the test.
  """

  def _hammer(self, target: Callable[[], bool]) -> list[bool]:
    """Run 'target' in many threads at once and collect what each saw"""
    barrier = threading.Barrier(_THREADS)

    def run() -> bool:
      """Wait for every thread, then call the target repeatedly"""
      barrier.wait()
      return all(target() for _ in range(_READS))

    with ThreadPoolExecutor(_THREADS) as pool:
      futures = [pool.submit(run) for _ in range(_THREADS)]
      return [future.result() for future in futures]

  def test_each_read_sees_its_own_instance(self) -> None:
    class Owner:
      f = SlowInstance()

    def readOwn() -> bool:
      """Read through a fresh instance and tell whether the read saw it"""
      owner = Owner()
      return owner.f is owner

    self.assertEqual(self._hammer(readOwn), [True] * _THREADS)
    self.assertFalse(Owner.f.hasContext())

  def test_same_instance_not_recursive(self) -> None:
    class Owner:
      f = SlowHook()

    shared = Owner()

    def readShared() -> bool:
      """Read through the instance every thread shares"""
      #  Without an '__instance_get__' of its own, the fixture hands
      #  back the descriptor; the hook ran on the way.
      return shared.f is Owner.f

    self.assertEqual(self._hammer(readShared), [True] * _THREADS)
    self.assertEqual(Owner.f.__get_lock__, [])

  def test_new_thread_starts_without_frames(self) -> None:
    desc = Object()
    seen: list[bool] = []

    def look() -> None:
      """Record whether the new thread sees a frame"""
      seen.append(desc.hasContext())

    desc.createContext(1, int)
    try:
      thread = threading.Thread(target=look)
      thread.start()
      thread.join()
      self.assertTrue(desc.hasContext())
    finally:
      desc.exitContext()
    self.assertEqual(seen, [False])

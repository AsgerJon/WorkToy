"""
TestNamespaceThreads tests that class statements running in several
threads at once each keep their own namespace in the hooks.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import threading
from concurrent.futures import ThreadPoolExecutor
from typing import TYPE_CHECKING

from worktoy.dispatch import overload
from worktoy.mcls import BaseObject
from . import MclsTest, SlowSpaceHook, SlowMeta

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Callable

#  Threads building classes at once, and class statements run by each.
_THREADS = 8
_BUILDS = 25


class TestNamespaceThreads(MclsTest):
  """
  One hook object serves every class statement of its namespace class,
  and a phase reads the namespace through 'hook.space'. The tests pin
  that the namespace a hook reads is the one of the class statement
  running in its own thread, even while other threads run theirs, and
  that classes built in threads at once keep the overloads of their
  bodies. A thread pool carries what each thread saw, and any exception,
  back to the test.
  """

  def setUp(self) -> None:
    super().setUp()
    SlowSpaceHook.seen.clear()

  def _hammer(self, target: Callable[[], bool]) -> list[bool]:
    """Run 'target' in many threads at once and collect what each saw"""
    barrier = threading.Barrier(_THREADS)

    def run() -> bool:
      """Wait for every thread, then call the target repeatedly"""
      barrier.wait()
      return all(target() for _ in range(_BUILDS))

    with ThreadPoolExecutor(_THREADS) as pool:
      futures = [pool.submit(run) for _ in range(_THREADS)]
      return [future.result() for future in futures]

  def test_hook_reads_its_own_namespace(self) -> None:
    def build() -> bool:
      """Run one class statement under the slow namespace"""
      class Built(metaclass=SlowMeta):
        """A class whose body runs in a 'SlowSpace'."""

      return Built.__name__ == 'Built'

    self.assertEqual(self._hammer(build), [True] * _THREADS)
    self.assertEqual(len(SlowSpaceHook.seen), _THREADS * _BUILDS)
    self.assertTrue(all(SlowSpaceHook.seen))

  def test_classes_built_at_once_keep_their_overloads(self) -> None:
    def build() -> bool:
      """Build a class with two overloads and tell whether both work"""
      class Built(BaseObject):
        @overload(int)
        def pick(self, value: int) -> str:
          return 'int'

        @overload(str)
        def pick(self, value: str) -> str:
          return 'str'

      built = Built()
      return (built.pick(1), built.pick('a')) == ('int', 'str')

    self.assertEqual(self._hammer(build), [True] * _THREADS)

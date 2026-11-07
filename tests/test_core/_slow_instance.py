"""
SlowInstance is a descriptor that yields to other threads before reading
the instance of its own access.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import time
from typing import TYPE_CHECKING

from worktoy.core import Object

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any


class SlowInstance(Object):
  """
  A stack shared between threads shows its fault only when another
  thread's frame lands on top between the push and the read of the
  instance. 'SlowInstance' makes room for exactly that by yielding the
  processor inside the read, so a test with many threads reading at
  once meets the fault on every run rather than by luck.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  PARENT METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __instance_get__(self, instance: Any, owner: type, **kwargs) -> Any:
    time.sleep(0)
    return self.instance

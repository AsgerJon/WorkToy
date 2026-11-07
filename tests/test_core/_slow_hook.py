"""
SlowHook is a descriptor whose read hook yields to other threads while
it runs.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import time
from typing import TYPE_CHECKING

from worktoy.core import Object

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import Any


class SlowHook(Object):
  """
  A read of an instance while a read hook runs for that instance is
  refused as recursive. Two threads reading the same instance at once
  must not be taken for that, which only shows when the hook of one
  thread is still running as the other arrives. 'SlowHook' holds its
  hook open long enough for the second thread to arrive.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  PARENT METHODS   # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def hookPreGet(self, instance: Any, **kwargs) -> None:
    time.sleep(0.001)

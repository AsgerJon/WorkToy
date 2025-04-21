"""StartupException is raised when a startup task encounters errors. """
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Callable


class StartupException(Exception):
  """StartupException is raised when a startup task encounters errors."""

  __startup_task__ = None
  __task_exception__ = None

  def __init__(self, task: Callable, exception: Exception) -> None:
    """Initialize the StartupException object."""
    self.__startup_task__ = task
    self.__task_exception__ = exception
    info = "Startup task '%s' encountered exception '%s'!"
    Exception.__init__(self, info % (task, exception))

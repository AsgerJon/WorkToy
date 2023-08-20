"""TestError is for testing."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.waitaminute import AbstractError


class TestError(AbstractError):
  """some testing!"""

  def __init__(self, *args, **kwargs) -> None:
    AbstractError.__init__(self, *args, )

  def _getMessage(self) -> str:
    """This is a test error!"""
    return 'LOL'

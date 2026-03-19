"""
TestLoremSample subclasses 'SampleTest' and provides tests for
'LoremSample' from the 'worktoy.work_test.samples' module.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from . import SampleTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Self, Callable, TypeAlias, Union, Optional


class TestLoremSample(SampleTest):
  """
  TestLoremSample provides tests for 'LoremSample' from the
  'worktoy.work_test.samples' module.
  """

  def test_init(self) -> None:
    """
    This method tests instantiation of the 'LoremSample' class.
    """

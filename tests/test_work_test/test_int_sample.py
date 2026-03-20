"""
TestIntSample subclasses 'SampleTest' and provides test cases for the
'IntSample' class.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from . import SampleTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Self, Callable, Never


class TestIntSample(SampleTest):
  """
  TestIntSample provides test cases for the 'IntSample' class.
  """

  def test_init(self, ) -> None:
    """
    This method test the instantiation of the 'IntSample' class.
    """

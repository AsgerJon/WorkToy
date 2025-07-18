"""
TestAlias tests specific functionality of the 'Alias' descriptor not
covered by the contextual tests in 'DescTest'.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from . import DescTest, ComplexAlias

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Dict, Optional


class TestAlias(DescTest):
  """
  TestAlias tests specific functionality of the 'Alias' descriptor not
  covered by the contextual tests in 'DescTest'.
  """

  def test_delete(self, ) -> None:
    """Test that deleting an alias works as expected."""
    z = ComplexAlias(1.0, 2.0)

    del z.x

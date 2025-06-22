"""
TestDataField tests the EZData entries of class DataField from the
'worktoy.ez_data' module.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.ezdata import DataField, EZData, EZMeta

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Self


class TestDataField(TestCase):
  """
  TestDataField tests the EZData entries of class DataField from the
  'worktoy.ez_data' module.
  """

  def test_init(self) -> None:
    """
    Tests that 'DataField' can be instantiated.
    """
    strField = DataField('key', str, 'key')
    intField = DataField('index', int, 69)

  def test_str(self, ) -> None:
    """
    Test the output of DataField.__str__
    """

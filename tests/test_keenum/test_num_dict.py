"""
TestNumDict tests that KeeNum enumerations can be used as dictionary keys.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.keenum import KeeNum
from . import KeeTest
from .examples import RGBNum

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestNumDict(KeeTest):
  """
  TestNumDict tests that KeeNum enumerations can be used as dictionary keys.
  """

  def setUp(self) -> None:
    self.colorDict = {num: str.capitalize(num.name) for num in RGBNum}

  def test_num_dict(self, ) -> None:
    """Test that KeeNum enumerations can be used as dictionary keys. """
    for keenum in RGBNum.mroNum:
      for num in keenum:
        self.assertIn(num, self.colorDict)
        self.assertEqual(self.colorDict[num], str.capitalize(num.name))

    for key, val in self.colorDict.items():
      self.assertIsInstance(key, KeeNum)
      self.assertIsInstance(val, str)
      self.assertEqual(val, str.capitalize(key.name))


"""PYTHONDONTWRITEBYTECODE=1"""

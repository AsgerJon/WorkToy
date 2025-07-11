"""
TestEZUmbrella covers the more esoteric lines of code in the ezdata module.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

import builtins

from worktoy.mcls import AbstractMetaclass
from . import EZTest, baseValues
from typing import TYPE_CHECKING

from worktoy.ezdata import EZData

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Type


class RGB(EZData):
  red: int
  green: int
  blue: int


class TestEZUmbrella(EZTest):
  """
  TestEZUmbrella covers the more esoteric lines of code in the ezdata module.
  """

  def test_rgb(self) -> None:
    """
    Test the RGB class to ensure it works as expected.
    """

    class LOL(metaclass=AbstractMetaclass):
      """
      A class that uses the AbstractMetaclass to ensure it is an abstract
      class.
      """
      pass

    self.assertIsInstance(LOL, AbstractMetaclass)
    self.assertIsSubclass(LOL, object)
    lmao = [*baseValues, ]
    for item in self.getBaseValues():
      self.assertEqual(item, lmao.pop(0))

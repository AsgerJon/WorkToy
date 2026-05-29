"""KeeTest provides a common test class for the 'tests.test_keenum'
module."""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.work_test import BaseTest
from .examples import FlagsExample, SubclassExample, ChessPieceNum
from .examples import PrimeNum, CurrencyNum, PlanetNum, ElementNum
from .examples import CurrencyData, PlanetData, ElementData
from .examples import NobleGasNum, NetworkPortNum
from .examples import VAlignum, HAlignum, HTTPStatus
from .examples import FileAccess, KeyboardModifier
from .examples import RootRGB, MoreRGB, EvenMoreRGB, RGBNum, Month, WeekDay

if TYPE_CHECKING:  # pragma: no cover
  pass


class KeeTest(BaseTest):
  """KeeTest provides a common test class for the 'tests.test_keenum'
  module. """

  def setUp(self, ) -> None:
    self.exampleFlags = [
      FlagsExample,
      FileAccess,
      KeyboardModifier,
      SubclassExample,
    ]
    self.exampleNums = [
      RootRGB, MoreRGB, EvenMoreRGB, RGBNum, Month, WeekDay,
    ]
    self.colorNums = (RootRGB, MoreRGB, EvenMoreRGB, RGBNum)

    self.allNums = (
      HAlignum,
      VAlignum,
      WeekDay,
      Month,
      HTTPStatus,
      RootRGB,
      MoreRGB,
      EvenMoreRGB,
      RGBNum,
      ChessPieceNum,
      NobleGasNum,
      NetworkPortNum,
      PrimeNum,
    )

    self.baseNums = (
      HAlignum,
      VAlignum,
      WeekDay,
      Month,
      RootRGB,
      MoreRGB,
      EvenMoreRGB,
      RGBNum,
      ChessPieceNum,
      NobleGasNum,
      NetworkPortNum,
      PrimeNum,
    )

    self.classResolveNums = (
      CurrencyNum,
      PlanetNum,
      ElementNum,
    )

    self.classResolveData = (
      CurrencyData,
      PlanetData,
      ElementData,
    )

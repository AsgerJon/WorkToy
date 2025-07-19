"""
TestLoad tests the NumLoad scenario for overloading with KeeNum classes.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from . import NumLoad, OverloadTest, WeekNum, FlagRoll

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Self


class TestLoad(OverloadTest):
  """
  TestLoad tests the NumLoad scenario for overloading with KeeNum classes.
  """

  def test_init(self) -> Self:
    """Tests the initialization of the TestLoad class."""

    strArg = 'breh'
    numArg = WeekNum.TUESDAY
    flagArg = FlagRoll[13]
    strNumArg = strArg, numArg
    strFlagArg = strArg, flagArg
    strNumFlagArg = strArg, numArg, flagArg
    args = (
        (strArg,),
        (numArg,),
        (flagArg,),
        strNumArg,
        strFlagArg,
        strNumFlagArg,
        (FlagRoll.NULL, WeekNum.FRIDAY),
        (WeekNum.SATURDAY, FlagRoll[7]),
        (WeekNum.SUNDAY, 'lmao'),
        (FlagRoll[9], 'yeet'),
    )
    for arg in args:
      numLoad = NumLoad(*arg, )
      expected = numLoad.loaded
      actual = str(arg)
      self.assertIn(expected, actual)

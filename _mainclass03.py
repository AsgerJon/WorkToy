"""Testing CallMeMaybe"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from icecream import ic

from worktoy.worktype import CallMeMaybe

ic.configureOutput(includeContext=True)


class YOLO:
  """BLABLABLA"""

  bla = CallMeMaybe(lambda x: x)

  @CallMeMaybe
  def cunt(self) -> None:
    """LOL"""
    print('cunts')

  def __init__(self, *args, **kwargs) -> None:
    pass

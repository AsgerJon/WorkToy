"""LMAO"""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from main_tester_script_02 import Float
from worktoy.desc import AttriBox
from worktoy.ezdata import EZData


class SpacePoint(EZData):
  """YOLO"""

  x = AttriBox[float]()
  y = AttriBox[float]()
  z = AttriBox[float]()

  bla = AttriBox[Float]()
  lmao = AttriBox[Float]()

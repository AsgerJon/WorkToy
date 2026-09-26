"""
Testing more stupid typing stuff!!
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from main_tester_00 import Box
from worktoy.desc import AttriBox


class Bar:
  good = Box[int]
  cunt = good.__call__
  bad = AttriBox[int](420)


class Trolololo:
  def __new__(cls, *__, **_) -> object:
    return """u mad bro?"""

"""TypeField subclasses Constant providing a field specially for type"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.field import Constant


class TypeField(Constant):
  """TypeField subclasses Constant providing a field specially for type"""

  def __init__(self, type_: type = None) -> None:
    Constant.__init__(self, type_)

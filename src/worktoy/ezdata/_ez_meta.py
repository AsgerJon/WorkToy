"""EZMeta provides the metaclass used by the 'EZData' class. This metaclass
provides the functionality of the 'EZData' class."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.base import FastMeta, FastSpace
from worktoy.ezdata import EZSpace
from worktoy.meta import Bases, AbstractNamespace

Space = EZSpace


class EZMeta(FastMeta):
  """EZMeta provides the metaclass used by the 'EZData' class. This metaclass
  provides the functionality of the 'EZData' class."""

  @classmethod
  def __prepare__(mcls, name: str, bases: Bases, **kwargs) -> Space:
    return Space(mcls, name, bases, **kwargs)

  def __new__(mcls, name: str, bases: Bases, space: Space, **kwargs) -> type:
    for line in space.getLines():
      print(line)
    return FastMeta.__new__(mcls, name, bases, space, **kwargs)

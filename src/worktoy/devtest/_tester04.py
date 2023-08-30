"""Tester"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from icecream import ic

from worktoy.fields import LabelField, ConstLabelField
from worktoy.metaclass import WorkToyBase


class Test(WorkToyBase):
  """LMAO"""

  labelTest = LabelField('LMAO')

  titleField = ConstLabelField('TITLE!')

  def __init__(self, *args, **kwargs) -> None:
    pass

  def __getattr__(self, key: str) -> object:
    ic(self, key)
    cls = object.__getattribute__(self, '__class__')
    return object.__getattribute__(cls, key)

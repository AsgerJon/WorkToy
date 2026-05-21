"""
RichData subclasses 'EZData' and provides an example of an 'EZData'
subclass that has methods and a descriptor in addition to the single
'EZField' attribute.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.desc import Field
from worktoy.ezdata import EZData, EZField

if TYPE_CHECKING:  # pragma: no cover
  pass


class RichData(EZData):
  value: EZField[float] = .69  # Replaced by 'EZHook'

  valueFormat: Field[str] = Field()

  def __float__(self, ) -> float:
    return self.value

  def __int__(self, ) -> int:
    return int(round(float(self)))

  @valueFormat.GET
  def _getValueFormat(self, ) -> str:
    digitPlaces = 0
    val = float(self)
    while not float.is_integer(val):
      digitPlaces += 1
      val *= 10
    if not digitPlaces:
      return str(int(self))
    infoSpecSpec = """%%.%df"""
    infoSpec = infoSpecSpec % digitPlaces
    return infoSpec % float(self)

  def __str__(self, ) -> str:
    return self.valueFormat

  def __repr__(self, ) -> str:
    infoSpec = """%s(%f)"""
    clsName = type(self).__name__
    return infoSpec % (clsName, self.value)

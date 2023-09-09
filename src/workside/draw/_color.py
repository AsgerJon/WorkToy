"""WorkSide - Draw - Color"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtGui import QColor

from worktoy.base import DefaultClass
from worktoy.fields import IntAttribute


class Color(DefaultClass):
  """WorkSide - Settings - Styles - Color"""

  alpha = IntAttribute(255)
  red = IntAttribute(255)
  green = IntAttribute(255)
  blue = IntAttribute(0)

  @classmethod
  def getDefaultInstance(cls) -> Color:
    """Getter-function for default instance"""
    defaultInstance = cls(255, 255, 255, 0)
    return defaultInstance

  def __init__(self, *args, **kwargs) -> None:
    DefaultClass.__init__(self, *args, **kwargs)
    redKwarg = self.maybeKey(int, 'red', **kwargs)
    greenKwarg = self.maybeKey(int, 'green', **kwargs)
    blueKwarg = self.maybeKey(int, 'blue', **kwargs)
    alphaKwarg = self.maybeKey(int, 'alpha', **kwargs)
    rgba = self.maybeTypes(int, padChar=None, pad=4)
    redArg, greenArg, blueArg, alphaArg = rgba
    defaultValues = 255, 255, 255, 0
    redDefault, greenDefault, blueDefault, alphaDefault = defaultValues
    self.red = self.maybe(redKwarg, redArg, redDefault)
    self.green = self.maybe(greenKwarg, greenArg, greenDefault)
    self.blue = self.maybe(blueKwarg, blueArg, blueDefault)
    self.alpha = self.maybe(alphaKwarg, alphaArg, alphaDefault)

  def asQColor(self) -> QColor:
    """Returns QColor representation"""
    return QColor(self.red, self.green, self.blue, self.alpha)

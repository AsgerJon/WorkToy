"""WorkSide - Style - RGB
Base class defining the red, green and blue color space."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtGui import QColor

from worktoy.fields import IntField, AbstractField
from worktoy.sym import BaseSym, SYM


class RGB(BaseSym):
  """WorkSide - Style - RGB
  Base class defining the red, green and blue color space."""

  R = IntField(127)
  G = IntField(255)
  B = IntField(0)

  def asQColor(self) -> QColor:
    """Converts to instance of QColor."""
    return QColor(self.R, self.G, self.B)

  white = SYM.auto()
  white.R = 255
  white.G = 255
  white.B = 255

  black = SYM.auto()
  black.R = 0
  black.G = 0
  black.B = 0

  red = SYM.auto()
  red.R = 255
  red.G = 0
  red.B = 0

  green = SYM.auto()
  green.R = 0
  green.G = 255
  green.B = 0

  blue = SYM.auto()
  blue.R = 0
  blue.G = 0
  blue.B = 255

  yellow = SYM.auto()
  yellow.R = 255
  yellow.G = 255
  yellow.B = 0

  magenta = SYM.auto()
  magenta.R = 255
  magenta.G = 0
  magenta.B = 255

  Aqua = SYM.auto()
  Aqua.R = 0
  Aqua.G = 255
  Aqua.B = 255

  orange = SYM.auto()
  orange.R = 255
  orange.G = 127
  orange.B = 0

  cyan = SYM.auto()
  cyan.R = 0
  cyan.G = 255
  cyan.B = 127

  violet = SYM.auto()
  violet.R = 127
  violet.G = 0
  violet.B = 255

  lime = SYM.auto()
  lime.R = 127
  lime.G = 255
  lime.B = 0

  dodgerBlue = SYM.auto()
  dodgerBlue.R = 0
  dodgerBlue.G = 127
  dodgerBlue.B = 255

  pink = SYM.auto()
  pink.R = 255
  pink.G = 0
  pink.B = 127


class RGBField(AbstractField):
  """Implementation of RGB class as a field"""

  def __init__(self, *rgb, **kwargs) -> None:
    defVal = RGB.white
    AbstractField.__init__(self, defVal, **kwargs)

  def getFieldSource(self) -> type:
    """Integer"""
    return RGB

  def getPermissionLevel(self) -> int:
    """Protected. """
    return 2

  def explicitSetter(self, obj: object, newValue: RGB) -> None:
    """Explicit setter function. Tries to find the _set[NAME] method on
    the object."""
    return setattr(obj, self.getPrivateName(), newValue)

  def explicitGetter(self, obj: object, cls: type) -> RGB:
    return AbstractField.explicitGetter(self, obj, cls)

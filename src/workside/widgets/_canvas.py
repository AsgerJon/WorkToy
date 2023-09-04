"""WorkSide - Widgets - Canvas
The canvas allows other widgets to anchor themselves to it ."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
from typing import Any

from workside.widgets import CoreWidget


class Canvas(CoreWidget):
  """WorkSide - Widgets - Canvas
  The canvas allows other widgets to anchor themselves to it."""

  def __init__(self, *args, **kwargs) -> None:
    CoreWidget.__init__(self, *args, **kwargs)

  @abstractmethod
  def computeRequiredSize(self, *args, **kwargs) -> Any:
    """Method responsible for determining what size is necessary for this
    widget instance of the widget."""

  def sizeControl(self, *args, **kwargs) -> None:
    """Implementation of the size control. """
    self.setFixedSize(self.computeRequiredSize(*args, **kwargs))

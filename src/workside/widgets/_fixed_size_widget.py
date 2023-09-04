"""WorkSide - Widgets - FixedSizeWidget
Subclass of the core widget implementing a fixed size. This size is
computed at instance creation time and then remains fixed."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
from typing import Any

from workside.widgets import CoreWidget


class FixedSizeWidget(CoreWidget):
  """WorkSide - Widgets - FixedSizeWidget
  Subclass of the core widget implementing a fixed size. This size is
  computed at instance creation time and then remains fixed."""

  def __init__(self, *args, **kwargs) -> None:
    CoreWidget.__init__(self, *args, **kwargs)

  @abstractmethod
  def computeRequiredSize(self, *args, **kwargs) -> Any:
    """Method responsible for determining what size is necessary for this
    widget instance of the widget."""

  @abstractmethod
  def sizeControl(self, *args, **kwargs, ) -> None:
    """Implementation of the size control. """
    self.setFixedSize(self.computeRequiredSize(*args, **kwargs))

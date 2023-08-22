"""WorkSide - MetaSide - WidgetNameSpace
This class provides the namespace class for use by the widget class
creation system."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy import AbstractNameSpace


class WidgetNameSpace(AbstractNameSpace):
  """WorkSide - MetaSide - WidgetNameSpace
  This class provides the namespace class for use by the widget class
  creation system."""

  def __init__(self, *args, **kwargs) -> None:
    AbstractNameSpace.__init__(self, *args, **kwargs)

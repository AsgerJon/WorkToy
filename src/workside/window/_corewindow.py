"""WorkToy - Window - CoreWindow
This class provides the core window class which implements the menubars,
menus and actions."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from workside.metaside import BaseWindow


class CoreWindow(BaseWindow):
  """WorkToy - Window - CoreWindow
  This class provides the core window class which implements the menubars,
  menus and actions."""

  def __init__(self, *args, **kwargs) -> None:
    BaseWindow.__init__(self, *args, **kwargs)

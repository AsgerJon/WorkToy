"""WorkSide - Window - MainWindow
Top level window class. This class should provide the logic occurring in
the main application window."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from workside.window import LayoutWindow


class MainWindow(LayoutWindow):
  """WorkSide - MainWindow"""

  def __init__(self, *args, **kwargs) -> None:
    LayoutWindow.__init__(self, *args, **kwargs)
    self.setWindowTitle('MineSide | Qt and Minescript')

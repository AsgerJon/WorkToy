"""Main Tester Script"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

import os
import sys
import time
from typing import NoReturn, Never, Any, Union

from PySide6.QtWidgets import QApplication
from icecream import ic
from pyperclip import copy

from workside.windows import MainWindow

# from worktoy.descriptors import FieldClass, FieldInstance
# from worktoy.settings import AlignLeft, AlignTop

ic.configureOutput(includeContext=True)
Number = Union[int, float]


def tester00() -> NoReturn:
  """Hello World!"""
  stuff = ['hello world', os, sys, Never, Any, ]
  stuff = [*stuff, time, ]
  for item in stuff:
    ic(item)


def tester01() -> None:
  """FUCK"""

  app = QApplication(sys.argv)
  window = MainWindow()
  window.show()
  sys.exit(app.exec())


def tester02() -> None:
  """CUNT"""


if __name__ == '__main__':
  print(77 * '_')
  timeLine = time.ctime()
  print(len(timeLine) * '.')
  print(timeLine)
  print(len(timeLine) * '~')

  tester01()

  print(len(timeLine) * '~')
  print(timeLine)
  print(len(timeLine) * '.')
  print(77 * '¨')

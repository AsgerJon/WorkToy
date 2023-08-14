"""DIOError exceptions are raised by functions in the dio module."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations


class DIOError(Exception):
  """DIOError exceptions are raised by functions in the dio module.
  #  Copyright (c) 2023 Asger Jon Vistisen
  #  MIT Licence"""

  def __init__(self, *args, ) -> None:
    Exception.__init__(self, *args, )

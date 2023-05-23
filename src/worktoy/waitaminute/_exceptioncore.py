"""ExceptionCore implements basic error/warning functionality."""
#  MIT License
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from icecream import ic

ic.configureOutput(includeContext=True)


class ExceptionCore(Exception, ):
  """ExceptionCore implements basic error/warning functionality. To set a
  Custom message, reimplement the _createMsg method.
  #  MIT License
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  def __init__(self, *args, **kwargs) -> None:
    Exception.__init__(self, self._createMsg(*args, **kwargs))

  def _createMsg(self, *args, **kwargs) -> str:
    """This method creates the message displayed. Reimplement in subclass."""
    self._msg = Exception.__str__(self)
    return self._msg

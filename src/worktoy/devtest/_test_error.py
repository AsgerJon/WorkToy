"""WorkToy - Wait A Minute - TestError
For testing."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

import inspect
from inspect import FrameInfo

from worktoy.core import Function
from worktoy.waitaminute import MetaXcept


class TestError(MetaXcept):
  """WorkToy - Wait A Minute - TestError
  For testing."""

  def __init__(self, func: Function = None, *args, **kwargs) -> None:
    MetaXcept.__init__(self, *args, **kwargs)
    self._func = self.maybe(func, lambda: None)

  def cunt01(self) -> str:
    """String Representation"""
    __func__ = True if hasattr(self._func, '__func__') else False
    func = getattr(self._func, '__func__', self._func)
    funcQualName = getattr(func, '__qualname__', None)
    funcName = getattr(func, '__name__', None)
    funcPrintF = '%s' % func
    funcStr = self.maybe(funcQualName, funcName, funcPrintF)
    note = 'with __func__' if __func__ else 'without __func__'
    msg = """<br>%s<br>%s<br>""" % (note, funcStr)
    return self.monoSpace(msg)

  def cunt02(self) -> list[FrameInfo]:
    """String Representation"""

    # inspect.stack()[1].function

    return inspect.stack()

    msg = '%s<br>' % type(STACK)
    for frame in STACK:
      msg += ('<br>--> %s' % type(frame))

      # for item in frame:
      #   print(type(item))
      #   msg += ('<br>--> %s' % item)

    return self.monoSpace(msg)

  def __str__(self) -> str:
    """String Representation"""
    print(self.getStack()[-1])
    return 'cunt'

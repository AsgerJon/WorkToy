"""WorkToy - Tester - Decorators
FUCK YOU!"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

import os
import time

from icecream import ic

from worktoy.core import DefaultClass

ic.configureOutput(includeContext=True)


class ClassCallBack(DefaultClass):
  """CUNTS"""

  def __init__(self, cls: type, *args, **kwargs) -> None:
    DefaultClass.__init__(self, *args, **kwargs)

    self._wrappedClass = None
    text = self._setWrappedClass(cls)
    here = os.path.dirname(__file__)
    there = os.path.join(here, 'testfiles', )
    num = int(time.time()) % (2 ** 16 - 1)
    fileName = 'testdata_%d.txt' % num
    filePath = os.path.join(there, fileName)
    print(filePath)
    with open(filePath, 'w') as f:
      f.write(text)

  def __call__(self, *args, **kwargs) -> object:
    return self._setWrappedClass()

  def _setWrappedClass(self, cls: type = None) -> str:
    out = []
    self._wrappedClass = cls
    for base in (*cls.__mro__,):
      baseName = getattr(base, '__qualname__', str(base))

      sides = (64 - 4 - len(str(baseName))) // 2
      side = '*' * sides
      header = '| %s< %s >%s |' % (side, baseName, side)
      out.append(header)
      for (i, (key, val)) in enumerate(base.__dict__.items()):
        keyName = ('%18s' % key)[:17]
        typeName = getattr(type(val), '__qualname__', str(type(val)))
        clsName = ('%30s' % typeName)[:30]
        out.append('%s | %s | %15s' % (keyName, clsName, baseName))
    return '\n'.join(out)

  def leftAlignment(self, text: str, lineLength: int = None) -> str:
    """Aligns text to left"""
    lineLength = self.maybe(lineLength, 77)

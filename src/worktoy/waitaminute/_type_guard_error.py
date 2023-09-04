"""WorkToy - Wait A Minute! - TypeGuardError
Exception raised by a variable not passing a TypeGuard test."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

import inspect
from typing import Any

from icecream import ic

from worktoy.guards import TypeGuard
from worktoy.waitaminute import MetaXcept

from inspect import FrameInfo, stack

ic.configureOutput(includeContext=True)


class TypeGuardError(MetaXcept):
  """WorkToy - Wait A Minute! - TypeGuardError
  Exception raised by a variable not passing a TypeGuard test."""

  def __init__(self, val: Any, guard: TypeGuard,
               *args, **kwargs) -> None:
    MetaXcept.__init__(self, val, *args, **kwargs)
    self._val = val
    self._valType = type(val)
    self._valTypeName = getattr(self._valType, '__qualname__', None)
    self._guard = guard

  def __str__(self, ) -> str:
    header = MetaXcept.__str__(self)
    body = """Received variable of type '[%s]', but expected one of:"""
    body = body % self._valTypeName
    typeList = self._guard.getAllowableTypes()
    typeNameList = ['----\'[%s]\'' % i.__qualname__ for i in typeList]
    typeNameList = [self.monoSpace(i) for i in typeNameList]
    bullets = '<br>'.join(typeNameList)
    msg = '<br>'.join([body, bullets])
    out = '%s\n%s' % (header, self.justify(msg))
    return out.replace('----', '  - ')

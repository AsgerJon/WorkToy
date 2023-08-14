"""The maybeType function finds the first argument of a particular type"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
  from worktoy.typetools import Any


def maybeType(type_: type, *args) -> Any:
  """The maybeType function finds the first argument of a particular type
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""
  if type_.__name__ == 'Any':
    return None if not args else args[0]
  for arg in args:
    if arg is not None:
      if isinstance(arg, type_):
        return typing.cast(Any, arg)
  return typing.cast(Any, None)

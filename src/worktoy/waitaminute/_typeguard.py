"""The typeGuard function raises an error in case of mismatch between
argument and type"""
#  Copyright (c) 2023 Asger Jon Vistisen
#  MIT Licence
from __future__ import annotations

from typing import Any

from worktoy.waitaminute import WrongTypeError


def typeGuard(arg: Any, type_: type) -> Any:
  """The typeGuard function raises an error in case of mismatch between
  argument and type
  #  Copyright (c) 2023 Asger Jon Vistisen
  #  MIT Licence"""
  if isinstance(arg, type_):
    return arg
  raise WrongTypeError(arg, type_)

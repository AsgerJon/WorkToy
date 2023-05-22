"""The extractArg function collects an argument from args and kwargs and
returns a tuple with the extracted argument and the remaining args and
kwargs. For example:
  myType: type
  myKeys: tuple[str]
  myArg, newArgs, newKwargs = extractArg(myType, myKeys, *args, **kwargs)
"""
#  MIT License
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import TypeAlias, Union, Any

from worktoy.core import Kwargs, Args

KEYS: TypeAlias = Union[tuple[str, ...], list[str], str]
EXTRACTED: TypeAlias = Union[Any, Args, Kwargs]


def extractArg(type_: type, keys: KEYS, *args, **kwargs) -> EXTRACTED:
  """The extractArg function collects an argument from args and kwargs and
  returns a tuple with the extracted argument and the remaining args and
  kwargs. For example:
    myType: type
    myKeys: tuple[str]
    myArg, newArgs, newKwargs = extractArg(myType, myKeys, *args, **kwargs)
  #  Copyright (c) 2023 Asger Jon Vistisen
  #  MIT Licence"""
  if isinstance(keys, str):
    keys = [keys, ]
  out = None
  newArgs, newKwargs = [], {}
  for (key, val) in kwargs.items():
    if key in keys and isinstance(val, type_) and out is None:
      out = val
    else:
      newKwargs |= {key: val}
  for item in args:
    if isinstance(item, type_) and out is None:
      out = item
    else:
      newArgs.append(item)
  return (out, newArgs, newKwargs)

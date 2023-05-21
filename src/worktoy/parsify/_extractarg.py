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
from worktoy.typify import Kwargs, Args
from worktoy.parsify import searchKeys, maybeType, maybe

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
    keys = (keys,)
  extractKwarg = searchKeys(*keys) @ type_ >> kwargs
  extractPosArg = maybeType(type_, *args)
  extractDefault = None
  extract = maybe(extractKwarg, extractPosArg, extractDefault, None)
  newKwargs, newArgs = None, None
  if extract in kwargs.values():
    newKwargs = {k: v for (k, v) in kwargs.items() if v != extract}
  elif extract in args:
    newArgs = [arg for arg in args if arg != extract]
  newKwargs = maybe(newKwargs, kwargs)
  newArgs = maybe(newArgs, args)
  return (extract, newArgs, newKwargs)

"""The unStupid function takes the actual types out of typing Unions"""
#  Copyright (c) 2023 Asger Jon Vistisen
#  MIT Licence
from __future__ import annotations

import typing

from icecream import ic

_GenericAlias = getattr(typing, '_GenericAlias')

union = getattr(typing, '_UnionGenericAlias', None)

ic.configureOutput(includeContext=True)


# genericAlias = getattr(typing, 'GenericAlias', None)


def _typeGuard(typeFail: union) -> union:
  """Ensures the right types are here"""
  if isinstance(typeFail, _GenericAlias):
    return typeFail
  if getattr(typeFail, '__origin__', None) is union:
    return typeFail
  return False


def unStupid(typeFail: typing.Union) -> list[type]:
  """The unStupid function takes the actual types out of typing Unions
  #  Copyright (c) 2023 Asger Jon Vistisen
  #  MIT Licence"""
  if not _typeGuard(typeFail):
    return []
  return typeFail.__args__


def unPack(*types, ) -> list[type]:
  """The unPack function takes a collection of arguments and collects the
  unions and the types. Then it recursively replaces union with their
  types until it can return a list containing only types."""
  out = []
  for type_ in types:
    if isinstance(type_, type):
      out.append(type_)
    elif isinstance(type_, union):
      out.append((*unStupid(type_),))
    elif isinstance(type_, (list, tuple)):
      for t in type_:
        if isinstance(t, (type, union, list, tuple)):
          out.append(t)

  if any([isinstance(t, (union, list, tuple)) for t in out]):
    return unPack(*out)
  return out

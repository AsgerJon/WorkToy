"""The typeGuard function raises an error in case of mismatch between
argument and type"""
#  Copyright (c) 2023 Asger Jon Vistisen
#  MIT Licence
from __future__ import annotations

from types import GenericAlias
from typing import Any
import typing

from worktoy.core import unStupid, TypeBagParent
from worktoy.waitaminute import WrongTypeError, TypeGuardError

from icecream import ic

ic.configureOutput(includeContext=True)

Union = getattr(typing, '_UnionGenericAlias', None)
if Union is None:
  raise ImportError('Failed to import union')


def typeGuard(test: Any, *args: Any) -> Any:
  """The typeGuard function raises an error in case of mismatch between
  argument and type
  #  Copyright (c) 2023 Asger Jon Vistisen
  #  MIT Licence"""
  newTypes, newUnions = [], []

  for arg in args:
    if isinstance(arg, type):
      newTypes.append(arg)
    if isinstance(arg, Union):
      newUnions.append(arg)
  for union in newUnions:
    for type_ in unStupid(union):
      newTypes.append(type_)
  for type_ in newTypes:
    if isinstance(test, type_):
      return test
  if isinstance(test, TypeBagParent):
    if type in newTypes:
      return test

  print(77 * '_')
  ic(test)
  ic(newTypes)
  input('fuck you')
  raise TypeGuardError(test, newTypes)

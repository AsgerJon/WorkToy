"""The 'maybeType' function receives a type followed by any number of
positional arguments. The function returns the first argument that is an
instance of the given type. The first argument may be a type, a tuple or
list of types, a string or a tuple or list of strings. When strings are
used (not recommended), the function matches the '__name__' attribute of
the types of the arguments.
"""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from icecream import ic


def maybeType(*args) -> Any:
  """The 'maybeType' function receives a type followed by any number of
  positional arguments. The function returns the first argument that is an
  instance of the given type. The first argument may be a type, a tuple or
  list of types, a string or a tuple or list of strings. When strings are
  used (not recommended), the function matches the '__name__' attribute of
  the types of the arguments. """

  if not args:
    return None

  if isinstance(args[0], type):
    return _maybeType(args[0], *args[1:])

  if isinstance(args[0], str):
    return _maybeTypeName(args[0], *args[1:])

  if isinstance(args[0], (tuple, list)):
    if len(args[0]) == 0:
      return None
    for type_ in args[0]:
      val = None
      if isinstance(type_, type):
        val = _maybeType(type_, *args[1:])
        if val is not None:
          return val
      if isinstance(type_, str):
        val = _maybeTypeName(type_, *args[1:])
      if val is not None:
        return val


def _maybeTypeName(typeName: str, *args) -> Any:
  """This private function uses the '__name__' attribute of the types of the
  arguments to match the given type name."""
  for arg in args:
    if arg.__class__.__name__ == typeName:
      return arg


def _maybeType(type_: type, *args) -> Any:
  """This private function matches the given type."""
  for arg in args:
    if isinstance(arg, type_):
      return arg

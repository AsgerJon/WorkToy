"""
Nuthin much happenin here!
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

import builtins

from worktoy.waitaminute import MetaclassException, TypeException

oldBuild = builtins.__build_class__


def _resolveMetaclass(func, name, *args, **kwargs) -> type:
  """
  Finds the metaclass in the given arguments.
  """
  mcls = type
  if 'metaclass' in kwargs:
    mcls = kwargs['metaclass']
  elif args:
    if isinstance(args[0], type):
      mcls = type(args[0])
  if isinstance(mcls, type):
    return mcls
  raise TypeException('metaclass', mcls, type)


def _resolveBases(func, name, *args, **kwargs) -> tuple[type, ...]:
  """
  Finds the bases in the given arguments.
  """
  return args


def _validateMetaclass(mcls, name, *bases, ) -> None:
  """
  Validates that each base derives from the metaclass or a subclass of it.
  """
  for base in bases:
    meta = type(base)
    if meta is mcls or issubclass(meta, mcls):
      continue
    raise MetaclassException(mcls, name, base)


def newBuild(func, name, *args, **kwargs):
  """A new build function that does nothing."""
  try:
    cls = oldBuild(func, name, *args, **kwargs)
  except TypeError as typeError:
    try:
      mcls = _resolveMetaclass(func, name, *args, **kwargs)
      bases = _resolveBases(func, name, *args, **kwargs)
      _validateMetaclass(mcls, name, *bases)
    except MetaclassException as mce:
      raise mce from typeError
    else:
      raise typeError
  else:
    return cls
  finally:
    pass


builtins.__build_class__ = newBuild

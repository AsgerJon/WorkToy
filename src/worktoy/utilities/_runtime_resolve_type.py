"""
The 'runtimeResolveType' function receives the name of a type and attempts
to resolve it at runtime.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

import os
import sys
import builtins

from icecream import ic

ic.configureOutput(includeContext=True, )


def runtimeResolveType(typeName: str, *_checked: str) -> type:
  """
  Attempts to resolve and return the type object named by 'typeName'
  at runtime.

  This function recursively searches through the namespaces of loaded
  modules to locate the requested type by name.

  Parameters
  ----------
  typeName : str
    The name of the type (usually a class) to resolve.

  *_checked : str
    Private parameter used internally. Callers should not pass any
    arguments here.

  Returns
  -------
  type
    The resolved type object corresponding to 'typeName'.

  Raises
  ------
  ImportError
    If the type cannot be found in any accessible module namespace.

  Notes
  -----
  This function is designed for resolving types stored as string
  annotations, such as those produced when using
  'from __future__ import annotations' or encountered in runtime
  reflection scenarios.

  It is robust against circular references between modules and does
  not execute or evaluate arbitrary code, relying only on module
  namespaces. For most use-cases, 'typeName' should refer to a class
  that is already imported somewhere in the program.

  """
  if hasattr(builtins, typeName):
    return getattr(builtins, typeName)
  frozenGlobals = {**globals(), }
  if typeName in frozenGlobals:
    return frozenGlobals[typeName]
  ic(__name__)
  ic(__file__)
  ic(sys.modules['__main__'])
  ic(os.getcwd())

  raise NameError(typeName)

  exceptions = []
  mod = [*_checked, '__main__'][-1]
  if mod not in sys.modules:
    infoSpec = """Module '%s' not found. """
    info = infoSpec % mod
    raise ImportError(info)
  if typeName in sys.modules[mod].__dict__:
    return sys.modules[mod].__dict__[typeName]
  for key, val in sys.modules[mod].__dict__.items():
    if hasattr(val, '__module__'):
      if val.__module__ in _checked:
        continue
      try:
        type_ = runtimeResolveType(typeName, *_checked, val.__module__)
      except ImportError as importError:
        exceptions.append(importError)
        print(val.__module__)
        continue
      else:
        return type_
  else:
    infoSpec = """Type '%s' not found in module '%s'. """
    info = infoSpec % (typeName, mod)
    raise ImportError(info)

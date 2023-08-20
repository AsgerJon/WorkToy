"""This applies the new module"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations


def _applyImports() -> bool:
  """Augments the imports"""
  import builtins
  from ._customimport import customImport

  builtins.__import__ = customImport
  return True


ready = _applyImports()

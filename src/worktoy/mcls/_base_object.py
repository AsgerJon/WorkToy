"""
BaseObject is the standard entry point for using the worktoy library.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from . import BaseMeta
from ..static import AbstractObject

try:
  from typing import TYPE_CHECKING
except ImportError:  # pragma: no cover
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False


class BaseObject(AbstractObject, metaclass=BaseMeta):
  """
  BaseObject combines the core functionality of AbstractObject with the
  hook-based metaclass behavior of BaseMeta.

  From AbstractObject, it inherits robust constructor handling, controlled
  descriptor mutation, and context-aware access to instance and owner
  information. From BaseMeta, it gains support for function overloading
  and other hook-based class construction features via BaseSpace.

  Subclass this when you want both: sane, safe object semantics and
  overload-aware metaclass support.
  """
  pass

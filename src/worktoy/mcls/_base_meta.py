"""
BaseMeta provides an entry point for classes implementing the overload
protocol central to the worktoy library.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from . import AbstractMetaclass
from . import BaseSpace as BSpace
from . import Types


class BaseMeta(AbstractMetaclass):
  """
  BaseMeta is a simple extension of AbstractMetaclass that overrides
  the default class body namespace with 'BaseSpace', a custom namespace
  implementation.

  This metaclass does not introduce any behavior of its own beyond
  enabling namespace hooks defined in 'BaseSpace', such as 'LoadSpaceHook',
  'NamespaceHook', 'ReservedNamespaceHook', and 'FlexCallHook'.

  It serves as a ready-to-use entry point for classes that require
  hook-driven behavior during class construction without writing a custom
  metaclass.

  Example
  -------
      class MyClass(metaclass=BaseMeta):
        ...
  """

  @classmethod
  def __prepare__(mcls, name: str, bases: Types, **kwargs) -> BSpace:
    """Prepare the class namespace."""
    return BSpace(mcls, name, bases, **kwargs)

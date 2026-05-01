"""
BaseMeta provides an entry point for classes implementing the overload
protocol central to the worktoy library.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from ..desc import Field
from . import AbstractMetaclass
from . import BaseSpace as BSpace
from . import Types

if TYPE_CHECKING:  # pragma: no cover
  from typing import Self, TypeAlias, Union

  StrField: TypeAlias = Union[str, Field]


class BaseMeta(AbstractMetaclass):
  """
  BaseMeta is a simple extension of AbstractMetaclass that overrides
  the default class body namespace with `BaseSpace`, a custom namespace
  implementation.

  ## Purpose
6
  This metaclass does not introduce any behavior of its own beyond
  enabling namespace hooks defined in `BaseSpace`, such as `OverloadHook`,
  `PreClassHook`, `NameHook`, and `ReservedNameHook`.

  It serves as a ready-to-use entry point for classes that require
  hook-driven behavior during class construction without writing a custom
  metaclass.

  ## Example

      class MyClass(metaclass=BaseMeta):
        ...
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables

  #  Fallback Variables

  #  Private Variables

  #  Public Variables

  #  Virtual Variables

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def __prepare__(mcls, name: str, bases: Types, **kwargs) -> BSpace:
    """Prepare the class namespace."""
    bases = (*[b for b in bases if b.__name__ != '_InitSub'],)
    return BSpace(mcls, name, bases, **kwargs)

  def __new__(mcls, *args, **kwargs) -> BaseMeta:
    return super().__new__(mcls, *args, **kwargs)

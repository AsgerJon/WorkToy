"""
BaseMeta is the metaclass that wires up the overload protocol.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from . import AbstractMetaclass
from . import BaseSpace as BSpace

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias

  Types: TypeAlias = tuple[type, ...]


class BaseMeta(AbstractMetaclass):
  """
  BaseMeta is a simple extension of AbstractMetaclass that overrides
  the default class body namespace with 'BaseSpace', a custom namespace
  implementation.

  This metaclass introduces no behavior of its own beyond switching the
  namespace class to 'BaseSpace'. 'BaseSpace' adds 'LoadSpaceHook' and
  inherits 'NamespaceHook', 'ReservedNamespaceHook', and 'FlexCallHook'
  from 'AbstractNamespace'.

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
    """
    The '__prepare__' method returns a 'BaseSpace' as the class-body
    namespace, the one override 'BaseMeta' makes over
    'AbstractMetaclass'.
    """
    return BSpace(mcls, name, bases, **kwargs)

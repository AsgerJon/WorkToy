"""
BaseMeta is the metaclass that wires up the overload protocol.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from . import AbstractMetaclass
from . import BaseSpace as BSpace

if TYPE_CHECKING:  # pragma: no cover, no mutate
  from typing import TypeAlias

  Types: TypeAlias = tuple[type, ...]


class BaseMeta(AbstractMetaclass):
  """
  A class using '@overload' needs a metaclass whose namespace gathers the
  declarations and builds the dispatchers, on top of everything
  'AbstractMetaclass' does. A project writing a metaclass of its own
  with overloading needs a metaclass to build on.

  Implementation
  --------------

  'BaseMeta' is 'AbstractMetaclass' with 'BaseSpace' as the namespace,
  and nothing else. 'BaseObject' uses it. A metaclass with a namespace of
  its own subclasses 'BaseMeta' and returns an instance of a 'BaseSpace'
  subclass from '__prepare__'.
  """

  @classmethod
  def __prepare__(mcls, name: str, bases: Types, **kwargs) -> BSpace:
    return BSpace(mcls, name, bases, **kwargs)

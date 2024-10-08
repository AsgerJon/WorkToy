"""InfoMeta provides a needlessly complicated way of logging stuff.
Allegedly. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

try:
  from typing import Callable
except ImportError:
  Callable = object

try:
  from typing import TYPE_CHECKING
except ImportError:
  TYPE_CHECKING = False

try:
  from typing import Type
except ImportError:
  if TYPE_CHECKING:
    Type = type('Type', (), dict(__getitem__=lambda cls, key: cls.__class__))
  else:
    Type = {object: type}

from worktoy.parse import maybe


class InfoMeta(type):
  """Sets descriptor on class level"""

  __cls_instances__ = None

  def _getInstances(cls) -> dict:
    """Getter-function for list of instances"""
    return maybe(cls.__cls_instances__, {})

  def _addInstance(cls, self: object) -> None:
    """Setter-function for list of instances"""
    instances = cls._getInstances()
    cls.__cls_instances__ = {**instances, getattr(self, 'name'): self}

  def __getattr__(cls, key: str) -> object:
    """Allows the dot to return a name instance. """
    value = cls._getInstances().get(key, None)
    if value is None:
      return object.__getattribute__(cls, key)

  def __call__(cls, name: str) -> object:
    """The '__call__' method is invoked when the class is called."""

    self = type.__call__(cls, name)
    cls._addInstance(self)

    return self

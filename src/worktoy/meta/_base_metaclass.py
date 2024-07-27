"""BaseMetaclass provides general functionality for derived classes. This
includes primarily function overloading. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from worktoy.meta import AbstractMetaclass, Bases, BaseNamespace


class BaseMetaclass(AbstractMetaclass):
  """BaseMetaclass provides general functionality for derived classes. This
  includes primarily function overloading. """

  @classmethod
  def __prepare__(mcls, name: str, bases: Bases, **kwargs) -> BaseNamespace:
    """The __prepare__ method is invoked before the class is created. This
    implementation ensures that the created class has access to the safe
    __init__ and __init_subclass__ through the BaseObject class in its
    method resolution order."""
    return BaseNamespace(mcls, name, bases, **kwargs)

  def __new__(mcls,
              name: str,
              bases: Bases,
              space: BaseNamespace,
              **kwargs) -> type:
    """The __new__ method is invoked to create the class."""
    namespace = space.compile()
    return super().__new__(mcls, name, bases, namespace, **kwargs)

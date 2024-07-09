"""AbstractMetaclass provides an abstract baseclass for custom
metaclasses. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Union

from worktoy.meta import AbstractNamespace


class MetaMetaclass(type):
  """MetaMetaclass is necessary to customize the __str__ method of a
  metaclass"""

  def __str__(cls) -> str:
    return cls.__name__


class AbstractMetaclass(MetaMetaclass, metaclass=MetaMetaclass):
  """The AbstractMetaclass class provides a base class for custom
  metaclasses."""

  @classmethod
  def __prepare__(mcls,
                  name: str,
                  bases: tuple[type, ...],
                  **kwargs) -> Union[AbstractNamespace, dict]:
    """The __prepare__ method is invoked before the class is created."""
    return AbstractNamespace(mcls, name, bases, **kwargs)

  def __new__(mcls,
              name: str,
              bases: tuple[type, ...],
              namespace: Union[AbstractNamespace, dict],
              **kwargs) -> type:
    """The __new__ method is invoked to create the class."""
    if hasattr(namespace, 'compile'):
      namespace = namespace.compile()
    return MetaMetaclass.__new__(mcls, name, bases, namespace, **kwargs)

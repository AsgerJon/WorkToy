"""MetaJuice provides for decorating methods as factory methods"""
#  Copyright (c) 2023 Asger Jon Vistisen
#  MIT Licence
from __future__ import annotations

from worktoy.core import CallMeMaybe, maybe


class _FactoryMeta(type):
  """Classes having this as their metaclass can access factories marked
  with the factory decorator through the class dictionary _mainFactories."""

  def __init__(cls, name, bases, nameSpace):
    cls._mainFactories = {}
    cls._validator = None
    for key, val in nameSpace.items():
      factoryKey = getattr(val, '__factory__', False)
      validatorKey = getattr(val, '__validator__', False)
      if factoryKey and validatorKey:
        raise ValueError('Function cannot be both validator and factory!')
      if factoryKey:
        cls._mainFactories[factoryKey] = val
      if validatorKey and cls._validator is not None:
        raise ValueError('Multiple functions marked as validator!')
      if validatorKey and cls._validator is None:
        cls._validator = val
    super().__init__(name, bases, nameSpace)


class MetaJuice(metaclass=_FactoryMeta):
  """This in between mixin removes the need for the keyword metaclass."""
  pass

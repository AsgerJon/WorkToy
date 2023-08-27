"""WorkToy - Core - TypeAware
This mixin class adds several methods relating to types and classes. """
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

import builtins

from worktoy.core import BuiltinFunction, Function, FunctionTuple


class TypeAware:
  """WorkToy - Core - TypeAware
  This class adds several methods relating to types and classes. """

  @staticmethod
  def getBuiltinTypes() -> dict:
    """Getter-function for list of builtin types"""
    base = []
    for (key, val) in builtins.__dict__.items():
      test = isinstance(val, type)
      test = test and (not isinstance(val, BuiltinFunction))
      test = test and (not issubclass(val, BaseException))
      test = test and (not key.startswith('__'))
      if test:
        try:
          val.__new__(val)
          base.append((key, val))
        except TypeError as e:
          base.append((key, val, e))
    return {i[0]: i[1] for i in base if len(i) == 2}

  @classmethod
  def resolveType(cls, typeName: str) -> type:
    """Returns the type that matches the given name"""
    if typeName == 'type':
      return type
    builtInType = cls.getBuiltinTypes().get(typeName, None)
    localType = locals().get(typeName, None)
    globalType = globals().get(typeName, None)
    typesFound = [i for i in [builtInType, localType, globalType] if i]
    if not typesFound:
      raise NameError(typeName)
    if len(typesFound) == 1:
      return typesFound[-1]
    if len(typesFound) == 2:
      if typesFound[0] is typesFound[-1]:
        return typesFound[0]
    for foundType in typesFound:
      if foundType is not typesFound[0]:
        raise TypeError
    return typesFound[0]

  @classmethod
  def createInstanceOf(cls, type_: object) -> object:
    """Creator-function for sample of the type."""
    if type_ is type:
      return type('SampleClass', (), {})
    if isinstance(type_, type):
      try:
        return type_.__new__(type_, )
      except TypeError as e:
        msg = """Failed to create base sample of %s""" % type_
        raise TypeError(msg) from e
    if isinstance(type_, str):
      type_ = cls.resolveType(type_)
      return cls.createInstanceOf(type_)
    if not isinstance(type_, str):
      return cls.createInstanceOf(type(type_))

  @classmethod
  def createInstanceFactory(cls, type_: type,
                            callBack: Function = None) -> Function:
    """Creates a factory for instance of the given type. The factory is
    tested before being returned. If not callback function is provided,
    and the factory fails, the method will raise a TypeError. Otherwise,
    the method will invoke the callback in case of failure.

    The base function expects the type argument to be a type, but any
    object is acceptable. If 'type_' is a string, a type of the same name
    is resolved to a type, which is then passed to the base function. For
    all other types, the type of the provided argument is passed on.
    """

    if isinstance(type_, str):
      type_ = cls.resolveType(type_)
      return cls.createInstanceFactory(type_)
    if not isinstance(type_, type):
      return cls.createInstanceFactory(type(type_))

    def errorHandle(error: Exception) -> object:
      """Handles error"""
      if isinstance(callBack, FunctionTuple):
        return callBack(error)
      raise error

    def factory() -> object:
      """Factory function"""
      return type_.__new__(type_)

    try:
      factory()
      return factory
    except Exception as e:
      return errorHandle(e)

  @classmethod
  def flatten(cls, notFlat: list, r=None) -> list:
    """Flattens a nested list"""
    if r is None:
      r = 0
    else:
      r = r + 1
    if r > 10:
      raise RecursionError
    out = []
    flat = True
    for item in notFlat:
      if isinstance(item, list):
        for item2 in cls.flatten(item):
          out.append(item2)
        flat = False
      else:
        out.append(item)
    return out if flat else cls.flatten(out, r)

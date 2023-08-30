"""WorkToy - Core - MetaClassParams
The meta-metaclass implements __repr__ and __str__ for even the
metaclasses themselves. """
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from random import choices
from string import ascii_letters, digits
from typing import cast

from icecream import ic

from worktoy.core import Bases, Function
from worktoy.waitaminute import MissingKeyHandleError

ic.configureOutput(includeContext=True)


class _MetaMetaClass(type):
  """The meta-metaclass implements __repr__ and __str__ for even the
  metaclasses themselves."""

  @staticmethod
  def _generateRandomKey(n: int = None) -> str:
    """Generator function for alphanumerical keys."""
    n = 16 if n is None else n
    alphaNum = [c for c in '%s%s' % (ascii_letters, digits)]
    return ''.join(choices(alphaNum, k=n))

  @classmethod
  def _validatePrepareMethod(mcls, prepare: Function) -> Function:
    """Pass the __prepare__ method."""

    name = 'Test'
    bases = ()

    if hasattr(prepare, '__func__'):
      prepare = getattr(prepare, '__func__')
    try:
      nameSpace = prepare(mcls, name, bases)
    except TypeError as e:
      nameSpace = prepare(name, bases)

    key = mcls._generateRandomKey(16)
    val = None
    try:
      nameSpace[key]
    except KeyError as e:
      if str(e) != key:
        raise MissingKeyHandleError(nameSpace, mcls, )

  @classmethod
  def _updateNameSpace(mcls, nameSpace: dict, name: str) -> Function:
    """Since the meta-metaclass is responsible for all other metaclasses,
    it can enforce behaviour even on the metaclass level. This method
    ensures that a newly created metaclass will still enforce the
    validation check of the namespace. If the '__prepare__' keyword
    points to a function, it gets replaced with a wrapped version that
    includes validation."""
    if not isinstance(nameSpace, dict):
      from worktoy.base import DefaultClass
      msg = """Expected nameSpace to be of type dict. The _updateNameSpace 
      should first look through the basic nameSpace returned by the 
      __prepare__ method on the MetaMetaClass. Instead, received: %s."""
      msg = DefaultClass().monoSpace(msg) % type(nameSpace)
      raise TypeError(msg)
    new__prepare__ = None
    key, val = None, None
    for (key, val) in nameSpace.__dict__.items():
      if key == '__prepare__':
        new__prepare__ = val
        break
    if new__prepare__ is None or not isinstance(new__prepare__, Function):
      nameSpace['__prepare__'] = mcls.__prepare__
      return nameSpace
    #  Testing the nameSpace returned by the __prepare__ method. Please
    #  note that the nameSpace analyzed up to now was the one returned
    #  from the MetaMetaClass.

  @classmethod
  def __prepare__(mcls, name, bases, **kwargs) -> dict:
    """Implementing the nameSpace generation"""
    return dict()

  def __new__(mcls,
              name: str,
              bases: Bases,
              nameSpace: dict,
              **kwargs) -> type:
    # nameSpace = mcls._updateNameSpace(nameSpace, name)
    return type.__new__(mcls, name, bases, nameSpace, **kwargs)

  def __init__(cls,
               name: str,
               bases: Bases,
               nameSpace: dict,
               **kwargs) -> None:
    type.__init__(cls, name, bases, nameSpace, **kwargs)

  def __str__(cls) -> str:
    """String Representation"""
    return cls.__qualname__

  def __repr__(cls) -> str:
    """Code Representation"""
    return cls.__qualname__

  def __getattr__(cls, key: str) -> object:
    bases = object.__getattribute__(cls, '__bases__')
    errors = []
    for base in bases:
      try:
        return object.__getattribute__(base, key)
      except AttributeError as e:
        errors.append(e)
    raise errors[-1]


class MetaMetaClass(_MetaMetaClass, metaclass=_MetaMetaClass):
  """This class is both derived from and subclass of the _MetaMetaClass."""
  pass

  # def __getattr__(cls, key: str) -> object:
  #   return _MetaMetaClass.__getattr__(cls, key)
  # def __new__(mcls,
  #             name: str = None,
  #             bases: Bases = None,
  #             nameSpace: dict = None,
  #             **kwargs) -> type:
  #   nameSpace = {} if nameSpace is None else nameSpace
  #   bases = () if bases is None else bases
  #   name = 'GenericWorkToyClass' if name is None else name
  #
  #   return _MetaMetaClass.__new__(mcls, name, bases, nameSpace, **kwargs)

  # def __init__(cls,
  #              name: str = None,
  #              bases: Bases = None,
  #              nameSpace: dict = None,
  #              **kwargs) -> None:
  #   nameSpace = {} if nameSpace is None else nameSpace
  #   bases = () if bases is None else bases
  #   name = 'GenericWorkToyClass' if name is None else name
  #   if not isinstance(cls, _MetaMetaClass):
  #     raise TypeError
  #   _MetaMetaClass.__init__(cls, name, bases, nameSpace, **kwargs)

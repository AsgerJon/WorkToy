"""LMAO"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from types import GenericAlias
from typing import Never

from icecream import ic

from worktoy.core import ParsingClass, Function

ic.configureOutput(includeContext=True)


class CUNT(type):
  """LMAO"""

  def __call__(cls, *args, **kwargs) -> Never:
    """LMAO"""
    if kwargs.get('_root', False):
      return super().__call__(args, **kwargs)
    raise TypeError('LMAO XD')

  def __repr__(cls) -> str:
    return cls.__class__.__qualname__

  def __str__(cls) -> str:
    return cls.__class__.__qualname__


class FUCK(ParsingClass, metaclass=CUNT):
  """LMAO"""

  @classmethod
  def __class_getitem__(cls, item):
    """OMG"""
    return cls(*item, _root=True)

  def __init__(self, *args, **kwargs) -> None:
    ParsingClass.__init__(self, *args, **kwargs)
    self._signature = self.collectTypes(*args)

  def collectTypes(self, *args) -> list:
    """Collects the types from the positional arguments"""
    onlyThese = (list, tuple, GenericAlias, type)
    typeBag = [arg for arg in args if isinstance(arg, onlyThese)]
    baseTypes = self.fromTypes(*typeBag)
    return baseTypes

  def getCallBack(self, ) -> Function:
    """Getter-function for the callback function"""

    def getRawName(cls: type) -> str:
      """Getter-function for raw name"""
      baseNames = [
        getattr(cls, '__qualname__', None),
        getattr(cls, '__name__', None),
        str(cls)
      ]
      for name in baseNames:
        if name is not None:
          return name

    def getCoolName(cls: type) -> str:
      """Getter-function for the cool name"""
      name = getRawName(cls)
      if len(name) < 6:
        return name.upper()

      return name.capitalize()

    def func(cls: type, r: int) -> dict:
      """TypeClass callback"""
      return dict(rawName=getRawName(cls),
                  coolName=getCoolName(cls),
                  nestLevel=r, cls=cls)

    return func

  def fromTypes(self, *args) -> list:
    """LMAO"""
    array = []
    callBack = None
    for arg in args:
      if isinstance(arg, GenericAlias):
        array.append(list(arg.__args__))
      if isinstance(arg, tuple):
        array.append(list(arg))
      if isinstance(arg, (type, list)):
        array.append(arg)
      if isinstance(arg, Function) and callBack is None:
        callBack = arg
    return self.walk(array, self.getCallBack())

  def walk(self, array: object,
           callBack: Function = None,
           **kwargs) -> list:
    """LMAO"""
    r = kwargs.get('r', -1) + 1
    if not isinstance(array, (list, tuple)):
      return array if callBack is None else callBack(array, r)
    array = [item for item in array]
    out = []
    for element in array:
      out.append(self.walk(element, callBack, r=r))
    while len(out) == 1 and isinstance(out[0], list):
      out = out[0]
    return out

  def __call__(cls, *args, **kwargs) -> Never:
    raise TypeError('LMAO XD')

  def getRawNames(self) -> list[str]:
    """Getter function for the type names."""
    rawCallBack = lambda entry: entry.get('rawName', None)
    nestCallBack = lambda entry: entry.get('nestLevel', None)
    callBack = lambda e: (rawCallBack(e), nestCallBack(e))
    return self.telescope(self._signature, callBack)

  def getTypes(self) -> list[type]:
    """Getter function for the type names."""
    clsCallBack = lambda entry: entry.get('cls', None)
    nestCallBack = lambda entry: entry.get('nestLevel', None)
    callBack = lambda e: (clsCallBack(e), nestCallBack(e))
    return self.telescope(self._signature, callBack)

  def getCoolNames(self) -> list[str]:
    """Getter function for the type names."""
    coolCallBack = lambda entry: entry.get('coolName', None)
    nestCallBack = lambda entry: entry.get('nestLevel', None)
    callBack = lambda e: (coolCallBack(e), nestCallBack(e))
    return self.telescope(self._signature, callBack)

  def __str__(self, ) -> str:
    """String Representation"""
    header = self.__class__.__qualname__
    tab = lambda x: '%s%s' % (x[1] * ' ', x[0])
    rawNames = self.getRawNames()
    body = '\n'.join([tab(name) for name in rawNames])
    return '%s\n%s' % (header, body)

  def __repr__(self, ) -> str:
    """String Representation"""
    mcls = self.__class__
    types = '\n'.join([str(i) for i in self._signature])
    return '%s(%s)' % (mcls, types)

  @staticmethod
  def telescope(signature: list, callBack: Function) -> list:
    """Telescopes into a signature"""
    out = []
    for entry in signature:
      if isinstance(entry, dict):
        out.append(callBack(entry))
      else:
        out.append(FUCK.telescope(entry, callBack))
    return out

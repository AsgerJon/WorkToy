"""AbstractType provides a basic implementation of the type related
classes"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

import os

from abc import abstractmethod

from worktoy.worktype import AbstractMetaType


class AbstractType(AbstractMetaType):

  def __new__(mcls, name: str, bases: tuple, namespace: dict,
              **kwargs) -> type:
    print('fuck fuck')
    newClass = super(AbstractType, mcls).__new__(
      mcls, name, bases, namespace, **kwargs)
    originalInit = newClass.__init__

    def wrappedInit(cls, *args, **kwargs2) -> None:
      """Wrapped initializer"""
      originalInit(cls, *args, **kwargs2)
      cls.protocolify(name, namespace)

    newClass.__init__ = wrappedInit
    return newClass

  def protocolify(cls, name: str, namespace: dict) -> None:
    """Create Protocol version of a class and save as .py file in
    _typingversions module."""
    print('cunt cunt cunt')
    protocolClassName = '%sProtocol' % name
    protocolClassBody = {}
    for attrName, attrValue in namespace.items():
      if callable(attrValue):
        protocolClassBody[attrName] = abstractmethod(attrValue)

    typingVersionsDir = '_typingversions'
    if not os.path.exists(typingVersionsDir):
      os.makedirs(typingVersionsDir)

    protocolFilePath = os.path.join(
      typingVersionsDir, '%s.py' % protocolClassName)
    with open(protocolFilePath, 'w') as protocolFile:
      protocolCode = 'from typing import Protocol\n'
      protocolCode += 'from abc import abstractmethod\n\n'
      protocolCode += 'class %s(Protocol):\n' % protocolClassName
      for methodName, method in protocolClassBody.items():
        args = ', '.join(getattr(method, '__code__').co_varnames)
        # args = ', '.join(method.__code__.co_varnames)
        protocolCode += '  @abstractmethod\n'
        protocolCode += '  def %s(%s) -> None:\n' % (methodName, args)
        protocolCode += '    ...\n\n'
      protocolFile.write(protocolCode)
  #
  # def __init__(cls, name: str, bases: tuple, namespace: dict, **kwargs):
  #   super().__init__(name, bases, namespace, **kwargs)
  #   print('Shit')

  def __contains__(cls, element: object) -> bool:
    return isinstance(element, cls)

  @abstractmethod
  def __instancecheck__(cls, obj: object) -> bool:
    pass

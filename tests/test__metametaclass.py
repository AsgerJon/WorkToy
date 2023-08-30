"""Testing MetaMetaClass"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen

from unittest import TestCase

from worktoy.base import DefaultClass
from worktoy.core import Bases
from worktoy.fields import INT
from worktoy.metaclass import MetaMetaClass, AbstractMetaClass


class BadNameSpace(dict):
  """Dictionary subclass not raising KeyError"""

  def __init__(self, *args, **kwargs) -> None:
    self._contents = {}
    dict.__init__(self, *args, **kwargs)

  def _getContents(self) -> dict:
    return self._contents

  def __contains__(self, key: str) -> bool:
    print(key)
    return key in self._getContents()

  def __setitem__(self, key, val) -> None:
    print(key, val)
    self._contents[key] = val

  def __getitem__(self, key: str) -> object:
    print(key)
    try:
      return self._getContents()[key]
    except KeyError as e:
      print('LMAO')


class BadMeta(AbstractMetaClass):
  """Bad meta class"""

  @classmethod
  def __prepare__(mcls, name, bases, **kwargs) -> object:
    """Implementing the nameSpace generation"""
    return BadNameSpace()

  def __new__(mcls,
              name: str,
              bases: Bases,
              nameSpace: object,
              **kwargs) -> type:
    print(nameSpace)
    print(type(nameSpace))
    return type.__new__(mcls, name, bases, nameSpace, **kwargs)

  def __init__(cls, name, bases, nameSpace, **kwargs) -> None:
    type.__init__(cls, name, bases, nameSpace, **kwargs)
    setattr(cls, '__unique_name__', nameSpace.get('__unique_name__', None))

  def __call__(cls, *args, **kwargs) -> object:
    self = object.__new__(cls)
    cls.__init__(self, *args, **kwargs)
    return self

  def __str__(cls) -> str:
    uniqueName = getattr(cls, '__unique_name__', None)
    if uniqueName is None:
      return 'LMAO'
    return uniqueName


class BadClass(metaclass=BadMeta):
  """Bad Class"""

  a = 1

  b = 7777

  # b = INT(77)

  def __str__(self, ) -> str:
    return 'I am a bad class!'

  def __repr__(self) -> str:
    return self.__class__.__qualname__

  def __init__(self, *args, **kwargs) -> None:
    self._number = 7

  def __call__(self) -> str:
    return 'LMAO'

  def _doStuff(self, *args, **kwargs) -> None:
    for arg in args:
      if isinstance(arg, type):
        print(arg)


class Test_MetaMetaClass(TestCase):
  """Testing MetaMetaClass"""

  def setUp(self) -> None:
    """Setting up"""
    self.badNameSpace = BadNameSpace()
    self.badMeta = BadMeta
    self.badClass = BadClass
    self.badInstance = self.badClass()

  def test_badNameSpace(self) -> None:
    self.badNameSpace['bla'] = 7
    self.assertEqual(self.badNameSpace['bla'], 7)

  def test_badNameSpaceError(self) -> None:
    self.assertIsNone(self.badNameSpace['lmao'])

  def test_NormalDictError(self) -> None:
    lmao = dict()
    self.assertRaises(KeyError, lambda: lmao['lol'])

  def test_BadMetaPrepare(self) -> None:
    test = self.badMeta('LMAO', (), {})
    nameSpace = BadMeta.__prepare__('lol', (), )
    self.assertIsInstance(nameSpace, BadNameSpace)

  # def test_IntDescriptor(self) -> None:
  #   self.assertIsInstance(self.badInstance.b, int)
  #
  # def test_IntDescriptorOperation(self) -> None:
  #   self.badInstance.b = 7
  #   self.assertEqual(self.badInstance.b, 7)

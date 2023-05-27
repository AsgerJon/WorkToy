"""Testing BaseMeta"""
#  Copyright (c) 2023 Asger Jon Vistisen
#  MIT Licence
from __future__ import annotations

from typing import NoReturn, Any
from unittest import TestCase

from icecream import ic

from worktoy.core import extractArg
from worktoy.field import BaseMeta
from worktoy.stringtools import stringList

ic.configureOutput(includeContext=True)


class SomeMeta(BaseMeta):
  """Sub metaclass of BaseMeta"""

  _docFooter = 'Thank you for using SomeMeta!'
  _docTitle = 'Welcome to SomeMeta!'
  _docHeader = 'Documentation'
  _docBody = """Where is the documentation?"""

  @classmethod
  def getHeader(mcls, ) -> str:
    """Getter-function for documentation footer"""
    return mcls._docHeader

  @classmethod
  def getTitle(mcls, cls: type) -> str:
    """Getter-function for documentation footer"""
    return '%s - %s' % (mcls._docTitle, cls.__qualname__)

  @classmethod
  def getBody(mcls, cls: type) -> str:
    """Getter-function for documentation body"""
    return getattr(cls, '__doc__', mcls._docBody)

  @classmethod
  def getFooter(mcls, ) -> str:
    """Getter-function for documentation footer"""
    return mcls._docFooter

  @classmethod
  def getDoc(mcls, cls: type) -> str:
    """Getter-function for documentation!"""
    components = [
      mcls.getHeader(),
      mcls.getTitle(cls),
      mcls.getBody(cls),
      mcls.getFooter()
    ]
    return '\n'.join(components)

  def __call__(cls, *args, **kwargs) -> Any:
    """Creates a new instance of a class using as metaclass this."""
    instance = cls.__new__(cls)
    cls.__init__(instance, *args, **kwargs)
    setattr(instance, '__doc__', SomeMeta.getDoc(cls))
    return instance


class SomeClass(metaclass=SomeMeta):
  """Basic class using the SomeMeta as baseclass"""

  def __init__(self, *args, **kwargs) -> None:
    nameKeys = stringList('name, named, title, titled')
    self._name, args, kwargs = extractArg(str, nameKeys, *args, **kwargs)

  def __str__(self, ) -> str:
    """String Representation"""
    return '%s\n%s' % (self._name, getattr(self, '__doc__'))


class TestBaseMeta(TestCase):
  """Testing BaseMeta
  #  Copyright (c) 2023 Asger Jon Vistisen
  #  MIT Licence"""

  def setUp(self, ) -> NoReturn:
    """Setting up classes"""
    self.cls = SomeClass
    self.instanceName = 'Testing BaseMeta'
    self.instance = SomeClass(self.instanceName)

  def testBase(self) -> NoReturn:
    """This seemingly unambitious test simply requires no errors to have
    occurred."""
    self.assertTrue(True)

  def testInit(self) -> NoReturn:
    """Tests that init has run"""
    self.assertEqual(self.instanceName, self.instance._name)

  def testDoc(self) -> NoReturn:
    """Tests that documentation was set"""
    self.assertTrue('Thank you for using SomeMeta' in self.instance.__doc__)

  def testMetaAttribute(self) -> NoReturn:
    """Tests that the class knows its meta"""
    self.assertEqual(self.cls.__meta__, SomeMeta)

  def testClassAttribute(self) -> NoReturn:
    """Testing if attributes on SomeClass was properly set"""
    for (key, val) in self.cls.__dict__.items():
      if not (BaseMeta.isDunder(key) or BaseMeta.isImmutable(val)):
        attrCls = getattr(val, '__cls__', None)
        self.assertIsNotNone(attrCls)
        self.assertEqual(attrCls, self.cls)

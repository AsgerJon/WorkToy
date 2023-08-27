"""WorkToy - DevTest - TesterClass
LMAO"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen

from worktoy.core import DefaultClass


class MetaMeta(type):
  """LMAO"""

  def __str__(cls) -> str:
    """LMAO"""
    return 'Class: %s' % cls.__qualname__

  def __repr__(cls, *self) -> str:
    return '%s(LMAO)' % cls.__qualname__


class TestClass(DefaultClass, metaclass=MetaMeta):
  """LMAO"""

  @staticmethod
  def TestStaticMethod() -> str:
    """LMAO"""
    return 'lmao'

  @classmethod
  def TestClassMethod(cls) -> type:
    """CUNT"""
    return cls

  def __init__(self, cls: type) -> None:
    DefaultClass.__init__(self, cls)

  def _underScored(self) -> str:
    """blabla"""
    return 'blabla'

  bla = 7

  def __str__(self) -> str:
    """String Representation"""
    return 'Instance of: %s' % (self.__class__.__qualname__)

  def __repr__(self) -> str:
    return '%s(...)' % (self.__class__.__qualname__)

  def fuck(self) -> None:
    """LMAO"""

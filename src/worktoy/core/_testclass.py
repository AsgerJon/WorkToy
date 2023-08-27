"""WorkToy - Core - TestClass
Used for testing and demonstration. """
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

import os

from worktoy.core import DefaultClass, CallMeMaybe


class TestClass(DefaultClass):
  """WorkToy - Core - TestClass
  Used for testing and demonstration. """

  @CallMeMaybe
  def __init__(self, this, *args, **kwargs) -> None:
    DefaultClass.__init__(self, *args, **kwargs)

  def __str__(self, ) -> str:
    msg = """Hello there! I'm the %s of the %s module"""
    return msg % (self.__class__.__qualname__, self.__module__)

  def __repr__(self, ) -> str:
    return '%s()' % (self.__class__.__qualname__)

  def moduleName(self) -> str:
    """LMAO"""
    here = os.path.dirname(__file__)
    there = '__init__.py'
    filePath = os.path.join(here, there)
    with open(filePath, 'r') as f:
      data = f.read()
    lines = data.split('\n')
    moduleName = lines[0].replace('\"\"\"', '')
    return self.trimWhitespace(moduleName)

  def tester(self, obj: object) -> str:
    """LMAO"""
    return obj.__module__

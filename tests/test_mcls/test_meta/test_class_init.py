"""
TestClassInit tests the '__class_init__' dunder hook for classes derived
from 'AbstractMetaclass' and subclasses of it from the 'worktoy.mcls'
module.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.mcls import AbstractMetaclass, BaseObject
from .. import MCLSTest


class Init(BaseObject, metaclass=AbstractMetaclass):
  """
  Init class that implements __class_init__.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  __custom_class_init__ = False

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def __class_init__(cls, *args, **kwargs) -> None:
    """Custom class initialization."""
    type.__setattr__(cls, '__custom_class_init__', True)


class NoInit(BaseObject, metaclass=AbstractMetaclass):
  """
  NoInit class that does not implement __class_init__.
  """
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  __custom_class_init__ = False


class TestClassInit(MCLSTest):
  """
  TestClassInit tests the '__class_init__' dunder hook for classes derived
  from 'AbstractMetaclass' and subclasses of it from the 'worktoy.mcls'
  module.
  """

  def test_class_init(self) -> None:
    """
    Tests that the __class_init__ method is called correctly.
    """
    self.assertTrue(Init.__custom_class_init__)
    self.assertFalse(NoInit.__custom_class_init__)

"""TestLazyInstantiation tests that the AttriBox descriptor instances do
defer instantiation of the field classes until the first time the field
is accessed. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.base import BaseObject
from worktoy.desc import AttriBox
from worktoy.meta import BaseMetaclass
from worktoy.parse import maybe

try:
  from typing import Any
except ImportError:
  Any = object


class LazyMeta(BaseMetaclass):
  """This class keeps track of instances"""

  __iter_contents__ = None
  __instance_objects__ = []

  def getInstances(cls, ) -> list:
    """This class keeps track of instances"""
    return maybe(cls.__instance_objects__, [])

  def addInstance(cls, self: object) -> Any:
    """This class keeps track"""
    existing = cls.getInstances()
    cls.__instance_objects__ = [*existing, self]
    return self

  def __call__(cls, *args, **kwargs):
    """This class keeps track of instances"""
    return cls.addInstance(BaseMetaclass.__call__(cls, *args, **kwargs))

  def __contains__(cls, self: object) -> bool:
    """This class keeps track of instances"""
    return True if self in cls.getInstances() else False

  def __iter__(cls, ) -> iter:
    """Implementation of the iterator protocol"""
    cls.__iter_contents__ = cls.getInstances()
    return cls

  def __next__(cls, ) -> object:
    """Implementation of the iterator protocol"""
    if cls.__iter_contents__:
      return cls.__iter_contents__.pop(0)
    raise StopIteration

  def __len__(cls, ) -> int:
    """Implementation of the length protocol"""
    out = 0
    for _ in cls:
      out += 1
    return out

  def __bool__(cls, ) -> bool:
    for _ in cls:
      return True
    return False


class Lazy(metaclass=LazyMeta):
  """This class is derived from LazyMeta allowing it to keep track of
  instances"""

  __instance_name__ = None

  def __init__(self, name: str) -> None:
    """This class is derived from LazyMeta allowing it to keep track of
    instances"""
    self.__instance_name__ = name

  def __str__(self, ) -> str:
    """This class is derived from LazyMeta allowing it to keep track of
    instances"""
    return self.__instance_name__


class Owner(BaseObject):
  """This class owns lazy instances"""

  trait = AttriBox[Lazy]('lazy trait!')


class TestLazyInstantiation(TestCase):
  """
  TestLazyInstantiation tests that the AttriBox descriptor instances do
  defer instantiation of the field classes until the first time the field
  is accessed.
  """

  def setUp(self, ) -> None:
    """Instantiates test classes"""
    self.owner = Owner()

  def test_lazy_instantiation(self, ) -> None:
    """Tests that the AttriBox descriptor instances do defer instantiation
    of the field classes until the first time the field is accessed."""
    self.assertIsInstance(Owner.trait, AttriBox)
    self.assertFalse(Lazy)
    self.assertIsInstance(self.owner.trait, Lazy)
    self.assertTrue(Lazy)

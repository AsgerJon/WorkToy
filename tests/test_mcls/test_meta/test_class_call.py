"""
TestClassCall tests that the class call hook enables actual functionality.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.attr import Field
from worktoy.parse import maybe
from worktoy.static import AbstractObject
from worktoy.mcls import AbstractMetaclass
from worktoy.waitaminute import TypeException

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Self, TypeAlias, Any


class Thing(AbstractObject, metaclass=AbstractMetaclass):
  """
  Thing reuses instances from the key. When calling the class with a key,
  if the class has already been instantiated with that key, it returns the
  existing instance instead of creating a new one.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables
  __instance_registry__ = None

  #  Private Variables
  __instance_name__ = None

  #  Public Variables
  name = Field()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def _getInstances(cls) -> dict[str, Any]:
    """
    Get the private instance registry.
    """
    return maybe(cls.__instance_registry__, dict())

  @name.GET
  def _getName(self) -> str:
    """
    Get the name of the instance.
    """
    return self.__instance_name__

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def _addInstance(cls, key: str, instance: Any) -> None:
    """
    Add an instance to the registry.
    """
    existing = cls._getInstances()
    if key not in existing:
      existing[key] = instance
      cls.__instance_registry__ = existing

  @name.SET
  def _setName(self, name: str) -> None:
    """
    Set the name of the instance.
    """
    if not isinstance(name, str):
      raise TypeException('name', name, str)
    self.__instance_name__ = name

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  Python API   # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __contains__(self, key: str) -> bool:
    """
    Check if the instance registry contains the key.
    """
    existing = self._getInstances()
    return True if key in existing else False

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  CONSTRUCTORS   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def __init__(self, key: str) -> None:
    self.name = key

  def __str__(self) -> str:
    """
    String representation of the Thing instance.
    """
    infoSpec = """%s named: '%s'"""
    return infoSpec % (type(self).__name__, self.name)

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @classmethod
  def __class_call__(cls, key: str, **kwargs) -> Any:
    existing = cls._getInstances()
    try:
      self = existing[key]
    except KeyError:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self = super().__new__(cls)
      cls._addInstance(key, self)
      return cls.__class_call__(key, _recursion=True)
    else:
      return self


class TestClassCallRegistry(TestCase):

  def setUp(self) -> None:
    """
    Sets up each test case
    """
    self.alpha = Thing('alpha')
    self.beta = Thing('beta')
    self.gamma = Thing('gamma')

  def test_class_call_registry(self) -> None:
    """
    Tests that calling 'Thing' returns a new instance for new keys and
    existing instances for existing keys.
    """

    newAlpha = Thing('alpha')
    newBeta = Thing('beta')
    newGamma = Thing('gamma')

    newDelta = Thing('delta')
    newEpsilon = Thing('epsilon')
    newZeta = Thing('zeta')

    self.assertIs(self.alpha, newAlpha)
    self.assertIs(self.beta, newBeta)
    self.assertIs(self.gamma, newGamma)

    newerDelta = Thing('delta')
    newerEpsilon = Thing('epsilon')
    newerZeta = Thing('zeta')

    self.assertIs(newDelta, newerDelta)
    self.assertIs(newEpsilon, newerEpsilon)
    self.assertIs(newZeta, newerZeta)

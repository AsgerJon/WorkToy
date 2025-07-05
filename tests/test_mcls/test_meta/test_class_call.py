"""
TestClassCall tests that the class call hook enables actual functionality.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.desc import Field
from worktoy.utilities import maybe
from worktoy.core import Object
from worktoy.mcls import AbstractMetaclass
from worktoy.waitaminute import TypeException

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class Thing(Object, metaclass=AbstractMetaclass):
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
        raise RecursionError  # pragma: no cover
      self = super().__new__(cls)
      cls._addInstance(key, self)
      cls._addInstance(key, self)  # coverage
      return cls.__class_call__(key, _recursion=True)
    else:
      return self


class TestClassCallRegistry(TestCase):

  @classmethod
  def tearDownClass(cls) -> None:
    import sys
    import gc
    sys.modules.pop(__name__, None)
    gc.collect()

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

    thing = Thing('breh')

"""TestAbstractNamespace - Test the AbstractNamespace class."""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

from unittest import TestCase

from worktoy.mcls import AbstractNamespace, Base, Space, AbstractMetaclass

if TYPE_CHECKING:
  from typing import Any, Callable, Self


class Base(metaclass=AbstractMetaclass):
  """Base class for testing."""

  def getNameSpace(self, ) -> AbstractNamespace:
    """Get the namespace of the class."""
    return getattr(type(self), '__namespace__', )

  def getPrime(self, ) -> AbstractNamespace:
    """Get the prime namespace of the class."""

    space = self.getNameSpace()
    return space.getPrimeSpace()


class SubClass(Base):
  """SubClass of Base for testing."""
  pass


class SubSubClass(SubClass):
  """SubClass of SubClass for testing."""
  pass


class TestAbstractNamespace(TestCase):
  """Test the AbstractNamespace class."""

  def setUp(self, ) -> None:
    """Set up the test case."""
    self._base = Base()
    self._subClass = SubClass()
    self._subSubClass = SubSubClass()

    space = Base.getNameSpace(self._base)
    entries = space.getMRO()

  def test_prime_space(self, ) -> None:
    """Test the prime space of the class."""
    self.assertIs(self._base.getPrime(), self._subClass.getPrime())
    self.assertIs(self._subClass.getPrime(), self._subSubClass.getPrime())
    self.assertIs(self._base.getPrime(), self._subSubClass.getPrime())

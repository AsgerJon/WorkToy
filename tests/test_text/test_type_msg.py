"""TestTypeMsg tests the typeMsg function."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from types import FunctionType
from unittest import TestCase

from worktoy.text import typeMsg
from worktoy.attr import AttriBox


class IntOnly:
  """Class requiring integer types."""

  value = AttriBox[int](0)

  def __init__(self, value: int) -> None:
    if not isinstance(value, int):
      e = typeMsg('value', value, int)
      raise TypeError(e)
    self.value = value


class Descriptor:
  """Implementation of the descriptor protocol. """

  __getter_function__ = None

  def _getGetterFunction(self) -> FunctionType:
    """Getter for the getter function."""
    if self.__getter_function__ is None:
      e = """The getter function has not been set!"""
      raise AttributeError(e)
    return self.__getter_function__

  def _setGetterFunction(self, callMeMaybe: FunctionType) -> FunctionType:
    """Test of the decorator."""
    if not isinstance(callMeMaybe, FunctionType):
      e = typeMsg('callMeMaybe', callMeMaybe, FunctionType)
      raise TypeError(e)
    self.__getter_function__ = callMeMaybe
    return callMeMaybe

  def GET(self, callMeMaybe: FunctionType) -> FunctionType:
    """Decorator for the getter function."""
    return self._setGetterFunction(callMeMaybe)

  def __get__(self, instance: object, owner: object) -> object:
    """Getter-function on the descriptor protocol"""
    if instance is None:
      return self
    getterFunction = self._getGetterFunction()
    return getterFunction(instance)


class NameTag:
  """Class requiring string types"""

  def __init__(self, name: str) -> None:
    if isinstance(name, str):
      self.name = name
    else:
      e = typeMsg('name', name, str)
      raise TypeError(e)


class TestTypeMsg(TestCase):
  """TestTypeMsg tests the typeMsg function."""

  def test_int(self) -> None:
    """Tests the typeMsg function."""
    try:
      IntOnly('hello')
    except BaseException as baseException:
      assert isinstance(baseException, TypeError)
      assert typeMsg('value', 'hello', int) == str(baseException)

  def test_callable(self) -> None:
    """Tests the typeMsg function."""
    try:
      class NameTag:
        """Class requiring string types"""

        __inner_name__ = 'NameTag'

        name = Descriptor()

        name.GET('LMAO')

        @name.GET
        def _getName(self) -> str:
          """Getter-function for the name"""
          return self.__inner_name__
    except BaseException as baseException:
      assert isinstance(baseException, TypeError)
      e = typeMsg('callMeMaybe', 'LMAO', FunctionType)
      assert e == str(baseException)

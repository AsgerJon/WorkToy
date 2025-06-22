"""
TestSome tests the 'Some' class from the worktoy.core module.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.core import Some

from typing import TYPE_CHECKING

from worktoy.core._some import _MetaSome, _InitSub
from worktoy.text import stringList
from worktoy.waitaminute import IllegalInstantiation


class TestSome(TestCase):
  """TestSome tests the 'Some' class from the worktoy.core module."""

  def test_is_instance(self) -> None:
    """
    Tests that Some correctly identifies everything other than 'None' as
    an instance of itself.
    """
    self.assertIsInstance(object, Some)
    self.assertIsInstance(object(), Some)
    self.assertIsInstance(69, Some)
    self.assertIsInstance('420', Some)
    self.assertIsInstance((80085,), Some)
    self.assertNotIsInstance(None, Some)
    self.assertIsInstance(Some, Some)

  def test_is_subclass(self) -> None:
    """
    Tests that Some correctly identifies every class other than 'NoneType'
    as a subclass of itself.
    """
    self.assertTrue(issubclass(object, Some))
    self.assertTrue(issubclass(int, Some))
    self.assertTrue(issubclass(float, Some))
    self.assertTrue(issubclass(complex, Some))
    self.assertTrue(issubclass(str, Some))
    self.assertTrue(issubclass(type('breh', (), {}), Some))
    self.assertTrue(issubclass(type, Some))
    self.assertFalse(issubclass(type(None), Some))

  def test_bad_subclass_check(self) -> None:
    """
    Tests that Some raises a TypeError when trying to check if a class
    is a subclass of Some with an invalid argument.
    """

    with self.assertRaises(TypeError) as context:
      issubclass('imma a type, trust!', Some)
    exception = context.exception
    expectedMessage = """arg 1 must be a class"""
    self.assertIn(expectedMessage, str(exception))

  def test_illegal_subclass(self) -> None:
    """
    Tests that 'Some' can't be subclassed.
    """
    with self.assertRaises(IllegalInstantiation) as context:
      class Sus(Some):
        """
        breh
        """
    exception = context.exception
    self.assertIs(exception.cls, _MetaSome)

  def test_deviant_subclass(self) -> None:
    """
    Tests that one can create a subclass of 'Some' by passing the '_root'
    keyword argument
    """

    class Sus(Some, _root=True):
      """
      breh
      """

    self.assertIsInstance(Sus, _MetaSome)

  def test_illegal_instantiation(self) -> None:
    """
    Tests that 'Some' can't be instantiated.
    """
    with self.assertRaises(IllegalInstantiation) as context:
      _ = Some()
    exception = context.exception
    self.assertIs(exception.cls, Some)

  def test_deviant_instantiation(self) -> None:
    """
    Tests that one can create an instance of 'Some' with 'type.__call__'.
    This is confirmed by instance checking the created instance against
    the _InitSub class.
    """
    sus = type.__call__(Some, )
    self.assertIsInstance(sus, _InitSub)

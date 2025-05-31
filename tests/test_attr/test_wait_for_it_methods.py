"""
TestWaitForItMethods tests classmethods, staticmethods and builtins.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.attr import WaitForIt

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False
if TYPE_CHECKING:
  from typing import Any, Self


class TrustMeBro:
  """
  Context manager where you assert nothing will go wrong.
  """

  def __enter__(self, ) -> Self:
    """
    Enter the context manager.
    """
    return self

  def __exit__(self, *args: Any) -> None:
    """
    Exit the context manager.
    """
    pass


class Foo:
  """
  Foo waits for a few attributes.
  """

  waitForClassMethod = WaitForIt(69, 420)
  waitForStaticmethod = WaitForIt(420, 69)
  waitForBuiltin = WaitForIt(callable, True)

  @classmethod
  @waitForClassMethod
  def _waiting(cls, *args: Any) -> Any:
    """
    A classmethod that does something.
    """
    return (*args,)

  @staticmethod
  @waitForStaticmethod
  def _waitingStatic(*args: Any) -> Any:
    """
    A staticmethod that does something.
    """
    return (*args,)


class TestWaitForItMethods(TestCase):
  """
  TestWaitForItMethods tests classmethods, staticmethods and builtins.
  """

  def setUp(self) -> None:
    """
    Set up the test case.
    """
    self.foo = Foo()

  def test_attr(self) -> None:
    """
    Test that descriptors actually exist on the class
    """
    self.assertIsInstance(Foo.waitForClassMethod, WaitForIt)
    self.assertIsInstance(Foo.waitForStaticmethod, WaitForIt)
    self.assertIsInstance(Foo.waitForBuiltin, WaitForIt)

  def test_init(self, ) -> None:
    """
    Test the initialization of the Foo class.
    """

"""
TestWaitForIt tests the WaitForIt descriptor.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.attr import Field, WaitForIt
from worktoy.mcls import BaseMeta
from worktoy.parse import maybe
from worktoy.static import overload
from worktoy.static.zeroton import THIS
from worktoy.waitaminute import ProtectedError, ReadOnlyError

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Any, Self


def waiting(*args: Any) -> Any:
  """
  Passthrough function
  """
  return (*args,)


class Foo:
  """
  Foo waits for a few attributes.
  """

  bar = WaitForIt(waiting, 69)
  baz = WaitForIt(69, 420)

  @baz
  def func(self, *args) -> Any:
    """
    A function that does something.
    """
    return (*args,)


class TestWaitForIt(TestCase):
  """
  TestWaitForIt tests the WaitForIt descriptor.
  """

  def setUp(self) -> None:
    """
    Set up the test case.
    """
    self.foo = Foo()

  def test_attr(self, ) -> None:
    """
    Tests that the 'WaitForIt' attributes does indeed exist.
    """
    self.assertIsInstance(Foo.bar, WaitForIt)
    self.assertIsInstance(Foo.baz, WaitForIt)

  def test_init(self, ) -> None:
    """
    Test the initialization of the Foo class.
    """
    self.assertIsInstance(self.foo, Foo)
    #
    self.assertIsInstance(self.foo.bar, tuple)
    self.assertIsInstance(self.foo.bar[0], int)
    self.assertAlmostEqual(self.foo.bar[0], 69)
    self.assertIsInstance(self.foo.baz, tuple)
    self.assertIsInstance(self.foo.baz[0], int)
    self.assertIsInstance(self.foo.baz[1], int)
    self.assertAlmostEqual(self.foo.baz[0], 69)
    self.assertAlmostEqual(self.foo.baz[1], 420)

  def test_bad_set(self) -> None:
    """
    Tests that setting raises ReadOnlyError.
    """
    with self.assertRaises(ReadOnlyError):
      self.foo.bar = 42

  def test_bad_delete(self) -> None:
    """
    Test that deleting raises ProtectedError.
    """
    with self.assertRaises(ProtectedError):
      del self.foo.bar

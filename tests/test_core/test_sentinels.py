"""
TestSentinels performs edge case focused testing of the 'Sentinel' classes
provided by the 'worktoy.core.sentinels' package.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from . import CoreTest
from worktoy.core.sentinels import DESC, THIS, OWNER, METACALL
from worktoy.core.sentinels import DELETED
from worktoy.core.sentinels import Sentinel, SentinelMeta
from worktoy.waitaminute.meta import IllegalInstantiation


class TestSentinels(CoreTest):
  """
  TestSentinels performs edge case focused testing of the 'Sentinel' classes
  provided by the 'worktoy.core.sentinels' package.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def setUp(self) -> None:
    self.sentinels = [
      THIS, OWNER, DESC, METACALL, DELETED,
    ]

  def test_recursion(self, ) -> None:
    """
    Tests the recursion protection
    """

    with self.assertRaises(KeyError) as context:
      _ = SentinelMeta.__new__(SentinelMeta, 'breh', (), {}, _recursion=True)
    e = context.exception
    self.assertEqual(str(e), str(KeyError('breh')))

  def test_str_repr(self) -> None:
    """
    Tests the string representation of a Sentinel
    """
    for sentinel in self.sentinels:
      self.assertEqual(str(sentinel), repr(sentinel))
      self.assertIsInstance(sentinel, SentinelMeta)

  def test_subclass_of_sentinel(self) -> None:
    """
    Every sentinel declared with 'class X(Sentinel)' really is a subclass
    of 'Sentinel'. This pins the fix where 'SentinelMeta.__new__' used to
    discard the declared bases on the first build.
    """
    for sentinel in self.sentinels:
      self.assertTrue(issubclass(sentinel, Sentinel))
      self.assertIn(Sentinel, sentinel.__mro__)

  def test_docstrings_survive(self) -> None:
    """
    The docstring written in each sentinel class body survives class
    creation. This pins the fix where 'SentinelMeta.__new__' used to
    discard the class namespace on the first build.
    """
    for sentinel in (Sentinel, *self.sentinels):
      self.assertIsNotNone(sentinel.__doc__)
      self.assertIn(sentinel.__name__, sentinel.__doc__)

  def test_registry_singleton(self) -> None:
    """
    A class statement reusing the name of a registered sentinel receives
    the existing sentinel instead of building a second one.
    """

    class THIS(Sentinel):  # noqa: F811
      pass

    self.assertIs(THIS, self.sentinels[0])

  def test_no_instantiation(self) -> None:
    """
    Calling a sentinel class raises 'IllegalInstantiation'.
    """
    for sentinel in (Sentinel, *self.sentinels):
      with self.assertRaises(IllegalInstantiation):
        sentinel()

"""
TestSentinelFamilyRegistry subclasses 'CoreTest' and pins that a
sentinel family built on a subclass of 'SentinelMeta' shares the one
registry of 'SentinelMeta'. The family used to keep a registry of its
own from its first sentinel on, so a second sentinel of a taken name was
accepted without a word when one of the two class statements went
through the family and the other through plain 'Sentinel'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core.sentinels import Sentinel, SentinelMeta
from worktoy.waitaminute.meta import DuplicateSentinel

from . import CoreTest


class TaskMeta(SentinelMeta):
  """A sentinel family of task states, built on 'SentinelMeta'."""


class AWAITING_REVIEW(metaclass=TaskMeta):
  """A task waiting for review, declared through the family."""


class ARCHIVED_TASK(Sentinel):
  """A task archived, declared through plain 'Sentinel'."""


#  The tests declare classes of the same names, which makes the names
#  local to each test, so they compare against these.
FAMILY_SENTINEL = AWAITING_REVIEW
PLAIN_SENTINEL = ARCHIVED_TASK


class TestSentinelFamilyRegistry(CoreTest):
  """
  TestSentinelFamilyRegistry provides tests for the registry a sentinel
  family shares with 'SentinelMeta'.
  """

  def test_plain_sentinel_after_family_refused(self) -> None:
    """A plain 'Sentinel' at a name the family holds is refused."""
    with self.assertRaises(DuplicateSentinel) as context:
      class AWAITING_REVIEW(Sentinel):  # noqa: F811
        """A second one, through plain 'Sentinel'."""
    self.assertIs(context.exception.existing, FAMILY_SENTINEL)

  def test_family_after_plain_sentinel_refused(self) -> None:
    """A family sentinel at a name a plain 'Sentinel' holds is refused."""
    with self.assertRaises(DuplicateSentinel) as context:
      class ARCHIVED_TASK(metaclass=TaskMeta):  # noqa: F811
        """A second one, through the family."""
    self.assertIs(context.exception.existing, PLAIN_SENTINEL)

  def test_one_registry(self) -> None:
    """The family and 'SentinelMeta' list the same sentinels, the
    library's own and both of this file."""
    family = TaskMeta._getRegisteredSentinels()
    root = SentinelMeta._getRegisteredSentinels()
    self.assertEqual(family, root)
    self.assertIn(AWAITING_REVIEW, root)
    self.assertIn(ARCHIVED_TASK, family)
    self.assertNotIn('__registered_sentinels__', TaskMeta.__dict__)

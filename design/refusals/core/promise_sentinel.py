"""
RefusedSentinel holds the refusals that belong with
'design.promises.core.promise_sentinel'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.core.sentinels import Sentinel, SentinelMeta
from worktoy.core.sentinels import DELETED, OWNER, THIS, DESC, METACALL
from worktoy.waitaminute.meta import IllegalInstantiation, DuplicateSentinel


class RefusedSentinel(TestCase):
  """
  Each of the following is refused, and the exception named is the one raised
  as of 1.2.3. A sentinel cannot be instantiated: calling one raises
  'IllegalInstantiation'. A second class statement at a taken sentinel name,
  'Sentinel' itself included, raises 'DuplicateSentinel'. Source: the
  docstrings of the 'sentinels' package, 'Sentinel' and 'SentinelMeta'.
  """

  def test_not_instantiable(self) -> None:
    class PROMISE_UNSET(Sentinel):
      pass

    with self.assertRaises(Exception) as refused:
      PROMISE_UNSET()
    self.assertIsInstance(refused.exception, IllegalInstantiation)

  def test_one_per_name(self) -> None:
    class PROMISE_TWICE(Sentinel):
      pass

    first = PROMISE_TWICE
    with self.assertRaises(Exception) as refused:
      class PROMISE_TWICE(Sentinel):
        pass
    self.assertIsInstance(refused.exception, DuplicateSentinel)

  def test_name_sentinel_taken(self) -> None:
    with self.assertRaises(Exception) as refused:
      class Sentinel(metaclass=SentinelMeta):
        pass
    self.assertIsInstance(refused.exception, DuplicateSentinel)

  def test_family(self) -> None:
    with self.assertRaises(Exception) as refused:
      class PROMISE_ON(Sentinel):
        pass
    self.assertIsInstance(refused.exception, DuplicateSentinel)

  def test_library_sentinels(self) -> None:
    for sentinel in (DELETED, OWNER, THIS, DESC, METACALL):
      with self.subTest(sentinel=sentinel):
        with self.assertRaises(Exception) as refused:
          sentinel()
        self.assertIsInstance(refused.exception, IllegalInstantiation)

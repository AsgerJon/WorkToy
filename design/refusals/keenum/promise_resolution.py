"""
RefusedResolution holds the refusals that belong with
'design.promises.keenum.promise_resolution'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.keenum import KeeNum, Kee
from worktoy.waitaminute import TypeException
from worktoy.waitaminute.keenum import KeeResolveError


class RefusedResolution(TestCase):
  """
  Each of the following is refused, and the exception named is the one raised
  as of 1.2.3. A miss raises 'KeeResolveError', holding the enumeration and
  the identifier. A call with several arguments, or with a keyword, raises
  'TypeError'. 'fromValue' raises 'TypeException' for a value of another type
  and 'KeeResolveError' when no member holds it. Source: the 'KeeMeta'
  docstring, "Member resolution", and the docstrings of '__class_resolve__'
  handling, 'fromValue' and '__getattr__'.
  """

  def makeRank(self) -> type:
    class Rank(KeeNum):
      LOW = Kee[int](2)
      MID = Kee[int](5)
      HIGH = Kee[int](9)

    return Rank

  def test_bool_refused_1(self) -> None:
    Rank = self.makeRank()
    with self.assertRaises(Exception) as refused:
      Rank(True)
    self.assertIsInstance(refused.exception, KeeResolveError)

  def test_bool_refused_2(self) -> None:
    Rank = self.makeRank()
    with self.assertRaises(Exception) as refused:
      Rank[True]
    self.assertIsInstance(refused.exception, KeeResolveError)

  def test_miss_1(self) -> None:
    Rank = self.makeRank()
    with self.assertRaises(Exception) as refused:
      Rank('nope')
    self.assertIsInstance(refused.exception, KeeResolveError)

  def test_miss_2(self) -> None:
    Rank = self.makeRank()
    with self.assertRaises(Exception) as refused:
      Rank(7)
    self.assertIsInstance(refused.exception, KeeResolveError)

  def test_call_arguments_1(self) -> None:
    Rank = self.makeRank()
    with self.assertRaises(Exception) as refused:
      Rank('low', 'mid')
    self.assertIsInstance(refused.exception, TypeError)

  def test_call_arguments_2(self) -> None:
    Rank = self.makeRank()
    with self.assertRaises(Exception) as refused:
      Rank(name='low')
    self.assertIsInstance(refused.exception, TypeError)

  def test_from_value_1(self) -> None:
    Rank = self.makeRank()
    with self.assertRaises(Exception) as refused:
      Rank.fromValue('9')
    self.assertIsInstance(refused.exception, TypeException)

  def test_from_value_2(self) -> None:
    Rank = self.makeRank()
    with self.assertRaises(Exception) as refused:
      Rank.fromValue(7)
    self.assertIsInstance(refused.exception, KeeResolveError)

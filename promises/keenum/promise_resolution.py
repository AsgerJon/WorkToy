"""
PromiseResolution promises how a 'KeeNum' finds a member, from
'worktoy.keenum'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.keenum import KeeNum, Kee
from worktoy.waitaminute import TypeException
from worktoy.waitaminute.keenum import KeeResolveError


class PromiseResolution(TestCase):
  """
  'Day(x)' and 'Day[x]' give a member in this order: the member itself,
  a name in any case, the answer of a classmethod '__class_resolve__'
  when the class defines one, a position for 'Day[x]' only, as list
  indexing with 'Day[-1]' the last, and then a value, the first member
  holding it. A 'bool' is no position and no value of an 'int'
  enumeration. A miss raises 'KeeResolveError', holding the enumeration
  and the identifier. A call takes exactly one argument and no keyword,
  or raises 'TypeError'. 'Day.monday' is 'Day.MONDAY'. 'fromValue' looks
  up a value alone, raising 'TypeException' for a value of another type
  and 'KeeResolveError' when no member holds it. Source: the 'KeeMeta'
  docstring, "Member resolution", and the docstrings of
  '__class_resolve__' handling, 'fromValue' and '__getattr__'.
  """

  def makeRank(self) -> type:
    class Rank(KeeNum):
      LOW = Kee[int](2)
      MID = Kee[int](5)
      HIGH = Kee[int](9)

    return Rank

  def test_order(self) -> None:
    Rank = self.makeRank()
    self.assertIs(Rank(Rank.MID), Rank.MID)
    self.assertIs(Rank('mid'), Rank.MID)
    self.assertIs(Rank('MID'), Rank.MID)
    self.assertIs(Rank[2], Rank.HIGH)
    self.assertIs(Rank(2), Rank.LOW)
    self.assertIs(Rank[-1], Rank.HIGH)
    self.assertIs(Rank[5], Rank.MID)

  def test_name_before_value(self) -> None:
    class Swapped(KeeNum):
      LOW = Kee[str]('high')
      HIGH = Kee[str]('low')

    class Twins(KeeNum):
      FIRST = Kee[int](1)
      SECOND = Kee[int](1)

    self.assertIs(Swapped('high'), Swapped.HIGH)
    self.assertIs(Twins(1), Twins.FIRST)
    self.assertIs(Twins('second'), Twins.SECOND)

  def test_class_resolve(self) -> None:
    class Level(KeeNum):
      LOW = Kee[int](1)
      HIGH = Kee[int](10)

      @classmethod
      def __class_resolve__(cls, identifier):
        if identifier == 'max':
          return cls.HIGH
        return NotImplemented

    self.assertIs(Level('max'), Level.HIGH)
    self.assertIs(Level('low'), Level.LOW)
    self.assertIs(Level(1), Level.LOW)

  def test_bool_refused(self) -> None:
    Rank = self.makeRank()
    with self.assertRaises(KeeResolveError):
      Rank(True)
    with self.assertRaises(KeeResolveError):
      Rank[True]

  def test_miss(self) -> None:
    Rank = self.makeRank()
    with self.assertRaises(KeeResolveError) as context:
      Rank('nope')
    self.assertIs(context.exception.keeNum, Rank)
    self.assertEqual(context.exception.identifier, 'nope')
    with self.assertRaises(KeeResolveError):
      Rank(7)

  def test_call_arguments(self) -> None:
    Rank = self.makeRank()
    with self.assertRaises(TypeError):
      Rank('low', 'mid')
    with self.assertRaises(TypeError):
      Rank(name='low')

  def test_attribute_any_case(self) -> None:
    Rank = self.makeRank()
    self.assertIs(Rank.low, Rank.LOW)

  def test_from_value(self) -> None:
    Rank = self.makeRank()
    self.assertIs(Rank.fromValue(9), Rank.HIGH)
    with self.assertRaises(TypeException):
      Rank.fromValue('9')
    with self.assertRaises(KeeResolveError):
      Rank.fromValue(7)

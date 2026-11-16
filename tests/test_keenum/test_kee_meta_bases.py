"""
TestKeeMetaBases tests an enumeration from 'worktoy.keenum' based on
several enumerations.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import KeeNum, Kee
from worktoy.waitaminute import DeprecatedPromise
from worktoy.waitaminute.keenum import KeeDuplicate, KeeTypeException
from . import KeenumTest


class TestKeeMetaBases(KeenumTest):
  """
  An enumeration may be based on several enumerations. It holds the
  members of its bases, the very objects, in the order of the bases, a
  member reached through two bases once, and its own members after
  them. Two different members under one name are refused with
  'KeeDuplicate', and bases of different value types with
  'KeeTypeException'. A position belongs to the class: an inherited
  member keeps the deprecated index it has in the class that declared
  it. The tests pin each, and the first enumeration base as 'base'.
  """

  def makeColors(self) -> tuple:
    class Color(KeeNum):
      RED = Kee[int](1)

    class Warm(Color):
      ORANGE = Kee[int](2)

    class Cool(Color):
      BLUE = Kee[int](3)

    return Color, Warm, Cool

  def test_members_of_every_base(self) -> None:
    Color, Warm, Cool = self.makeColors()

    class Mixed(Warm, Cool):
      PURPLE = Kee[int](4)

    expected = [Color.RED, Warm.ORANGE, Cool.BLUE, Mixed.PURPLE]
    self.assertEqual([*Mixed], expected)
    self.assertEqual(len(Mixed), 4)
    self.assertIs(Mixed.RED, Color.RED)
    self.assertIs(Mixed.BLUE, Cool.BLUE)
    self.assertIs(Mixed[2], Cool.BLUE)
    self.assertIs(Mixed[3], Mixed.PURPLE)
    self.assertIs(Mixed('blue'), Cool.BLUE)
    self.assertIs(Mixed(3), Cool.BLUE)
    self.assertIn(Cool.BLUE, Mixed)
    self.assertIsInstance(Cool.BLUE, Mixed)
    self.assertIs(Mixed.valueType, int)
    self.assertIs(Mixed.base, Warm)
    self.assertEqual(Mixed.mroNum, (Warm, Cool, Color))

  def test_position_belongs_to_the_class(self) -> None:
    Color, Warm, Cool = self.makeColors()

    class Mixed(Warm, Cool):
      PURPLE = Kee[int](4)

    self.assertIs(Cool[1], Cool.BLUE)
    self.assertIs(Mixed[2], Cool.BLUE)
    with self.assertWarns(DeprecatedPromise):
      self.assertEqual(Mixed.BLUE.index, 1)
    with self.assertWarns(DeprecatedPromise):
      self.assertEqual(Mixed.PURPLE.index, 3)

  def test_same_name_different_members_refused(self) -> None:
    class Left(KeeNum):
      X = Kee[int](1)

    class Right(KeeNum):
      X = Kee[int](2)

    with self.assertRaises(KeeDuplicate) as context:
      type(Left)('Both', (Left, Right), {})

    self.assertEqual(context.exception.clsName, 'Both')
    self.assertEqual(context.exception.name, 'X')
    self.assertIs(context.exception.oldMember, Left.X.kee)
    self.assertIs(context.exception.newMember, Right.X.kee)
    self.assertEqual(str(context.exception), str.join(' ', """Enumeration
      'Both' already contains member: '<Kee member: X>', and cannot take
      another member named 'X'! The names of the members of an
      enumeration must differ by more than their case, since a lookup by
      name ignores case.""".split()))

  def test_names_differing_by_case_refused(self) -> None:
    class Left(KeeNum, strictCase=False):
      mw = Kee[int](1)

    class Right(KeeNum):
      MW = Kee[int](2)

    for keywords in (dict(), dict(strictCase=False)):
      with self.subTest(keywords=keywords):
        with self.assertRaises(KeeDuplicate) as context:
          type(Left)('Both', (Left, Right), {}, **keywords)

        self.assertEqual(context.exception.clsName, 'Both')
        self.assertEqual(context.exception.name, 'MW')
        self.assertIs(context.exception.oldMember, Left.mw.kee)
        self.assertIs(context.exception.newMember, Right.MW.kee)
        self.assertIn("Enumeration 'Both' already contains member: "
                      "'<Kee member: mw>', and cannot take another "
                      "member named 'MW'!", str(context.exception))
        self.assertIn('must differ by more than their case',
                      str(context.exception))

  def test_one_member_in_another_case_through_two_bases(self) -> None:
    class Top(KeeNum, strictCase=False):
      mw = Kee[int](1)

    class Left(Top):
      pass

    class Right(Top):
      pass

    class Both(Left, Right):
      pass

    self.assertEqual([*Both], [Top.mw])
    self.assertIs(Both('MW'), Top.mw)

  def test_value_types_must_agree(self) -> None:
    class Number(KeeNum):
      ONE = Kee[int](1)

    class Word(KeeNum):
      TWO = Kee[str]('two')

    with self.assertRaises(KeeTypeException) as context:
      type(Number)('Both', (Number, Word), {})

    self.assertEqual(context.exception.name, 'TWO')
    self.assertEqual(context.exception.value, 'two')
    self.assertEqual(context.exception.expectedTypes, (int,))
    self.assertEqual(str(context.exception), str.join(' ', """Member 'TWO'
      has value 'two' of type 'str', but expected the value to be an
      instance of 'int'!""".split()))

  def test_bases_without_members(self) -> None:
    class Shape(KeeNum):
      pass

    class Tagged(KeeNum):
      pass

    class Polygon(Shape, Tagged):
      TRIANGLE = Kee[int](3)

    self.assertEqual([*Polygon], [Polygon.TRIANGLE])
    self.assertIn(Polygon.TRIANGLE, Shape)
    self.assertIn(Polygon.TRIANGLE, Tagged)
    self.assertIs(Polygon.base, Shape)

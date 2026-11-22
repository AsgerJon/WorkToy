"""
PromiseDeclaring promises how a 'KeeNum' enumeration is declared, from
'worktoy.keenum'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.keenum import KeeNum, Kee


class PromiseDeclaring(TestCase):
  """
  'class Day(KeeNum)' with 'MONDAY = Kee[str]('Mandag')' in its body declares
  a member 'MONDAY' whose value is built as 'str('Mandag')', so 'Kee[int]()'
  holds 0 and 'Kee[int]('3')' holds 3. A method in the body is a method of
  every member. Member names are upper case, values need not be unique, and a
  subclass holds the members of its base before its own. An entry that is no
  'Kee' stays an ordinary class attribute. Every value has the type of the
  first.

  The class keyword 'strictCase=False' on the class statement, as in 'class
  Unit(KeeNum, strictCase=False)', lets the body of that class name its
  members in any case, and a subclass takes the choice of its base unless it
  says 'strictCase=True' itself. 'strictCase=True' is the rule above spelled
  out. Promised from 1.2.2.

  Deprecated in 1.2.0, with its reason in 'design/promises/deprecations':
  'index' on a member. Source: the docstrings of 'Kee', 'KeeSpace',
  'KeeSpaceHook' and 'KeeMeta', and the 1.1.0 changelog. Source: the
  docstrings of 'KeeSpaceHook' and 'KeeDuplicate'.
  """

  def test_members(self) -> None:
    class Size(KeeNum):
      SMALL = Kee[int](1)
      MEDIUM = Kee[int](2)
      LARGE = Kee[int](2)
      unit = 'cm'

    self.assertEqual([m.name for m in Size], ['SMALL', 'MEDIUM', 'LARGE'])
    self.assertEqual([m.value for m in Size], [1, 2, 2])
    self.assertEqual(Size.unit, 'cm')

  def test_methods_and_constructed_values(self) -> None:
    class Day(KeeNum):
      MONDAY = Kee[str]('Mandag')
      SATURDAY = Kee[str]('Lordag')

      def isWeekend(self) -> bool:
        return self is Day.SATURDAY

    class Counter(KeeNum):
      ZERO = Kee[int]()
      THREE = Kee[int]('3')

    self.assertFalse(Day.MONDAY.isWeekend())
    self.assertTrue(Day.SATURDAY.isWeekend())
    self.assertEqual((Counter.ZERO.value, Counter.THREE.value), (0, 3))

  def test_inherited_first(self) -> None:
    class Size(KeeNum):
      SMALL = Kee[int](1)

    class BigSize(Size):
      HUGE = Kee[int](9)

    self.assertEqual([m.name for m in BigSize], ['SMALL', 'HUGE'])
    self.assertIs(BigSize.SMALL, Size.SMALL)

  def test_any_case_by_keyword(self) -> None:
    class Unit(KeeNum, strictCase=False):
      mm = Kee[float](0.001)
      Cm = Kee[float](0.01)
      KM = Kee[float](1000.0)

    self.assertEqual([m.name for m in Unit], ['mm', 'Cm', 'KM'])
    self.assertEqual(Unit.mm.value, 0.001)

  def test_keyword_inherited(self) -> None:
    class Metric(KeeNum, strictCase=False):
      mm = Kee[float](0.001)

    class Imperial(Metric):
      inch = Kee[float](0.0254)

    self.assertEqual([m.name for m in Imperial], ['mm', 'inch'])

"""
PromiseDeclaring promises how a 'KeeNum' enumeration is declared, from
'worktoy.keenum'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.keenum import KeeNum, Kee
from worktoy.waitaminute.keenum import KeeCaseException, KeeDuplicate
from worktoy.waitaminute.keenum import KeeTypeException, KeeMemberNameError
from worktoy.waitaminute.meta import ShadowedClassHook


class PromiseDeclaring(TestCase):
  """
  'class Day(KeeNum)' with 'MONDAY = Kee[str]('Mandag')' in its body
  declares a member 'MONDAY' whose value is built as 'str('Mandag')', so
  'Kee[int]()' holds 0 and 'Kee[int]('3')' holds 3. A method in the body
  is a method of every member. Member names are upper case, values need
  not be unique, and a subclass holds the members of its base before
  its own.
  An entry that is no 'Kee' stays an ordinary class attribute. Every
  value has the type of the first. As the class is created, a name not
  upper case raises 'KeeCaseException', a second type
  'KeeTypeException', a name declared twice 'KeeDuplicate', a plain value
  at a member's name 'KeeMemberNameError', a 'Kee' without parentheses
  or in the body of a class that is no enumeration 'TypeError', wrapped
  in 'RuntimeError' before Python 3.12, and a class hook of an operation
  the enumeration owns, as '__class_len__', 'ShadowedClassHook'. Source:
  the docstrings of 'Kee', 'KeeSpace', 'KeeSpaceHook' and 'KeeMeta', and
  the 1.1.0 changelog.

  Deprecated in 1.2.0, with its reason in 'promises/deprecations':
  'index' on a member.
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

  def test_refusals(self) -> None:
    with self.assertRaises(KeeCaseException) as context:
      class Lower(KeeNum):
        small = Kee[int](1)
    self.assertEqual(context.exception.name, 'small')
    with self.assertRaises(KeeTypeException) as context:
      class Mixed(KeeNum):
        A = Kee[int](1)
        B = Kee[str]('b')
    self.assertEqual(context.exception.name, 'B')
    self.assertEqual(context.exception.value, 'b')
    self.assertEqual(context.exception.expectedTypes, (int,))
    with self.assertRaises(KeeDuplicate) as context:
      class Twice(KeeNum):
        A = Kee[int](1)
        A = Kee[int](2)
    self.assertEqual(context.exception.name, 'A')
    with self.assertRaises(KeeMemberNameError) as context:
      class Overwritten(KeeNum):
        A = Kee[int](1)
        A = 3
    self.assertEqual(context.exception.clsName, 'Overwritten')
    self.assertEqual(context.exception.memberName, 'A')

  def test_misplaced_kee(self) -> None:
    for case in ('bare', 'plain class'):
      with self.subTest(case=case):
        with self.assertRaises((TypeError, RuntimeError)) as context:
          if case == 'bare':
            class Bare(KeeNum):
              A = Kee[int]
          else:
            class Plain:
              A = Kee[int](1)
        refusal = context.exception.__cause__ or context.exception
        self.assertIsInstance(refusal, TypeError)

  def test_owned_hook(self) -> None:
    with self.assertRaises(ShadowedClassHook) as context:
      class Counted(KeeNum):
        A = Kee[int](1)

        @classmethod
        def __class_len__(cls) -> int:
          return 3
    self.assertEqual(context.exception.hookName, '__class_len__')

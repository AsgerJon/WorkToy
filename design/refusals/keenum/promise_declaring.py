"""
RefusedDeclaring holds the refusals that belong with
'design.promises.keenum.promise_declaring'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.keenum import KeeNum, Kee
from worktoy.waitaminute import TypeException
from worktoy.waitaminute.keenum import KeeCaseException, KeeDuplicate
from worktoy.waitaminute.keenum import KeeTypeException, KeeMemberNameError
from worktoy.waitaminute.meta import ShadowedClassHook, ReservedName


class RefusedDeclaring(TestCase):
  """
  Each of the following is refused, and the exception named is the one raised
  as of 1.2.3. As the class is created, a name not upper case raises
  'KeeCaseException', a second type 'KeeTypeException', a name declared twice
  'KeeDuplicate', a plain value at a member's name 'KeeMemberNameError', a
  'Kee' without parentheses or in the body of a class that is no enumeration
  'TypeError', wrapped in 'RuntimeError' before Python 3.12, and a class hook
  of an operation the enumeration owns, as '__class_len__',
  'ShadowedClassHook'. A 'strictCase' that is no 'bool' raises
  'TypeException', whether or not the body declares a member. Whatever their
  case, two members may not differ by the case of their names alone, since a
  lookup by name ignores case: the second raises 'KeeDuplicate', holding the
  name of the enumeration, the name refused and both declarations. A class
  that names its members in any case may not name one as something a base or
  the metaclass holds already, as 'members' or a method of a base: such a
  member raises 'ReservedName', a 'SyntaxError' holding the name. Source: the
  docstrings of 'Kee', 'KeeSpace', 'KeeSpaceHook' and 'KeeMeta', and the
  1.1.0 changelog. Source: the docstrings of 'KeeSpaceHook' and
  'KeeDuplicate'.
  """

  def test_refusals_1(self) -> None:
    with self.assertRaises(Exception) as refused:
      class Lower(KeeNum):
        small = Kee[int](1)
    self.assertIsInstance(refused.exception, KeeCaseException)

  def test_refusals_2(self) -> None:
    with self.assertRaises(Exception) as refused:
      class Mixed(KeeNum):
        A = Kee[int](1)
        B = Kee[str]('b')
    self.assertIsInstance(refused.exception, KeeTypeException)

  def test_refusals_3(self) -> None:
    with self.assertRaises(Exception) as refused:
      class Twice(KeeNum):
        A = Kee[int](1)
        A = Kee[int](2)
    self.assertIsInstance(refused.exception, KeeDuplicate)

  def test_refusals_4(self) -> None:
    with self.assertRaises(Exception) as refused:
      class Overwritten(KeeNum):
        A = Kee[int](1)
        A = 3
    self.assertIsInstance(refused.exception, KeeMemberNameError)

  def test_any_case_by_keyword_1(self) -> None:
    with self.assertRaises(Exception) as refused:
      class Strict(KeeNum, strictCase=True):
        small = Kee[int](1)
    self.assertIsInstance(refused.exception, KeeCaseException)

  def test_any_case_by_keyword_2(self) -> None:
    with self.assertRaises(Exception) as refused:
      class Vague(KeeNum, strictCase='no'):
        A = Kee[int](1)
    self.assertIsInstance(refused.exception, TypeException)

  def test_any_case_by_keyword_3(self) -> None:
    with self.assertRaises(Exception) as refused:
      class Empty(KeeNum, strictCase='no'):
        pass
    self.assertIsInstance(refused.exception, TypeException)

  def test_names_differ_by_more_than_case(self) -> None:
    with self.assertRaises(Exception) as refused:
      class Power(KeeNum, strictCase=False):
        mW = Kee[float](0.001)
        MW = Kee[float](1000000.0)
    self.assertIsInstance(refused.exception, KeeDuplicate)

  def test_keyword_inherited(self) -> None:
    class Metric(KeeNum, strictCase=False):
      mm = Kee[float](0.001)

    with self.assertRaises(Exception) as refused:
      class Strict(Metric, strictCase=True):
        ft = Kee[float](0.3048)
    self.assertIsInstance(refused.exception, KeeCaseException)

  def test_names_of_the_class_refused_1(self) -> None:
    with self.assertRaises(Exception) as refused:
      class Role(KeeNum, strictCase=False):
        guests = Kee[int](1)
        members = Kee[int](2)
    self.assertIsInstance(refused.exception, ReservedName)

  def test_names_of_the_class_refused_2(self) -> None:
    class Unit(KeeNum, strictCase=False):
      mm = Kee[float](0.001)

      def describe(self) -> str:
        return self.name

    with self.assertRaises(Exception) as refused:
      class Imperial(Unit):
        describe = Kee[float](1.0)
    self.assertIsInstance(refused.exception, ReservedName)

  def test_owned_hook(self) -> None:
    with self.assertRaises(Exception) as refused:
      class Counted(KeeNum):
        A = Kee[int](1)

        @classmethod
        def __class_len__(cls) -> int:
          return 3
    self.assertIsInstance(refused.exception, ShadowedClassHook)

  def test_misplaced_kee(self) -> None:
    for case in ('bare', 'plain class'):
      with self.subTest(case=case):
        with self.assertRaises(Exception) as refused:
          if case == 'bare':
            class Bare(KeeNum):
              A = Kee[int]
          else:
            class Plain:
              A = Kee[int](1)
        self.assertIsInstance(refused.exception, (TypeError, RuntimeError))

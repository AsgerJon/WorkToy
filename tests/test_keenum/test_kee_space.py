"""
TestKeeSpace tests 'KeeSpace' from 'worktoy.keenum'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import KeeNum, Kee, KeeSpace, KeeMeta
from worktoy.mcls import BaseObject, BaseSpace
from worktoy.waitaminute.keenum import KeeDuplicate, KeeNameConflict
from worktoy.waitaminute.keenum import KeeTypeException, KeeCaseException
from . import KeenumTest, WeekDay


class TestKeeSpace(KeenumTest):
  """
  'KeeSpace' records the members of one body in order, inherited
  members first as clones, every name once, every value of one type,
  and writes the pinned value type into the class. The tests pin the
  records, each refusal, the inheritance from enumerations and the
  passing over of other bases, on class statements and by hand.
  """

  def test_records_in_order(self) -> None:
    space = WeekDay.__namespace__
    self.assertIsInstance(space, KeeSpace)
    self.assertIsInstance(space, BaseSpace)
    names = [*space.__enumeration_members__]
    self.assertEqual(names, [m.name for m in WeekDay])
    self.assertIs(space.__member_type__, str)
    self.assertIs(WeekDay.__dict__['__member_type__'], str)
    self.assertTrue(space.hasNum('MONDAY'))
    self.assertFalse(space.hasNum('monday'))
    self.assertFalse(space.hasNum('language'))

  def test_add_num_by_hand(self) -> None:
    space = KeeSpace(KeeMeta, 'Hand', ())
    self.assertIsNone(space.__member_type__)
    first = Kee[int](1)
    space.addNum('A', first)
    self.assertEqual(first.name, 'A')
    self.assertIs(space.__member_type__, int)
    self.assertIs(space.__enumeration_members__['A'], first)
    named = Kee[int](2)
    named.name = 'B'
    space.addNum('B', named)
    self.assertIs(space.typeGuard(named), named)
    compiled = space.compile()
    self.assertIs(compiled['__member_type__'], int)

  def test_duplicate_name_refused(self) -> None:
    with self.assertRaises(KeeDuplicate) as context:
      class Local(KeeNum):
        A = Kee[int](1)
        A = Kee[int](2)

    exception = context.exception
    self.assertEqual(exception.name, 'A')
    self.assertEqual(exception.oldMember.getPosArgs(), (1,))
    self.assertEqual(exception.newMember.getPosArgs(), (2,))
    self.assertIn("'A'", str(exception))

  def test_inherited_name_refused(self) -> None:
    class Base(KeeNum):
      A = Kee[int](1)

    with self.assertRaises(KeeDuplicate) as context:
      class Sub(Base):
        A = Kee[int](2)

    self.assertEqual(context.exception.name, 'A')
    self.assertIsNot(context.exception.oldMember, Base.A.kee)
    self.assertEqual(context.exception.oldMember.name, 'A')
    self.assertEqual(context.exception.newMember.getPosArgs(), (2,))
    self.assertIn("Enumeration name 'A' already contains member",
                  str(context.exception))

  def test_name_conflict_refused(self) -> None:
    with self.assertRaises(KeeNameConflict) as context:
      class Local(KeeNum):
        A = Kee[int](1)
        B = A

    exception = context.exception
    self.assertEqual(exception.oldName, 'A')
    self.assertEqual(exception.newName, 'B')
    self.assertEqual(exception.member.name, 'A')
    self.assertIn("'B'", str(exception))

  def test_lower_case_refused(self) -> None:
    with self.assertRaises(KeeCaseException) as context:
      class Local(KeeNum):
        red = Kee[int](1)

    self.assertEqual(context.exception.name, 'red')
    self.assertIn("must have upper case names, but received: 'red'",
                  str(context.exception))

  def test_second_type_refused(self) -> None:
    with self.assertRaises(KeeTypeException) as context:
      class Local(KeeNum):
        A = Kee[int](1)
        B = Kee[str]('b')

    exception = context.exception
    self.assertEqual(exception.name, 'B')
    self.assertEqual(exception.value, 'b')
    self.assertEqual(exception.expectedTypes, (int,))
    self.assertIn("'int'", str(exception))

  def test_subclass_values_of_the_pinned_type(self) -> None:
    class Base(KeeNum):
      A = Kee[int](1)

    with self.assertRaises(KeeTypeException) as context:
      class Sub(Base):
        B = Kee[bool](True)

    self.assertEqual(context.exception.name, 'B')
    self.assertIs(context.exception.value, True)
    self.assertEqual(context.exception.expectedTypes, (int,))
    self.assertIn("'B' has value 'True' of type 'bool'",
                  str(context.exception))

    class Fine(Base):
      B = Kee[int](True)

    self.assertIs(Fine.B.value, True)
    self.assertIs(Fine.valueType, int)

  def test_inherits_from_every_enumeration_base(self) -> None:
    class Base(KeeNum):
      A = Kee[int](1)

    class Plain:
      A = 'mixin'

    class Boxed(BaseObject):
      A = 'object'

    space = KeeSpace(KeeMeta, 'Hand', (Plain, Boxed, Base))
    self.assertEqual([*space.__enumeration_members__], ['A'])
    self.assertIs(space.__member_type__, int)
    clone = space.__enumeration_members__['A']
    self.assertIsNot(clone, Base.A.kee)
    self.assertEqual(clone.name, 'A')
    self.assertEqual(clone.getPosArgs(), (1,))
    empty = KeeSpace(KeeMeta, 'Hand', (Plain, Boxed))
    self.assertEqual(empty.__enumeration_members__, {})
    self.assertIsNone(empty.__member_type__)

  def test_two_bases_with_one_name_refused(self) -> None:
    class Left(KeeNum):
      A = Kee[int](1)

    class Right(KeeNum):
      A = Kee[int](2)

    with self.assertRaises(KeeDuplicate) as context:
      KeeSpace(KeeMeta, 'Hand', (Left, Right))
    self.assertEqual(context.exception.name, 'A')
    self.assertEqual(context.exception.oldMember.getPosArgs(), (1,))
    self.assertEqual(context.exception.newMember.getPosArgs(), (2,))
    self.assertIn("Enumeration name 'A' already contains member",
                  str(context.exception))

  def test_random_members(self) -> None:
    space = KeeSpace(KeeMeta, 'Hand', ())
    self.randomWord.size = 6
    words = [*dict.fromkeys(self.randomWord.row)]
    for word in words:
      space.addNum(word.upper(), Kee[str](word))
    self.assertEqual([*space.__enumeration_members__],
                     [w.upper() for w in words])
    for word in words:
      with self.subTest(word=word):
        self.assertTrue(space.hasNum(word.upper()))
        self.assertFalse(space.hasNum(word))

  def test_name_conflict_by_equality(self) -> None:
    space = KeeSpace(KeeMeta, 'Hand', ())
    kee = Kee[int](1)
    space.addNum('B', kee)
    with self.assertRaises(KeeNameConflict) as context:
      space.addNum('A', kee)
    self.assertIs(context.exception.member, kee)
    self.assertEqual(context.exception.oldName, 'B')
    self.assertEqual(context.exception.newName, 'A')
    self.assertIn("existing name 'B' versus new name 'A'",
                  str(context.exception))
    named = Kee[int](2)
    named.name = str.join('', ['R', 'ED'])
    space.addNum('RED', named)
    self.assertTrue(space.hasNum('RED'))

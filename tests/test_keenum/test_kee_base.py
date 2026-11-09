"""
TestKeeBase tests 'KeeBase' from 'worktoy.keenum', the members of an
enumeration.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import copy
import pickle

from worktoy.core import Object
from worktoy.desc import AttriBox
from worktoy.keenum import KeeBase, KeeNum, Kee
from worktoy.utilities import typeCast
from worktoy.waitaminute.dispatch import TypeCastException
from worktoy.waitaminute.keenum import KeeWriteOnceError
from . import KeenumTest, WeekDay, Bag


class TestKeeBase(KeenumTest):
  """
  A member is one object built once, holding the name, index, value and
  value type its 'Kee' gave, equal to itself alone, hashing where its
  value hashes, surviving copies and pickling as itself, and refusing
  every change. It is a plain object, not a worktoy 'Object', so a box
  leaves it untagged and another class body holds it as an ordinary
  class attribute. The tests pin each promise on the members of the
  fixtures and on members placed in other class bodies.
  """

  def test_answers_through_its_kee(self) -> None:
    member = WeekDay.WEDNESDAY
    self.assertIsInstance(member, KeeBase)
    self.assertNotIsInstance(member, Object)
    self.assertEqual(member.name, 'WEDNESDAY')
    self.assertEqual(member.index, 2)
    self.assertEqual(member.value, 'onsdag')
    self.assertIs(member.valueType, str)
    self.assertIs(member.kee, WeekDay.__namespace__.__enumeration_members__
                  ['WEDNESDAY'])
    self.assertEqual(int(member), 2)
    self.assertEqual(['a', 'b', 'c'][member], 'c')

  def test_frozen(self) -> None:
    member = WeekDay.MONDAY
    with self.assertRaises(KeeWriteOnceError) as context:
      member.extra = 1
    exception = context.exception
    self.assertIs(exception.member, member)
    self.assertIs(exception.keeNum, WeekDay)
    self.assertEqual(exception.attribute, 'extra')
    self.assertIn("'extra'", str(exception))
    self.assertIn("'WeekDay.MONDAY' in 'WeekDay'", str(exception))
    with self.assertRaises(KeeWriteOnceError) as context:
      del member.extra
    self.assertIs(context.exception.member, member)
    self.assertIs(context.exception.keeNum, WeekDay)
    self.assertEqual(context.exception.attribute, 'extra')
    self.assertIn("'extra'", str(context.exception))
    with self.assertRaises(KeeWriteOnceError) as context:
      member.__field_kee__ = None
    self.assertIs(context.exception.member, member)
    self.assertIs(context.exception.keeNum, WeekDay)
    self.assertEqual(context.exception.attribute, '__field_kee__')
    self.assertIn("'__field_kee__'", str(context.exception))

  def test_equality_is_identity(self) -> None:
    self.assertEqual(WeekDay.MONDAY, WeekDay.MONDAY)
    self.assertNotEqual(WeekDay.MONDAY, WeekDay.TUESDAY)
    self.assertIs(WeekDay.MONDAY.__eq__(Bag.FEW), NotImplemented)
    self.assertFalse(WeekDay.MONDAY == Bag.FEW)
    self.assertFalse(WeekDay.MONDAY == 'mandag')
    self.assertTrue(WeekDay.MONDAY != 'mandag')

  def test_hash_follows_the_value(self) -> None:
    self.assertEqual(hash(WeekDay.MONDAY), hash(WeekDay.MONDAY))
    self.assertNotEqual(hash(WeekDay.MONDAY), hash(WeekDay.TUESDAY))
    #  The hash of an integer is the same in every process, unlike that of
    #  a string, so a member hashes alike from one run to the next.
    expected = hash(int.from_bytes(b'WeekDay::MONDAY', 'big'))
    self.assertEqual(hash(WeekDay.MONDAY), expected)
    self.assertEqual({WeekDay.MONDAY: 1}[WeekDay.MONDAY], 1)
    with self.assertRaises(TypeError) as context:
      hash(Bag.FEW)
    self.assertIn('unhashable', str(context.exception))
    self.assertIn("'Bag.FEW'", str(context.exception))
    self.assertIsInstance(context.exception.__cause__, TypeError)
    with self.assertRaises(TypeError) as context:
      _ = {Bag.FEW: 1}
    self.assertIn('unhashable', str(context.exception))
    self.assertIn("'Bag.FEW'", str(context.exception))

  def test_copies_are_the_member(self) -> None:
    self.assertIs(copy.copy(WeekDay.FRIDAY), WeekDay.FRIDAY)
    self.assertIs(copy.deepcopy(WeekDay.FRIDAY), WeekDay.FRIDAY)
    self.assertIs(copy.deepcopy([WeekDay.FRIDAY])[0], WeekDay.FRIDAY)
    self.assertIs(copy.deepcopy(Bag.MANY), Bag.MANY)

  def test_pickles_as_itself(self) -> None:
    for member in WeekDay:
      with self.subTest(member=member.name):
        self.assertIs(pickle.loads(pickle.dumps(member)), member)
    self.assertIs(pickle.loads(pickle.dumps(Bag.SAME)), Bag.SAME)

  def test_text(self) -> None:
    self.assertEqual(str(WeekDay.SATURDAY), 'WeekDay.SATURDAY')
    self.assertEqual(repr(WeekDay.SATURDAY), 'WeekDay.SATURDAY')
    self.assertEqual('%s' % Bag.MANY, 'Bag.MANY')

  def test_placed_in_a_class_body(self) -> None:
    class Holder:
      day = WeekDay.THURSDAY

    holder = Holder()
    self.assertIs(holder.day, WeekDay.THURSDAY)
    self.assertIs(Holder.day, WeekDay.THURSDAY)
    holder.day = WeekDay.FRIDAY
    self.assertIs(holder.day, WeekDay.FRIDAY)
    self.assertIs(Holder.day, WeekDay.THURSDAY)
    del holder.day
    self.assertIs(holder.day, WeekDay.THURSDAY)
    self.assertNotIn('__field_owner__', vars(WeekDay.THURSDAY))
    self.assertNotIn('__field_name__', vars(WeekDay.THURSDAY))

  def test_cast_hook(self) -> None:
    self.assertIs(typeCast(WeekDay, 'monday'), WeekDay.MONDAY)
    self.assertIs(typeCast(WeekDay, 'fredag'), WeekDay.FRIDAY)
    self.assertIs(typeCast(WeekDay, WeekDay.SUNDAY), WeekDay.SUNDAY)
    with self.assertRaises(TypeCastException) as context:
      typeCast(WeekDay, 'nothing')
    self.assertIs(context.exception.type_, WeekDay)
    self.assertEqual(context.exception.arg, 'nothing')
    self.assertEqual(str(context.exception),
                     "Unable to cast value 'nothing' to type 'WeekDay'!")
    self.assertIs(WeekDay.__cast_as__('nothing'), NotImplemented)
    type.__setattr__(WeekDay, '__allow_instantiation__', True)
    try:
      self.assertIs(WeekDay.__cast_as__('monday'), NotImplemented)
    finally:
      type.__setattr__(WeekDay, '__allow_instantiation__', False)
    self.assertIs(WeekDay.__cast_as__('monday'), WeekDay.MONDAY)

  def test_box_leaves_a_member_untagged(self) -> None:
    class Local(KeeNum):
      A = Kee[int](1)
      B = Kee[int](2)

    class Holder(Object):
      built = AttriBox[Local]('A')
      given = AttriBox[Local](Local.B)

    holder = Holder()
    self.assertIs(holder.built, Local.A)
    self.assertIs(holder.given, Local.B)
    self.assertNotIn('__field_box__', Local.A.__dict__)
    self.assertNotIn('__field_name__', Local.A.__dict__)
    self.assertNotIn('__field_box__', Local.B.__dict__)
    self.assertEqual(str(Local.A), 'Local.A')
    self.assertIs(pickle.loads(pickle.dumps(Local.A.name)), 'A')

  def test_random_members(self) -> None:
    self.randomWord.size = 5
    words = [*dict.fromkeys(self.randomWord.row)]
    space = {word.upper(): Kee[str](word) for word in words}
    Local = type(WeekDay)('Local', (KeeNum,), space)
    for index, word in enumerate(words):
      member = getattr(Local, word.upper())
      with self.subTest(word=word):
        self.assertEqual(member.index, index)
        self.assertEqual(member.value, word)
        self.assertEqual(str(member), 'Local.%s' % word.upper())
        self.assertIs(copy.copy(member), member)

"""
TestKeeMetaBuild tests how 'KeeMeta' from 'worktoy.keenum' prepares,
creates and initializes an enumeration.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from collections.abc import Callable

from worktoy.keenum import KeeMeta, KeeNum, Kee, KeeSpace
from worktoy.mcls import BaseObject
from worktoy.waitaminute import TypeException, DeprecatedPromise
from worktoy.waitaminute.desc import SharedDescriptor
from . import KeenumTest, WeekDay, Shade, Bag


class TestKeeMetaBuild(KeenumTest):
  """
  '__prepare__' returns a 'KeeSpace', '__init__' runs the creators in
  order and hands over to 'BaseMeta' last, so '__class_init__' sees the
  members. The tests pin the namespace, the base and the resolution
  order of enumerations, the members and the two caches, the peek of
  every lazy getter, the validation of '__class_resolve__', and the
  refusals of the bases.
  """

  def test_prepare(self) -> None:
    space = KeeMeta.__prepare__('Hand', (WeekDay,), tag=1)
    self.assertIsInstance(space, KeeSpace)
    self.assertIs(space.getMetaclass(), KeeMeta)
    self.assertEqual(space.getKwargs(), {'tag': 1})
    self.assertTrue(space.hasNum('MONDAY'))

  def test_built_by_call(self) -> None:
    Local = KeeMeta('Local', (KeeNum,), {'A': Kee[int](1), 'x': 'plain'})
    self.assertIsInstance(Local.__namespace__, KeeSpace)
    self.assertEqual([m.name for m in Local], ['A'])
    self.assertEqual(Local.x, 'plain')
    self.assertIs(Local.space, Local.__namespace__)
    self.assertIs(Local.base, Local)

  def test_base_and_resolution_order(self) -> None:
    class Sub(WeekDay):
      HOLIDAY = Kee[str]('fridag')

    class Deep(Sub):
      pass

    self.assertIs(WeekDay.base, WeekDay)
    self.assertEqual(WeekDay.mroNum, ())
    self.assertIs(Sub.base, WeekDay)
    self.assertEqual(Sub.mroNum, (WeekDay,))
    self.assertIs(Deep.base, Sub)
    self.assertEqual(Deep.mroNum, (Sub, WeekDay))
    self.assertEqual(len(Deep), 8)
    self.assertIs(Deep.HOLIDAY, Sub.HOLIDAY)

  def test_mixins_are_no_bases(self) -> None:
    class Plain:
      tag = 'plain'

    class Boxed(BaseObject):
      tag = 'boxed'

    class Mixed(Plain, WeekDay):
      pass

    class Objected(Boxed, WeekDay):
      pass

    self.assertIs(Mixed.base, WeekDay)
    self.assertIs(Objected.base, WeekDay)
    self.assertEqual(Mixed.tag, 'plain')
    self.assertEqual(Objected.tag, 'boxed')
    self.assertIs(Mixed.MONDAY, WeekDay.MONDAY)

  def test_several_enumeration_bases(self) -> None:
    class Left(KeeNum):
      A = Kee[int](1)

    class Right(KeeNum):
      B = Kee[int](2)

    class Both(Left, Right):
      pass

    self.assertEqual([*Both], [Left.A, Right.B])
    self.assertIs(Both.base, Left)
    self.assertEqual(Both.mroNum, (Left, Right))

  def test_no_enumeration_base_refused(self) -> None:
    with self.assertRaises(ValueError) as context:
      KeeMeta('Loose', (), {})
    self.assertIn("based on 'KeeMeta.keeNum'", str(context.exception))
    self.assertIn("'Loose' has the bases: ()", str(context.exception))

  def test_namespace_must_be_a_kee_space(self) -> None:
    class Local(KeeNum):
      A = Kee[int](1)

    kept = Local.__namespace__
    Local.__namespace__ = {}
    try:
      with self.assertRaises(TypeException) as context:
        Local._createSpace()
    finally:
      Local.__namespace__ = kept
    self.assertEqual(context.exception.varName, '__namespace__')
    self.assertEqual(context.exception.actualObject, {})
    self.assertIs(context.exception.actualType, dict)
    self.assertEqual(context.exception.expectedTypes, (KeeSpace,))
    self.assertIn("'__namespace__'", str(context.exception))
    self.assertIn("'KeeSpace'", str(context.exception))

  def test_members_built_in_order(self) -> None:
    with self.assertWarns(DeprecatedPromise):
      self.assertEqual([m.index for m in WeekDay], [*range(7)])
    self.assertEqual(WeekDay.members, (*WeekDay,))
    self.assertIs(type(WeekDay.members), tuple)
    for member in WeekDay:
      with self.subTest(member=member.name):
        self.assertIs(WeekDay.__dict__[member.name], member)
        self.assertIs(member.kee.getFieldOwner(), WeekDay)

  def test_plain_base_attribute_gives_way(self) -> None:
    class Base(KeeNum):
      A = Kee[int](1)
      COLOR = 'plain'

    class Sub(Base):
      COLOR = Kee[int](2)

    self.assertEqual(Base.COLOR, 'plain')
    self.assertEqual(Sub.COLOR.value, 2)
    with self.assertWarns(DeprecatedPromise):
      self.assertEqual(Sub.COLOR.index, 1)
    self.assertIsNone(Sub._getInheritedMember('COLOR'))
    self.assertIs(Sub._getInheritedMember('A'), Base.A)
    self.assertIsNone(Sub._getInheritedMember('absent'))

  def test_kee_placed_on_two_enumerations_refused(self) -> None:
    shared = Kee[int](1)

    class One(KeeNum):
      A = shared

    with self.assertRaises(SharedDescriptor) as context:
      class Two(KeeNum):
        A = shared

    self.assertIs(context.exception.desc, shared)
    self.assertIs(context.exception.owner, One)
    self.assertEqual(context.exception.fieldName, 'A')
    self.assertEqual(context.exception.newOwner.__name__, 'Two')
    self.assertEqual(context.exception.newName, 'A')
    self.assertIn("The 'Kee' at 'One.A' is placed again at 'Two.A'",
                  str(context.exception))
    self.assertIs(One.A.kee, shared)

  def test_kee_without_parentheses_refused(self) -> None:
    with self.assertRaises(TypeError) as context:
      class Local(KeeNum):
        A = Kee[int]

    self.assertIn("The box at 'Local.A' is declared without parentheses",
                  str(context.exception))
    self.assertIn("'Kee[int]()'", str(context.exception))

  def test_caches(self) -> None:
    self.assertEqual(WeekDay.namedMembers,
                     {m.name.lower(): m for m in WeekDay})
    self.assertEqual(WeekDay.valuedMembers,
                     {m.value: m for m in WeekDay})
    self.assertEqual(Bag.valuedMembers, {'__unhashable__': [1]})

    class Twice(KeeNum):
      A = Kee[int](1)
      B = Kee[int](1)

    self.assertEqual(Twice.valuedMembers, {1: Twice.A})

  def test_value_type(self) -> None:
    self.assertIs(WeekDay.valueType, str)
    self.assertIs(Bag.valueType, list)

    class Empty(KeeNum):
      pass

    with self.assertRaises(TypeError) as context:
      _ = Empty.valueType
    self.assertEqual(str(context.exception), "KeeNum class 'Empty' has "
                                             "no members, so it has no "
                                             "'valueType'.")

  def test_peeks(self) -> None:
    class Local(KeeNum):
      A = Kee[int](1)

    peeks = (
      ('__name_space__', '_getSpace', 'space'),
      ('__base_class__', '_getBase', 'base'),
      ('__named_members__', '_getNamedMembers', 'namedMembers'),
      ('__valued_members__', '_getValuedMembers', 'valuedMembers'),
    )
    for slot, getter, field in peeks:
      with self.subTest(field=field):
        before = getattr(Local, field)
        type.__setattr__(Local, slot, None)
        with self.assertRaises(RecursionError) as context:
          getattr(Local, getter)(_recursion=True)
        self.assertEqual(context.exception.args, ())
        self.assertEqual(getattr(Local, field), before)
    type.__setattr__(Local, '__registered_members__', None)
    with self.assertRaises(RecursionError) as context:
      Local._getMembers(_recursion=True)
    self.assertEqual(context.exception.args, ())
    self.assertEqual(Local.members, ())

  def test_class_resolve_validated(self) -> None:
    self.assertFalse(WeekDay.__custom_resolve__)
    self.assertTrue(Shade.__custom_resolve__)

    class Off(Shade):
      __class_resolve__ = None

    self.assertFalse(Off.__custom_resolve__)
    with self.assertRaises(TypeException) as context:
      class Odd(KeeNum):
        A = Kee[int](1)
        __class_resolve__ = 5

    self.assertEqual(context.exception.varName, '__class_resolve__')
    self.assertEqual(context.exception.actualObject, 5)
    self.assertIs(context.exception.actualType, int)
    self.assertEqual(context.exception.expectedTypes, (Callable,))
    self.assertIn("'__class_resolve__'", str(context.exception))
    self.assertIn("'Callable'", str(context.exception))

  def test_class_init_sees_the_members(self) -> None:
    seen = []

    class Local(KeeNum):
      A = Kee[int](1)
      B = Kee[int](2)

      @classmethod
      def __class_init__(cls, name: str, bases: tuple, space, **kw) -> None:
        seen.append((name, len(cls), [m.name for m in cls]))

    self.assertEqual(seen, [('Local', 2, ['A', 'B'])])

  def test_random_bodies(self) -> None:
    self.randomWord.size = 5
    self.randomInteger.size = 5
    words = [*dict.fromkeys(self.randomWord.row)]
    numbers = self.randomInteger.row
    space = {w.upper(): Kee[int](n) for w, n in zip(words, numbers)}
    Local = KeeMeta('Local', (KeeNum,), space)
    self.assertEqual(len(Local), len(words))
    for index, (word, number) in enumerate(zip(words, numbers)):
      with self.subTest(word=word):
        member = Local[index]
        self.assertEqual(member.name, word.upper())
        self.assertEqual(member.value, number)

"""
TestKeeMetaClassApi tests the class-level operations 'KeeMeta' from
'worktoy.keenum' gives an enumeration.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import KeeNum, Kee
from worktoy.waitaminute.keenum import KeeWriteOnceError
from worktoy.waitaminute.meta import ShadowedClassHook
from . import KeenumTest, WeekDay, Shade


class TestKeeMetaClassApi(KeenumTest):
  """
  An enumeration iterates over its members, has a length and a truth,
  holds its members and nothing else, recognizes them by identity,
  answers a member's name in any case as an attribute, refuses the
  rebinding of a member, writes itself with its count, and leaves the
  operations it takes over to no class hook. The tests pin each.
  """

  def test_attribute_lookup(self) -> None:
    self.assertIs(WeekDay.monday, WeekDay.MONDAY)
    self.assertIs(WeekDay.Friday, WeekDay.FRIDAY)
    self.assertEqual(WeekDay.language, 'danish')
    with self.assertRaises(AttributeError):
      _ = WeekDay.nothing
    self.assertFalse(hasattr(WeekDay, 'nothing'))

  def test_members_are_write_once(self) -> None:
    with self.assertRaises(KeeWriteOnceError) as context:
      WeekDay.MONDAY = 1
    self.assertIs(context.exception.member, WeekDay.MONDAY)
    self.assertIs(context.exception.keeNum, WeekDay)
    self.assertEqual(context.exception.attribute, 'MONDAY')
    self.assertIn("'MONDAY' of member '%s' in 'WeekDay'" % WeekDay.MONDAY,
                  str(context.exception))
    with self.assertRaises(KeeWriteOnceError) as context:
      del WeekDay.MONDAY
    self.assertIs(context.exception.member, WeekDay.MONDAY)
    self.assertIs(context.exception.keeNum, WeekDay)
    self.assertEqual(context.exception.attribute, 'MONDAY')
    self.assertIn("'MONDAY'", str(context.exception))
    WeekDay.note = 'free'
    self.assertEqual(WeekDay.__dict__['note'], 'free')
    del WeekDay.note
    self.assertNotIn('note', WeekDay.__dict__)
    with self.assertRaises(AttributeError):
      del WeekDay.note

  def test_iteration_length_truth(self) -> None:
    self.assertEqual([*WeekDay], [*WeekDay.members])
    self.assertEqual(len(WeekDay), 7)
    self.assertTrue(WeekDay)

    class Empty(KeeNum):
      pass

    self.assertEqual([*Empty], [])
    self.assertEqual(len(Empty), 0)
    self.assertFalse(Empty)

  def test_contains_by_identity(self) -> None:
    self.assertIn(WeekDay.MONDAY, WeekDay)
    self.assertNotIn('MONDAY', WeekDay)
    self.assertNotIn('mandag', WeekDay)
    self.assertNotIn(Shade.MID, WeekDay)

    class Empty(KeeNum):
      pass

    self.assertNotIn(WeekDay.MONDAY, Empty)

  def test_contains_member_of_subclass(self) -> None:
    class Sub(WeekDay):
      HOLIDAY = Kee[str]('fridag')

    class Shape(KeeNum):
      pass

    class Polygon(Shape):
      TRIANGLE = Kee[int](3)

    self.assertIn(Sub.HOLIDAY, WeekDay)
    self.assertIn(Polygon.TRIANGLE, Shape)
    self.assertIn(Polygon.TRIANGLE, KeeNum)
    self.assertNotIn(WeekDay.MONDAY, Shape)
    self.assertNotIn('TRIANGLE', Shape)

  def test_instance_and_subclass_checks(self) -> None:
    class Sub(WeekDay):
      HOLIDAY = Kee[str]('fridag')

    self.assertIsInstance(WeekDay.MONDAY, WeekDay)
    self.assertIsInstance(Sub.HOLIDAY, WeekDay)
    self.assertIsInstance(Sub.MONDAY, Sub)
    self.assertNotIsInstance(Shade.MID, WeekDay)
    self.assertNotIsInstance('MONDAY', WeekDay)
    self.assertIsSubclass(Sub, WeekDay)
    self.assertNotIsSubclass(WeekDay, Sub)
    self.assertNotIsSubclass(Shade, WeekDay)
    self.assertNotIsSubclass(int, WeekDay)
    with self.assertRaises(TypeError):
      issubclass(5, WeekDay)

  def test_text(self) -> None:
    self.assertEqual(str(WeekDay), "<KeeNum 'WeekDay': 7 members>")
    self.assertEqual(repr(Shade), "<KeeNum 'Shade': 3 members>")

    class One(KeeNum):
      A = Kee[int](1)

    class Empty(KeeNum):
      pass

    self.assertEqual(str(One), "<KeeNum 'One': 1 member>")
    self.assertEqual(str(Empty), "<KeeNum 'Empty': 0 members>")

  def test_taken_over_operations_refuse_hooks(self) -> None:
    for hook in ('__class_len__', '__class_call__', '__class_iter__',
                 '__class_getattr__', '__class_setattr__'):
      with self.subTest(hook=hook):
        with self.assertRaises(ShadowedClassHook) as context:
          KeeNum.__class__('Bad', (KeeNum,), {hook: classmethod(len)})
        self.assertEqual(context.exception.className, 'Bad')
        self.assertEqual(context.exception.hookName, hook)
        self.assertEqual(context.exception.metaclassName, 'KeeMeta')
        self.assertEqual(context.exception.methodName,
                         hook.replace('class_', ''))
        self.assertIn("The class body of 'Bad' binds '%s'" % hook,
                      str(context.exception))
        self.assertIn("'KeeMeta' implements '%s'"
                      % hook.replace('class_', ''), str(context.exception))

  def test_other_hooks_work(self) -> None:
    class Hashed(KeeNum):
      A = Kee[int](1)

      @classmethod
      def __class_hash__(cls) -> int:
        return 17

    self.assertEqual(hash(Hashed), 17)
    self.assertEqual(hash(WeekDay), hash(('WeekDay', 'KeeNum', 'KeeMeta')))

    class Stored(KeeNum):
      A = Kee[int](1)

      @classmethod
      def __class_setitem__(cls, key: str, value: int) -> None:
        type.__setattr__(cls, '__stored__', (key, value))

    Stored['x'] = 1
    self.assertEqual(type.__getattribute__(Stored, '__stored__'), ('x', 1))

  def test_random_attribute_names(self) -> None:
    self.randomWord.size = 5
    words = [*dict.fromkeys(self.randomWord.row)]
    space = {w.upper(): Kee[str](w) for w in words}
    Local = type(WeekDay)('Local', (KeeNum,), space)
    for word in words:
      with self.subTest(word=word):
        self.assertIs(getattr(Local, word), getattr(Local, word.upper()))
        self.assertIs(getattr(Local, word.title()), Local(word))

  def test_inherited_member_by_name_in_any_case(self) -> None:
    class Longer(WeekDay):
      EIGHTH = Kee[str]('ottende')

    self.assertIs(Longer.MONDAY, WeekDay.MONDAY)
    self.assertIs(Longer.monday, WeekDay.MONDAY)
    self.assertIs(Longer.Monday, WeekDay.MONDAY)
    self.assertIs(Longer.eighth, Longer.EIGHTH)
    self.assertIn('monday', Longer.namedMembers)
    with self.assertRaises(AttributeError):
      _ = Longer.nothing
    with self.assertRaises(AttributeError):
      _ = WeekDay.eighth

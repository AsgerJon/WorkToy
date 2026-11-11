"""
TestKeeNum tests 'KeeNum' from 'worktoy.keenum' end to end.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import KeeNum, KeeBase, KeeMeta, Kee
from worktoy.waitaminute import DeprecatedPromise
from . import KeenumTest, WeekDay


class TestKeeNum(KeenumTest):
  """
  'KeeNum' is the root every enumeration subclasses: the members of a
  base are the members of the subclass, the subclass appends its own
  with the next indices, and the plain attributes stay plain; a member
  of the subclass counts as a member of the base, as 'isinstance' has
  it. The tests pin the root, the fixtures of the folder as a project
  sees them, and inheritance through two levels.
  """

  def test_root(self) -> None:
    self.assertIs(type(KeeNum), KeeMeta)
    self.assertIsSubclass(KeeNum, KeeBase)
    self.assertEqual(len(KeeNum), 0)
    self.assertIs(KeeNum.base, KeeNum)
    self.assertIsSubclass(WeekDay, KeeNum)

  def test_week_as_a_project_sees_it(self) -> None:
    names = ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY',
             'SATURDAY', 'SUNDAY']
    self.assertEqual([m.name for m in WeekDay], names)
    with self.assertWarns(DeprecatedPromise):
      self.assertEqual([m.index for m in WeekDay], [*range(7)])
    self.assertIs(WeekDay.MONDAY.valueType, str)
    self.assertEqual(WeekDay.language, 'danish')
    self.assertNotIn('language', [m.name for m in WeekDay])
    self.assertIs(WeekDay('Sunday'), WeekDay.SUNDAY)
    self.assertIs(WeekDay[6], WeekDay.SUNDAY)
    self.assertIs(WeekDay('soendag'), WeekDay.SUNDAY)
    self.assertEqual([m.value for m in WeekDay][:2], ['mandag', 'tirsdag'])

  def test_inheritance_shares_members(self) -> None:
    class Sub(WeekDay):
      HOLIDAY = Kee[str]('fridag')

    class Deep(Sub):
      LEAVE = Kee[str]('orlov')

    self.assertIs(Sub.MONDAY, WeekDay.MONDAY)
    self.assertIs(Deep.HOLIDAY, Sub.HOLIDAY)
    with self.assertWarns(DeprecatedPromise):
      self.assertEqual(Sub.HOLIDAY.index, 7)
    with self.assertWarns(DeprecatedPromise):
      self.assertEqual(Deep.LEAVE.index, 8)
    self.assertEqual(len(WeekDay), 7)
    self.assertEqual(len(Sub), 8)
    self.assertEqual(len(Deep), 9)
    self.assertEqual([m.name for m in Deep][-2:], ['HOLIDAY', 'LEAVE'])
    self.assertIs(Deep('holiday'), Sub.HOLIDAY)
    self.assertIs(Deep.MONDAY.kee, WeekDay.MONDAY.kee)
    self.assertIs(Deep.MONDAY.kee.getFieldOwner(), WeekDay)
    self.assertIs(Deep.LEAVE.kee.getFieldOwner(), Deep)
    self.assertIn(Sub.HOLIDAY, WeekDay)
    self.assertIn(Sub.HOLIDAY, Deep)
    self.assertIn(WeekDay.MONDAY, Sub)

  def test_random_enumerations(self) -> None:
    self.randomWord.size = 4
    words = [*dict.fromkeys(self.randomWord.row)]
    space = {w.upper(): Kee[str](w) for w in words}
    Local = KeeMeta('Local', (KeeNum,), space)
    self.assertEqual(str(Local), "<KeeNum 'Local': %d member%s>" % (
      len(words), '' if len(words) == 1 else 's'))
    for word in words:
      with self.subTest(word=word):
        self.assertIs(Local(word), getattr(Local, word.upper()))

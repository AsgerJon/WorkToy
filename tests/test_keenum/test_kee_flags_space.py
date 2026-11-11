"""
TestKeeFlagsSpace tests 'KeeFlagsSpace' from 'worktoy.keenum'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import KeeFlags, Kee, KeeFlagsSpace, KeeFlagsMeta
from worktoy.mcls import BaseSpace
from worktoy.waitaminute.keenum import KeeFlagNameError, KeeCaseException
from worktoy.waitaminute.keenum import KeeFlagDuplicate
from . import KeenumTest, Permission, Extended


class TestKeeFlagsSpace(KeenumTest):
  """
  'KeeFlagsSpace' records the flags the bases hold, the bases in order,
  a flag reached through two bases once, and the declarations of one
  body after them, naming each declaration. It refuses a name with an
  underscore, the name 'NULL', a name that is not upper case, a name
  declared twice or declared over an inherited flag, and two different
  flags of one name from two bases. The tests pin each on class
  statements and by hand.
  """

  def test_records(self) -> None:
    space = Permission.__namespace__
    self.assertIsInstance(space, KeeFlagsSpace)
    self.assertIsInstance(space, BaseSpace)
    self.assertEqual([*space.getDeclaredFlags()], ['READ', 'WRITE', 'EXEC'])
    self.assertIs(space.getDeclaredFlags()['READ'], Permission.READ.kee)
    self.assertEqual(space.getBaseFlags(), {})
    extended = Extended.__namespace__
    self.assertEqual([*extended.getDeclaredFlags()], ['OWN'])
    self.assertEqual(extended.getBaseFlags(),
                     {'READ': Permission.READ, 'WRITE': Permission.WRITE,
                      'EXEC': Permission.EXEC})
    self.assertIsNot(space.getDeclaredFlags(), space.getDeclaredFlags())

  def test_underscore_refused(self) -> None:
    with self.assertRaises(KeeFlagNameError) as context:
      class Local(KeeFlags):
        READ_ONLY = Kee[str]()

    exception = context.exception
    self.assertEqual(exception.clsName, 'Local')
    self.assertEqual(exception.name, 'READ_ONLY')
    self.assertIn("'_'", str(exception))

  def test_null_refused(self) -> None:
    with self.assertRaises(KeeFlagNameError) as context:
      class Local(KeeFlags):
        NULL = Kee[str]()

    self.assertEqual(context.exception.clsName, 'Local')
    self.assertEqual(context.exception.name, 'NULL')
    self.assertIn("KeeFlags class 'Local' declares the flag 'NULL'",
                  str(context.exception))
    self.assertIn('no flag high', str(context.exception))

  def test_lower_case_refused(self) -> None:
    with self.assertRaises(KeeCaseException) as context:
      class Local(KeeFlags):
        Read = Kee[str]()

    self.assertEqual(context.exception.name, 'Read')
    self.assertIn("must have upper case names, but received: 'Read'",
                  str(context.exception))

  def test_duplicates_refused(self) -> None:
    first, second = Kee[int](1), Kee[int](2)
    with self.assertRaises(KeeFlagDuplicate) as context:
      class Local(KeeFlags):
        READ = first
        READ = second

    exception = context.exception
    self.assertEqual(exception.name, 'READ')
    self.assertIs(exception.oldFlag, first)
    self.assertIs(exception.newFlag, second)
    self.assertIn("'READ' already contains flag: '<Kee member: READ>'",
                  str(exception))
    with self.assertRaises(KeeFlagDuplicate) as context:
      class Again(Permission):
        WRITE = Kee[str]()

    self.assertEqual(context.exception.name, 'WRITE')
    self.assertIs(context.exception.oldFlag, Permission.WRITE)
    self.assertIsInstance(context.exception.newFlag, Kee)
    self.assertIn("'WRITE' already contains flag: '%s'" % Permission.WRITE,
                  str(context.exception))

  def test_two_flags_of_one_name_from_two_bases_refused(self) -> None:
    class Left(KeeFlags):
      READ = Kee[str]()

    class Right(KeeFlags):
      READ = Kee[str]()

    with self.assertRaises(KeeFlagDuplicate) as context:
      KeeFlagsMeta('Both', (Left, Right), {})
    self.assertEqual(context.exception.name, 'READ')
    self.assertIs(context.exception.oldFlag, Left.READ)
    self.assertIs(context.exception.newFlag, Right.READ)

  def test_by_hand(self) -> None:
    space = KeeFlagsSpace(KeeFlagsMeta, 'Hand', (Permission,))
    self.assertEqual([*space.getBaseFlags()], ['READ', 'WRITE', 'EXEC'])
    kee = Kee[str]()
    space.addKeeFlag('OWN', kee)
    self.assertEqual(kee.name, 'OWN')
    self.assertEqual([*space.getDeclaredFlags()], ['OWN'])
    space.addBaseFlag(Permission.READ)
    self.assertEqual([*space.getBaseFlags()], ['READ', 'WRITE', 'EXEC'])

  def test_bases_without_flags(self) -> None:
    class Plain:
      flags = ['not', 'flags']

    space = KeeFlagsSpace(KeeFlagsMeta, 'Hand', (Plain, KeeFlags))
    self.assertEqual(space.getBaseFlags(), {})
    self.assertEqual(space.getDeclaredFlags(), {})
    root = KeeFlagsSpace(KeeFlagsMeta, 'Root', (Permission,), _root=True)
    self.assertEqual(root.getBaseFlags(), {})

  def test_random_flags(self) -> None:
    space = KeeFlagsSpace(KeeFlagsMeta, 'Hand', ())
    self.randomWord.size = 5
    words = [*dict.fromkeys(self.randomWord.row)]
    for word in words:
      space.addKeeFlag(word.upper(), Kee[str]())
    self.assertEqual([*space.getDeclaredFlags()], [w.upper() for w in words])
    for word in words:
      with self.subTest(word=word):
        with self.assertRaises(KeeFlagDuplicate) as context:
          space.addKeeFlag(word.upper(), Kee[str]())
        self.assertEqual(context.exception.name, word.upper())
        self.assertIs(context.exception.oldFlag,
                      space.getDeclaredFlags()[word.upper()])
        self.assertIsInstance(context.exception.newFlag, Kee)
        self.assertIn("Enumeration name '%s' already contains flag"
                      % word.upper(), str(context.exception))

  def test_names_built_at_run_time_refused(self) -> None:
    space = KeeFlagsSpace(KeeFlagsMeta, 'Hand', ())
    with self.assertRaises(KeeFlagNameError) as context:
      space.addKeeFlag(str.join('', ['NU', 'LL']), Kee[str]())
    self.assertEqual(context.exception.clsName, 'Hand')
    self.assertEqual(context.exception.name, 'NULL')
    self.assertIn("KeeFlags class 'Hand' declares the flag 'NULL'",
                  str(context.exception))
    self.assertIn('no flag high', str(context.exception))
    with self.assertRaises(KeeFlagNameError) as context:
      space.addKeeFlag(str.join('', ['A', '_B']), Kee[str]())
    self.assertEqual(context.exception.clsName, 'Hand')
    self.assertEqual(context.exception.name, 'A_B')
    self.assertIn("KeeFlags class 'Hand' declares the flag 'A_B'",
                  str(context.exception))
    self.assertIn("may not contain '_'", str(context.exception))

  def test_plain_mixin_ahead_keeps_the_base_flags(self) -> None:
    class Mixin:
      tag = 'mixin'

    class Both(Mixin, Permission):
      pass

    self.assertEqual(Both.flags, Permission.flags)
    self.assertIs(Both.READ_WRITE, Permission.READ_WRITE)
    self.assertEqual(Both.tag, 'mixin')

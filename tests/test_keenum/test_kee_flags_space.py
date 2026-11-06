"""
TestKeeFlagsSpace tests 'KeeFlagsSpace' from 'worktoy.keenum'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import KeeFlags, KeeFlag, KeeFlagsSpace, KeeFlagsMeta
from worktoy.mcls import BaseSpace
from worktoy.waitaminute.keenum import KeeFlagNameError, KeeCaseException
from worktoy.waitaminute.keenum import KeeFlagDuplicate
from . import KeenumTest, Permission, Extended


class TestKeeFlagsSpace(KeenumTest):
  """
  'KeeFlagsSpace' records the flags of one body in order behind the
  flags of its bases, refuses a name with an underscore, the name
  'NULL', a name that is not upper case and a repeated or inherited
  name, and writes the merged flags and the 'getKeeFlags' classmethod
  into the class, the root excepted. The tests pin each on class
  statements and by hand.
  """

  def test_records(self) -> None:
    space = Permission.__namespace__
    self.assertIsInstance(space, KeeFlagsSpace)
    self.assertIsInstance(space, BaseSpace)
    self.assertEqual([*space.__kee_flags__], ['READ', 'WRITE', 'EXEC'])
    self.assertIsNone(space.__base_flags__)
    self.assertEqual([*space.getKeeFlags()], ['READ', 'WRITE', 'EXEC'])
    extended = Extended.__namespace__
    self.assertEqual([*extended.__kee_flags__], ['OWN'])
    self.assertEqual([*extended._getBaseFlags()], ['READ', 'WRITE', 'EXEC'])
    self.assertEqual([*extended.getKeeFlags()],
                     ['READ', 'WRITE', 'EXEC', 'OWN'])
    self.assertEqual([*Extended.__kee_flags__], [*extended.getKeeFlags()])

  def test_class_receives_flags_and_getter(self) -> None:
    self.assertIn('__kee_flags__', Permission.__dict__)
    self.assertIsInstance(Permission.__dict__['getKeeFlags'], classmethod)
    self.assertEqual(Permission.getKeeFlags.__name__, 'getKeeFlags')
    self.assertEqual(Permission.getKeeFlags.__doc__,
                     'Getter function for the flags dictionary.')
    cloned = Permission.getKeeFlags()
    self.assertEqual([f.index for f in cloned.values()], [0, 1, 2])
    self.assertEqual([f.fieldOwner for f in cloned.values()],
                     [Permission] * 3)
    self.assertNotIn('__kee_flags__', KeeFlags.__dict__)
    self.assertFalse(hasattr(KeeFlags, 'getKeeFlags'))

  def test_underscore_refused(self) -> None:
    with self.assertRaises(KeeFlagNameError) as context:
      class Local(KeeFlags):
        READ_ONLY = KeeFlag()

    exception = context.exception
    self.assertEqual(exception.clsName, 'Local')
    self.assertEqual(exception.name, 'READ_ONLY')
    self.assertIn("'_'", str(exception))

  def test_null_refused(self) -> None:
    with self.assertRaises(KeeFlagNameError) as context:
      class Local(KeeFlags):
        NULL = KeeFlag()

    self.assertEqual(context.exception.clsName, 'Local')
    self.assertEqual(context.exception.name, 'NULL')
    self.assertIn("KeeFlags class 'Local' declares the flag 'NULL'",
                  str(context.exception))
    self.assertIn('no flag high', str(context.exception))

  def test_lower_case_refused(self) -> None:
    with self.assertRaises(KeeCaseException) as context:
      class Local(KeeFlags):
        Read = KeeFlag()

    self.assertEqual(context.exception.name, 'Read')
    self.assertIn("must have upper case names, but received: 'Read'",
                  str(context.exception))

  def test_duplicates_refused(self) -> None:
    with self.assertRaises(KeeFlagDuplicate) as context:
      class Local(KeeFlags):
        READ = KeeFlag(1)
        READ = KeeFlag(2)

    exception = context.exception
    self.assertEqual(exception.name, 'READ')
    self.assertEqual(exception.oldFlag.args, (1,))
    self.assertEqual(exception.newFlag.args, (2,))
    self.assertIn("'READ'", str(exception))
    with self.assertRaises(KeeFlagDuplicate) as context:
      class Again(Permission):
        WRITE = KeeFlag()

    self.assertEqual(context.exception.name, 'WRITE')
    self.assertIs(context.exception.oldFlag, Permission.flags[1])
    self.assertEqual(context.exception.newFlag.args, ())
    self.assertIn("'WRITE' already contains flag: 'Permission.WRITE [1]'",
                  str(context.exception))

  def test_by_hand(self) -> None:
    space = KeeFlagsSpace(KeeFlagsMeta, 'Hand', (Permission,))
    self.assertEqual([*space._getBaseFlags()], ['READ', 'WRITE', 'EXEC'])
    flag = KeeFlag()
    space.addKeeFlag('OWN', flag)
    self.assertEqual(flag.name, 'OWN')
    self.assertEqual(flag.fieldName, 'OWN')
    self.assertEqual([*space.getKeeFlags()],
                     ['READ', 'WRITE', 'EXEC', 'OWN'])
    compiled = space.compile()
    self.assertEqual([*compiled['__kee_flags__']],
                     ['READ', 'WRITE', 'EXEC', 'OWN'])
    self.assertIsInstance(compiled['getKeeFlags'], classmethod)
    late = KeeFlag()
    space.addBaseFlag('LATE', late)
    self.assertIs(space._getBaseFlags()['LATE'], late)

  def test_bases_without_flags(self) -> None:
    class Plain:
      flags = ['not', 'flags']

    space = KeeFlagsSpace(KeeFlagsMeta, 'Hand', (Plain, KeeFlags))
    self.assertEqual(space._getBaseFlags(), {})
    self.assertEqual(space.getKeeFlags(), {})
    root = KeeFlagsSpace(KeeFlagsMeta, 'Root', (Permission,), _root=True)
    self.assertEqual(root._getBaseFlags(), {})
    compiled = root.compile()
    self.assertNotIn('__kee_flags__', compiled)
    self.assertNotIn('getKeeFlags', compiled)

  def test_random_flags(self) -> None:
    space = KeeFlagsSpace(KeeFlagsMeta, 'Hand', ())
    self.randomWord.size = 5
    words = [*dict.fromkeys(self.randomWord.row)]
    for word in words:
      space.addKeeFlag(word.upper(), KeeFlag())
    self.assertEqual([*space.getKeeFlags()], [w.upper() for w in words])
    for word in words:
      with self.subTest(word=word):
        with self.assertRaises(KeeFlagDuplicate) as context:
          space.addKeeFlag(word.upper(), KeeFlag())
        self.assertEqual(context.exception.name, word.upper())
        self.assertIs(context.exception.oldFlag,
                      space.getKeeFlags()[word.upper()])
        self.assertEqual(context.exception.newFlag.args, ())
        self.assertIn("Enumeration name '%s' already contains flag"
                      % word.upper(), str(context.exception))

  def test_names_built_at_run_time_refused(self) -> None:
    space = KeeFlagsSpace(KeeFlagsMeta, 'Hand', ())
    with self.assertRaises(KeeFlagNameError) as context:
      space.addKeeFlag(str.join('', ['NU', 'LL']), KeeFlag())
    self.assertEqual(context.exception.clsName, 'Hand')
    self.assertEqual(context.exception.name, 'NULL')
    self.assertIn("KeeFlags class 'Hand' declares the flag 'NULL'",
                  str(context.exception))
    self.assertIn('no flag high', str(context.exception))
    with self.assertRaises(KeeFlagNameError) as context:
      space.addKeeFlag(str.join('', ['A', '_B']), KeeFlag())
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

    self.assertEqual([f.__member_name__ for f in Both.flags],
                     ['READ', 'WRITE', 'EXEC'])
    self.assertEqual(Both.READ_WRITE.names, frozenset({'READ', 'WRITE'}))
    self.assertEqual(Both.tag, 'mixin')

"""
TestKeeFlagsMeta tests 'KeeFlagsMeta' from 'worktoy.keenum'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import KeeFlags, KeeFlag, KeeFlagsMeta, KeeFlagsSpace
from worktoy.waitaminute.keenum import KeeResolveError, KeeWriteOnceError
from worktoy.waitaminute.meta import ShadowedClassHook
from . import KeenumTest, Permission, Extended, FileAccess


class TestKeeFlagsMeta(KeenumTest):
  """
  'KeeFlagsMeta' builds one member per combination of the flags, keeps
  them in a list and a dictionary keyed by the names of the high flags,
  resolves a member from a member of the lineage, a name in any case
  and order, an index, a value or several identifiers, and takes over
  calling, length, iteration, membership and the attributes of the
  class. The tests pin each on the fixtures of the folder.
  """

  def test_members_built(self) -> None:
    self.assertEqual(len(Permission), 8)
    self.assertEqual(len(Extended), 16)
    names = [m.name for m in Permission]
    expected = ['NULL', 'READ', 'WRITE', 'READ_WRITE', 'EXEC', 'READ_EXEC',
                'WRITE_EXEC', 'READ_WRITE_EXEC']
    self.assertEqual(names, expected)
    self.assertEqual([m.index for m in Permission], [*range(8)])
    self.assertEqual(Permission.memberList, [*Permission])
    self.assertIs(Permission.memberDict[frozenset(('READ', 'EXEC'))],
                  Permission.READ_EXEC)
    self.assertEqual(len(Permission.memberDict), 8)
    for member in Permission:
      with self.subTest(member=member.name):
        self.assertIs(Permission.__dict__[member.name], member)
        self.assertIs(member.__field_owner__, Permission)
        self.assertEqual(member.__field_name__, member.name)

  def test_flags_cloned_once(self) -> None:
    flags = Permission.flags
    self.assertEqual([f.name for f in flags], ['READ', 'WRITE', 'EXEC'])
    self.assertEqual([f.index for f in flags], [0, 1, 2])
    self.assertIsNot(flags, Permission.flags)
    self.assertEqual(flags, Permission.flags)
    self.assertIs(flags[0], Permission.flags[0])
    self.assertIs(Permission.__dict__['__flag_clones__'][0], flags[0])
    self.assertEqual([f.name for f in Extended.flags],
                     ['READ', 'WRITE', 'EXEC', 'OWN'])
    self.assertIsNot(Extended.flags[0], Permission.flags[0])

  def test_value_type(self) -> None:
    self.assertIs(Permission.valueType, int)
    self.assertIs(FileAccess.valueType, bytes)

  def test_root(self) -> None:
    self.assertIs(KeeFlagsMeta.__kee_class__, KeeFlags)
    self.assertIs(type(KeeFlags), KeeFlagsMeta)
    self.assertNotIn('__member_list__', KeeFlags.__dict__)
    self.assertEqual(KeeFlags.__keyword_arguments__, {'_root': True})
    self.assertIsInstance(KeeFlagsMeta.__prepare__('A', ()), KeeFlagsSpace)

  def test_built_by_call(self) -> None:
    Local = KeeFlagsMeta('Local', (Permission,), {'OWN': KeeFlag()})
    self.assertEqual(len(Local), 16)
    self.assertEqual(Local.READ_OWN.index, 9)
    self.assertEqual([f.name for f in Local.flags],
                     ['READ', 'WRITE', 'EXEC', 'OWN'])

  def test_attributes_of_the_class(self) -> None:
    with self.assertRaises(KeeWriteOnceError) as context:
      Permission.READ = 1
    self.assertIs(context.exception.member, Permission.READ)
    self.assertIs(context.exception.keeNum, Permission)
    self.assertEqual(context.exception.attribute, 'READ')
    self.assertIn("'READ' of member 'Permission.READ [1]'",
                  str(context.exception))
    with self.assertRaises(KeeWriteOnceError) as context:
      del Permission.NULL
    self.assertIs(context.exception.member, Permission.NULL)
    self.assertIs(context.exception.keeNum, Permission)
    self.assertEqual(context.exception.attribute, 'NULL')
    self.assertIn("'NULL' of member 'Permission.NULL [0]'",
                  str(context.exception))
    Permission.note = 'free'
    self.assertEqual(Permission.__dict__['note'], 'free')
    Permission.note = 'again'
    self.assertEqual(Permission.__dict__['note'], 'again')
    del Permission.note
    self.assertNotIn('note', Permission.__dict__)
    with self.assertRaises(AttributeError):
      del Permission.note

  def test_call(self) -> None:
    self.assertIs(Permission(), Permission.NULL)
    self.assertIs(Permission('read'), Permission.READ)
    self.assertIs(Permission('READ', 'WRITE'), Permission.READ_WRITE)
    self.assertIs(Permission(Permission.EXEC, 'read'), Permission.READ_EXEC)
    self.assertIs(Permission(5), Permission.READ_EXEC)
    with self.assertRaises(TypeError) as context:
      Permission(flag='read')
    self.assertEqual(str(context.exception),
                     "Permission() takes no keyword arguments, "
                     "but received 'flag'.")

  def test_subscript(self) -> None:
    self.assertIs(Permission['write_read'], Permission.READ_WRITE)
    self.assertIs(Permission['Exec'], Permission.EXEC)
    self.assertIs(Permission['null'], Permission.NULL)
    self.assertIs(Permission[('READ', 'EXEC')], Permission.READ_EXEC)
    self.assertIs(Permission[['read', 'read']], Permission.READ)
    self.assertIs(Permission[{'WRITE'}], Permission.WRITE)
    self.assertIs(Permission[frozenset()], Permission.NULL)
    self.assertIs(Permission[0], Permission.NULL)
    self.assertIs(Permission[7], Permission.READ_WRITE_EXEC)

  def test_misses(self) -> None:
    for identifier in ('nothing', 'READ_NOTHING', 8, -1, True, 3.5):
      with self.subTest(identifier=identifier):
        with self.assertRaises(KeeResolveError) as context:
          Permission[identifier]
        self.assertIs(context.exception.keeNum, Permission)
        self.assertEqual(context.exception.identifier, identifier)
        self.assertIn("'Permission' could not resolve the identifier '%s'"
                      % (identifier,), str(context.exception))
    with self.assertRaises(KeeResolveError) as context:
      Permission('read', 'nothing')
    self.assertIs(context.exception.keeNum, Permission)
    self.assertEqual(context.exception.identifier, 'nothing')
    self.assertIn("'nothing'", str(context.exception))

  def test_values(self) -> None:
    self.assertIs(FileAccess(b'2'), FileAccess.CLOSE)
    self.assertIs(FileAccess[b'0'], FileAccess.NULL)
    self.assertIs(FileAccess._resolveValue(b'3'), FileAccess.OPEN_CLOSE)
    with self.assertRaises(KeeResolveError) as context:
      FileAccess(b'9')
    self.assertIs(context.exception.keeNum, FileAccess)
    self.assertEqual(context.exception.identifier, b'9')
    self.assertIn("'FileAccess' could not resolve the identifier 'b'9''",
                  str(context.exception))
    with self.assertRaises(KeeResolveError) as context:
      FileAccess('9')
    self.assertIs(context.exception.keeNum, FileAccess)
    self.assertEqual(context.exception.identifier, '9')
    self.assertIn("the identifier '9'", str(context.exception))
    with self.assertRaises(KeeResolveError) as context:
      FileAccess._resolveValue(True)
    self.assertIs(context.exception.keeNum, FileAccess)
    self.assertIs(context.exception.identifier, True)
    self.assertIn("the identifier 'True'", str(context.exception))
    self.assertIs(Permission._resolveValue(3), Permission.READ_WRITE)

  def test_value_tables(self) -> None:
    class Buffer(KeeFlags):
      OPEN = KeeFlag()
      CLOSE = KeeFlag()

      def _getValue(self) -> bytearray:
        return bytearray(str(self.index).encode())

    class Parity(KeeFlags):
      ODD = KeeFlag()
      BIG = KeeFlag()

      def _getValue(self) -> float:
        return float(self.index % 2)

    #  Unhashable values are compared with each member in turn.
    self.assertIs(Buffer(bytearray(b'2')), Buffer.CLOSE)
    with self.assertRaises(KeeResolveError) as context:
      Buffer(bytearray(b'9'))
    self.assertIs(context.exception.keeNum, Buffer)
    self.assertEqual(context.exception.identifier, bytearray(b'9'))
    self.assertIn("'Buffer' could not resolve the identifier "
                  "'bytearray(b'9')'", str(context.exception))
    #  A value several members share resolves to the lowest index.
    self.assertIs(Parity(1.0), Parity.ODD)
    self.assertIs(Parity(0.0), Parity.NULL)
    #  The scan takes an equal value alone, not one that sorts above the
    #  identifier, as b'2' sorts above b'15'.
    with self.assertRaises(KeeResolveError) as context:
      Buffer(bytearray(b'15'))
    self.assertIs(context.exception.keeNum, Buffer)
    self.assertEqual(context.exception.identifier, bytearray(b'15'))
    self.assertIn("'Buffer' could not resolve the identifier "
                  "'bytearray(b'15')'", str(context.exception))

    class Gappy(KeeFlags):
      A = KeeFlag()
      B = KeeFlag()

      def _getValue(self) -> float:
        return 0.0 if self.index == 2 else float(self.index)

    #  A value repeated over a member before it does not hide the values
    #  of the members after it.
    self.assertIs(Gappy(3.0), Gappy.A_B)

    class Mixed(KeeFlags):
      OPEN = KeeFlag()
      CLOSE = KeeFlag()

      def _getValue(self) -> object:
        if self.index:
          return str(self.index).encode()
        return bytearray(b'0')

    #  Once one value does not hash, a hashable identifier is compared
    #  with each value in turn as well.
    self.assertIs(Mixed(b'2'), Mixed.CLOSE)
    #  An unhashable identifier misses the table of hashable values and
    #  is compared with each member in turn.
    with self.assertRaises(KeeResolveError) as context:
      FileAccess(bytearray(b'1'))
    self.assertIs(context.exception.keeNum, FileAccess)
    self.assertEqual(context.exception.identifier, bytearray(b'1'))
    self.assertIn("'FileAccess' could not resolve the identifier "
                  "'bytearray(b'1')'", str(context.exception))

  def test_members_of_the_lineage(self) -> None:
    self.assertIs(Permission(Extended.READ), Permission.READ)
    self.assertIs(Extended(Permission.READ_WRITE), Extended.READ_WRITE)
    self.assertIsNot(Extended.READ, Permission.READ)
    self.assertIs(Permission._fromMember(Permission.EXEC), Permission.EXEC)
    self.assertIs(Permission._fromMember(Extended.EXEC), Permission.EXEC)
    self.assertIsNone(Permission._fromMember(Extended.OWN))
    self.assertIsNone(Permission._fromMember(FileAccess.OPEN))
    with self.assertRaises(KeeResolveError) as context:
      Permission(Extended.OWN)
    self.assertIs(context.exception.keeNum, Permission)
    self.assertIs(context.exception.identifier, Extended.OWN)
    self.assertIn("'Permission' could not resolve the identifier "
                  "'Extended.OWN [8]'", str(context.exception))
    with self.assertRaises(KeeResolveError) as context:
      Permission[FileAccess.OPEN]
    self.assertIs(context.exception.keeNum, Permission)
    self.assertIs(context.exception.identifier, FileAccess.OPEN)
    self.assertIn("the identifier 'FileAccess.OPEN [1]'",
                  str(context.exception))

  def test_contains(self) -> None:
    self.assertIn(Permission.READ, Permission)
    self.assertIn(Extended.READ_WRITE, Permission)
    self.assertNotIn(Extended.OWN, Permission)
    self.assertIn(Permission.READ, Extended)
    self.assertNotIn(FileAccess.OPEN, Permission)
    self.assertNotIn('READ', Permission)
    self.assertNotIn(1, Permission)
    self.assertNotIn(Permission.READ, FileAccess)

  def test_iteration_and_length(self) -> None:
    self.assertEqual([m.index for m in Extended], [*range(16)])
    self.assertEqual(len(FileAccess), 4)
    self.assertTrue(Permission)

  def test_text(self) -> None:
    self.assertEqual(str(Permission), 'Permission[metaclass=KeeFlagsMeta]')
    self.assertEqual(repr(Extended), 'Extended[metaclass=KeeFlagsMeta]')

  def test_taken_over_operations_refuse_hooks(self) -> None:
    for hook in ('__class_len__', '__class_call__', '__class_iter__',
                 '__class_contains__', '__class_setattr__'):
      with self.subTest(hook=hook):
        with self.assertRaises(ShadowedClassHook) as context:
          KeeFlagsMeta('Bad', (KeeFlags,), {hook: classmethod(len)})
        self.assertEqual(context.exception.className, 'Bad')
        self.assertEqual(context.exception.hookName, hook)
        self.assertEqual(context.exception.metaclassName, 'KeeFlagsMeta')
        self.assertEqual(context.exception.methodName,
                         hook.replace('class_', ''))
        self.assertIn("The class body of 'Bad' binds '%s'" % hook,
                      str(context.exception))
        self.assertIn("'KeeFlagsMeta' implements '%s'"
                      % hook.replace('class_', ''), str(context.exception))

  def test_other_hooks_work(self) -> None:
    class Shown(KeeFlags):
      READ = KeeFlag()

      @classmethod
      def __class_str__(cls) -> str:
        return 'shown'

    self.assertEqual(str(Shown), 'shown')
    self.assertEqual(len(Shown), 2)

  def test_random_flags_classes(self) -> None:
    self.randomWord.size = 4
    words = [*dict.fromkeys(self.randomWord.row)]
    space = {w.upper(): KeeFlag() for w in words}
    Local = KeeFlagsMeta('Local', (KeeFlags,), space)
    self.assertEqual(len(Local), 2 ** len(words))
    for index, word in enumerate(words):
      with self.subTest(word=word):
        member = Local(word)
        self.assertEqual(member.index, 1 << index)
        self.assertEqual(member.names, frozenset((word.upper(),)))

  def test_index_past_the_end_and_values_of_another_type(self) -> None:
    with self.assertRaises(KeeResolveError) as context:
      _ = Permission[len(Permission)]
    self.assertIs(context.exception.keeNum, Permission)
    self.assertEqual(context.exception.identifier, len(Permission))
    self.assertIn("'Permission' could not resolve the identifier '8'",
                  str(context.exception))
    with self.assertRaises(KeeResolveError) as context:
      _ = Permission[99]
    self.assertIs(context.exception.keeNum, Permission)
    self.assertEqual(context.exception.identifier, 99)
    self.assertIn("the identifier '99'", str(context.exception))
    with self.assertRaises(KeeResolveError) as context:
      Permission._resolveIndex(99)
    self.assertIs(context.exception.keeNum, Permission)
    self.assertEqual(context.exception.identifier, 99)
    self.assertIn("the identifier '99'", str(context.exception))

    class Scaled(FileAccess):
      def _getValue(self) -> float:
        return self.index * 1.5

    self.assertEqual([m.value for m in Scaled][:3], [0.0, 1.5, 3.0])
    self.assertIs(Scaled(1.5), Scaled.memberList[1])
    self.assertIs(Scaled(3.0), Scaled.memberList[2])
    with self.assertRaises(KeeResolveError) as context:
      Scaled(2.0)
    self.assertIs(context.exception.keeNum, Scaled)
    self.assertEqual(context.exception.identifier, 2.0)
    self.assertIn("'Scaled' could not resolve the identifier '2.0'",
                  str(context.exception))

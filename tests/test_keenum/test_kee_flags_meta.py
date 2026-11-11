"""
TestKeeFlagsMeta tests 'KeeFlagsMeta' from 'worktoy.keenum'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import KeeFlags, Kee, KeeFlagsMeta, KeeFlagsSpace
from worktoy.keenum import _kee_flags_meta
from worktoy.waitaminute.keenum import KeeResolveError, KeeWriteOnceError
from worktoy.waitaminute.keenum import KeeTypeException
from worktoy.waitaminute.meta import ShadowedClassHook
from . import KeenumTest, Permission, Extended, FileAccess


class TestKeeFlagsMeta(KeenumTest):
  """
  'KeeFlagsMeta' gives a flags class its flags, the bases' first, and
  one member per combination of them, in the order of the bit masks of
  the class. A member another class built already for the same flags,
  'NULL' among them, is that very member. The class keeps its members
  in a list and a dictionary keyed by the names of the high flags,
  resolves a member from a member, a name in any case and order, a
  position, a value or several identifiers, answers 'in' and
  'isinstance' by identity, and takes over calling, length, iteration,
  membership, the instance check and the attributes of the class. The
  tests pin each on the fixtures and on local classes.
  """

  def test_members_built(self) -> None:
    self.assertEqual(len(Permission), 8)
    self.assertEqual(len(Extended), 16)
    names = [m.name for m in Permission]
    expected = ['NULL', 'READ', 'WRITE', 'READ_WRITE', 'EXEC', 'READ_EXEC',
                'WRITE_EXEC', 'READ_WRITE_EXEC']
    self.assertEqual(names, expected)
    self.assertEqual(Permission.memberList, [*Permission])
    self.assertIs(Permission.memberDict[frozenset(('READ', 'EXEC'))],
                  Permission.READ_EXEC)
    self.assertEqual(len(Permission.memberDict), 8)
    for member in Permission:
      with self.subTest(member=member.name):
        self.assertIs(Permission.__dict__[member.name], member)
    self.assertEqual([*Extended][:8], [*Permission])

  def test_flags(self) -> None:
    flags = Permission.flags
    self.assertEqual(flags, [Permission.READ, Permission.WRITE,
                             Permission.EXEC])
    self.assertIsNot(flags, Permission.flags)
    self.assertEqual(Extended.flags, [*flags, Extended.OWN])
    self.assertEqual(KeeFlags.flags, [])

  def test_root(self) -> None:
    self.assertIs(KeeFlagsMeta.__kee_class__, KeeFlags)
    self.assertIs(type(KeeFlags), KeeFlagsMeta)
    self.assertEqual([*KeeFlags], [KeeFlags.NULL])
    self.assertEqual(len(KeeFlags), 1)
    self.assertEqual(KeeFlags.__keyword_arguments__, {'_root': True})
    self.assertIsInstance(KeeFlagsMeta.__prepare__('A', ()), KeeFlagsSpace)
    with self.assertRaises(TypeError) as context:
      _ = KeeFlags.valueType
    self.assertEqual(str(context.exception),
                     "Flags class 'KeeFlags' has no flags, so it has no "
                     "'valueType'.")

  def test_value_type(self) -> None:
    self.assertIs(Permission.valueType, str)
    self.assertIs(FileAccess.valueType, bytes)

  def test_flags_share_the_value_type(self) -> None:
    combinations = _kee_flags_meta._COMBINATIONS
    before = len(combinations)
    with self.assertRaises(KeeTypeException) as context:
      class Mixed(KeeFlags):
        ONE = Kee[int](1)
        RED = Kee[str]()

    #  A refused class enters none of its flags among the members.
    self.assertEqual(len(combinations), before)
    self.assertEqual(context.exception.name, 'RED')
    self.assertEqual(context.exception.value, 'RED')
    self.assertEqual(context.exception.expectedTypes, (int,))
    self.assertEqual(str(context.exception), str.join(' ', """Member 'RED'
      has value 'RED' of type 'str', but expected the value to be an
      instance of 'int'!""".split()))

    class Number(KeeFlags):
      ONE = Kee[int](1)

    class Word(KeeFlags):
      RED = Kee[str]()

    with self.assertRaises(KeeTypeException) as context:
      KeeFlagsMeta('Both', (Number, Word), {})
    self.assertEqual(context.exception.name, 'RED')
    self.assertEqual(context.exception.value, 'RED')
    self.assertEqual(context.exception.expectedTypes, (int,))

    class Halves(KeeFlags):
      HALF = Kee[str]()

      def _getValue(self) -> float:
        return 0.5 * len(self.names)

    with self.assertRaises(KeeTypeException) as context:
      class Wholes(Halves):
        WHOLE = Kee[str]()

        def _getValue(self) -> int:
          return len(self.names)

    self.assertEqual(context.exception.name, 'WHOLE')
    self.assertEqual(context.exception.value, 1)
    self.assertEqual(context.exception.expectedTypes, (float,))

  def test_null_and_combinations_are_exempt(self) -> None:
    class Numbered(KeeFlags):
      ONE = Kee[int](1)
      TWO = Kee[int](2)

    self.assertIs(Numbered.valueType, int)
    self.assertEqual(Numbered.ONE_TWO.value, 'ONE_TWO')
    self.assertEqual(Numbered.NULL.value, 'NULL')
    self.assertEqual(FileAccess.NULL.value, 'NULL')

  def test_built_by_call(self) -> None:
    Local = KeeFlagsMeta('Local', (Permission,), {'OWN': Kee[str]()})
    self.assertEqual(len(Local), 16)
    self.assertIs(Local[9], Local.READ_OWN)
    self.assertEqual(Local.flags, [*Permission.flags, Local.OWN])

  def test_several_bases(self) -> None:
    class User(KeeFlags):
      READ = Kee[str]()

    class Admin(KeeFlags):
      WRITE = Kee[str]()

    class Both(User, Admin):
      EXEC = Kee[str]()

    self.assertEqual(Both.flags, [User.READ, Admin.WRITE, Both.EXEC])
    self.assertEqual(len(Both), 8)
    self.assertIs(Both[1], User.READ)
    self.assertIs(Both[2], Admin.WRITE)
    self.assertIs(Both.NULL, KeeFlags.NULL)

    class Diamond(Both, User):
      pass

    self.assertEqual(Diamond.flags, Both.flags)
    self.assertIs(Diamond.READ_WRITE_EXEC, Both.READ_WRITE_EXEC)

  def test_attributes_of_the_class(self) -> None:
    with self.assertRaises(KeeWriteOnceError) as context:
      Permission.READ = 1
    self.assertIs(context.exception.member, Permission.READ)
    self.assertIs(context.exception.keeNum, Permission)
    self.assertEqual(context.exception.attribute, 'READ')
    self.assertIn("'READ' of member '%s'" % Permission.READ,
                  str(context.exception))
    with self.assertRaises(KeeWriteOnceError) as context:
      del Permission.NULL
    self.assertIs(context.exception.member, Permission.NULL)
    self.assertIs(context.exception.keeNum, KeeFlags)
    self.assertEqual(context.exception.attribute, 'NULL')
    self.assertIn("'NULL' of member '<KeeFlags>.NULL'",
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
    self.assertIs(FileAccess(b'CLOSE'), FileAccess.CLOSE)
    self.assertIs(FileAccess['NULL'], FileAccess.NULL)
    self.assertIs(FileAccess._resolveValue(b'OPEN_CLOSE'),
                  FileAccess.OPEN_CLOSE)
    self.assertIs(Permission._resolveValue('READ_WRITE'),
                  Permission.READ_WRITE)
    with self.assertRaises(KeeResolveError) as context:
      FileAccess(b'NOTHING')
    self.assertIs(context.exception.keeNum, FileAccess)
    self.assertEqual(context.exception.identifier, b'NOTHING')
    self.assertIn("'FileAccess' could not resolve the identifier "
                  "'b'NOTHING''", str(context.exception))
    with self.assertRaises(KeeResolveError) as context:
      FileAccess._resolveValue(True)
    self.assertIs(context.exception.keeNum, FileAccess)
    self.assertIs(context.exception.identifier, True)
    self.assertIn("the identifier 'True'", str(context.exception))

    class Numbered(KeeFlags):
      ONE = Kee[int](1)
      TWO = Kee[int](2)

    self.assertIs(Numbered._resolveValue(2), Numbered.TWO)
    #  'True' hashes as 1 and finds 'ONE' in the table, but a 'bool' is no
    #  value of an 'int' flag, and no member holds a 'bool'.
    with self.assertRaises(KeeResolveError) as context:
      Numbered._resolveValue(True)
    self.assertIs(context.exception.keeNum, Numbered)
    self.assertIs(context.exception.identifier, True)
    self.assertIn("'Numbered' could not resolve the identifier 'True'",
                  str(context.exception))

  def test_value_tables(self) -> None:
    class Buffer(KeeFlags):
      OPEN = Kee[str]()
      CLOSE = Kee[str]()

      def _getValue(self) -> bytearray:
        return bytearray(self.name.encode())

    class Parity(KeeFlags):
      ODD = Kee[str]()
      BIG = Kee[str]()

      def _getValue(self) -> float:
        return float(len(self.names) % 2)

    #  Unhashable values are compared with each member in turn.
    self.assertIs(Buffer(bytearray(b'CLOSE')), Buffer.CLOSE)
    with self.assertRaises(KeeResolveError) as context:
      Buffer(bytearray(b'NOTHING'))
    self.assertIs(context.exception.keeNum, Buffer)
    self.assertEqual(context.exception.identifier, bytearray(b'NOTHING'))
    self.assertIn("'Buffer' could not resolve the identifier "
                  "'bytearray(b'NOTHING')'", str(context.exception))
    #  A value several members share resolves to the first in the class.
    self.assertIs(Parity(1.0), Parity.ODD)
    self.assertIs(Parity(0.0), Parity.ODD_BIG)

    class Gappy(KeeFlags):
      A = Kee[str]()
      B = Kee[str]()

      def _getValue(self) -> float:
        return 0.0 if self.name == 'B' else float(len(self.name))

    #  A value repeated over a member before it does not hide the values
    #  of the members after it.
    self.assertIs(Gappy(3.0), Gappy.A_B)

    class Mixed(KeeFlags):
      OPEN = Kee[str]()
      CLOSE = Kee[str]()

      def _getValue(self) -> object:
        if len(self.names) > 1:
          return bytearray(self.name.encode())
        return self.name.encode()

    #  Once one value does not hash, a hashable identifier is compared
    #  with each value in turn as well.
    self.assertIs(Mixed(b'CLOSE'), Mixed.CLOSE)
    self.assertIs(Mixed(bytearray(b'OPEN_CLOSE')), Mixed.OPEN_CLOSE)
    #  An unhashable identifier misses the table of hashable values and
    #  is compared with each member in turn.
    with self.assertRaises(KeeResolveError) as context:
      FileAccess(bytearray(b'OPEN'))
    self.assertIs(context.exception.keeNum, FileAccess)
    self.assertEqual(context.exception.identifier, bytearray(b'OPEN'))
    self.assertIn("'FileAccess' could not resolve the identifier "
                  "'bytearray(b'OPEN')'", str(context.exception))

  def test_members_of_related_classes(self) -> None:
    self.assertIs(Permission(Extended.READ), Permission.READ)
    self.assertIs(Extended(Permission.READ_WRITE), Permission.READ_WRITE)
    #  A member of a subclass belongs to the class, as 'isinstance' has it.
    self.assertIs(Permission(Extended.OWN), Extended.OWN)
    with self.assertRaises(KeeResolveError) as context:
      Permission[FileAccess.OPEN]
    self.assertIs(context.exception.keeNum, Permission)
    self.assertIs(context.exception.identifier, FileAccess.OPEN)
    self.assertIn("the identifier '%s'" % FileAccess.OPEN,
                  str(context.exception))

  def test_contains_and_instance_check(self) -> None:
    self.assertIn(Permission.READ, Permission)
    self.assertIn(Permission.READ, Extended)
    self.assertIn(Extended.OWN, Permission)
    self.assertIn(Permission.NULL, FileAccess)
    self.assertNotIn(FileAccess.OPEN, Permission)
    self.assertNotIn(Permission.READ, FileAccess)
    self.assertNotIn('READ', Permission)
    self.assertNotIn(1, Permission)
    self.assertIsInstance(Permission.READ, Extended)
    self.assertIsInstance(Permission.NULL, Permission)
    self.assertIsInstance(Extended.OWN, Permission)
    self.assertNotIsInstance(FileAccess.OPEN, Permission)
    self.assertNotIsInstance('READ', Permission)

  def test_iteration_and_length(self) -> None:
    self.assertEqual([*Extended], Extended.memberList)
    self.assertEqual(len(FileAccess), 4)
    self.assertTrue(Permission)

  def test_text(self) -> None:
    self.assertEqual(str(Permission), 'Permission[metaclass=KeeFlagsMeta]')
    self.assertEqual(repr(Extended), 'Extended[metaclass=KeeFlagsMeta]')

  def test_taken_over_operations_refuse_hooks(self) -> None:
    for hook in ('__class_len__', '__class_call__', '__class_iter__',
                 '__class_contains__', '__class_setattr__',
                 '__class_instancecheck__'):
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
      READ = Kee[str]()

      @classmethod
      def __class_str__(cls) -> str:
        return 'shown'

    self.assertEqual(str(Shown), 'shown')
    self.assertEqual(len(Shown), 2)

  def test_random_flags_classes(self) -> None:
    self.randomWord.size = 4
    words = [*dict.fromkeys(self.randomWord.row)]
    space = {w.upper(): Kee[str]() for w in words}
    Local = KeeFlagsMeta('Local', (KeeFlags,), space)
    self.assertEqual(len(Local), 2 ** len(words))
    for index, word in enumerate(words):
      with self.subTest(word=word):
        member = Local(word)
        self.assertIs(Local[1 << index], member)
        self.assertEqual(member.names, frozenset((word.upper(),)))
        self.assertEqual(member.value, word.upper())

  def test_index_past_the_end(self) -> None:
    with self.assertRaises(KeeResolveError) as context:
      _ = Permission[len(Permission)]
    self.assertIs(context.exception.keeNum, Permission)
    self.assertEqual(context.exception.identifier, len(Permission))
    self.assertIn("'Permission' could not resolve the identifier '8'",
                  str(context.exception))
    with self.assertRaises(KeeResolveError) as context:
      Permission._resolveIndex(99)
    self.assertIs(context.exception.keeNum, Permission)
    self.assertEqual(context.exception.identifier, 99)
    self.assertIn("the identifier '99'", str(context.exception))

  def test_union_beyond_the_class_refused(self) -> None:
    with self.assertRaises(KeeResolveError) as context:
      Permission(Extended.OWN, 'read')
    self.assertIs(context.exception.keeNum, Permission)
    self.assertEqual(context.exception.identifier, (Extended.OWN, 'read'))
    self.assertIn("'Permission' could not resolve the identifier",
                  str(context.exception))

"""
TestKeeFlags tests 'KeeFlags' from 'worktoy.keenum', the members of a
flags class.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import copy
import pickle

from worktoy.keenum import KeeFlags, Kee
from worktoy.utilities import typeCast
from worktoy.waitaminute.dispatch import TypeCastException
from worktoy.waitaminute.keenum import KeeWriteOnceError, KeeResolveError
from . import KeenumTest, Permission, Extended, FileAccess


class TestKeeFlags(KeenumTest):
  """
  Every member of a flags class is a combination of its flags: a flag is
  the combination of itself, and 'NULL', built by 'KeeFlags' itself, is
  the one member combining none. A member knows its high flags, and its
  low flags among those of the class that built it; it is valued by its
  name unless that class gives values through '_getValue', is falsy only
  as 'NULL', equal to itself alone, hashes by the names of its high
  flags, combines with the three operators into the member of the
  resulting flags, inverts within the class that built it, survives
  copies and pickling as itself, and refuses every change. The tests pin
  each on the fixtures.
  """

  def test_flags_and_highs_and_lows(self) -> None:
    member = Permission.READ_EXEC
    self.assertEqual(member.flags, Permission.flags)
    self.assertEqual([*member.highs], [Permission.READ, Permission.EXEC])
    self.assertEqual([*member.lows], [Permission.WRITE])
    #  A low flag above a high one, and a high one between two lows.
    self.assertEqual([f.name for f in Permission.WRITE.lows],
                     ['READ', 'EXEC'])
    self.assertEqual([*member], [Permission.READ, Permission.EXEC])
    self.assertEqual([*Permission.READ.highs], [Permission.READ])
    self.assertEqual(member.names, frozenset(('READ', 'EXEC')))
    self.assertEqual(member.name, 'READ_EXEC')

  def test_null(self) -> None:
    null = Permission.NULL
    self.assertIs(null, KeeFlags.NULL)
    self.assertIs(null, FileAccess.NULL)
    self.assertIs(type(null), KeeFlags)
    self.assertEqual(null.name, 'NULL')
    self.assertEqual(null.names, frozenset())
    self.assertEqual([*null.highs], [])
    self.assertEqual([*null.lows], [])
    self.assertEqual(null.flags, [])
    self.assertEqual(null.value, 'NULL')
    self.assertIsNone(null.kee)

  def test_flags_are_members(self) -> None:
    self.assertIsInstance(Permission.READ, Permission)
    self.assertIs(type(Permission.READ), Permission)
    self.assertIs(Permission.READ.kee.getFieldOwner(), Permission)
    self.assertEqual(Permission.READ.kee.getFieldName(), 'READ')
    self.assertIsNone(Permission.READ_WRITE.kee)

  def test_values(self) -> None:
    self.assertEqual(Permission.READ.value, 'READ')
    self.assertEqual(Permission.READ_WRITE.value, 'READ_WRITE')
    self.assertEqual(FileAccess.OPEN_CLOSE.value, b'OPEN_CLOSE')

    class Numbered(KeeFlags):
      ONE = Kee[int](1)
      TWO = Kee[int](2)

    self.assertEqual(Numbered.ONE.value, 1)
    self.assertEqual(Numbered.ONE_TWO.value, 'ONE_TWO')

  def test_shared_along_the_lineage(self) -> None:
    self.assertIs(Extended.READ, Permission.READ)
    self.assertIs(Extended.READ_WRITE, Permission.READ_WRITE)
    self.assertIs(type(Extended.READ_OWN), Extended)
    self.assertEqual(Permission.READ.owners[:2], (Permission, Extended))
    self.assertEqual(Extended.READ_OWN.owners, (Extended,))

  def test_truth(self) -> None:
    self.assertFalse(Permission.NULL)
    self.assertTrue(Permission.READ)
    self.assertEqual([bool(m) for m in Permission].count(False), 1)

  def test_text(self) -> None:
    class Local(KeeFlags):
      READ = Kee[str]()

    self.assertEqual(str(Local.READ), '<Local>.READ')
    self.assertEqual(repr(Local.READ), '<Local>.READ')

    class Sub(Local):
      WRITE = Kee[str]()

    self.assertEqual(str(Local.READ), '<KeeFlags>.READ')
    self.assertEqual(str(Sub.READ_WRITE), '<Sub>.READ_WRITE')
    self.assertEqual(str(Sub.NULL), '<KeeFlags>.NULL')

  def test_frozen(self) -> None:
    with self.assertRaises(KeeWriteOnceError) as context:
      Permission.READ.extra = 1
    self.assertIs(context.exception.member, Permission.READ)
    self.assertIs(context.exception.keeNum, Permission)
    self.assertEqual(context.exception.attribute, 'extra')
    self.assertIn("'extra' of member '%s'" % Permission.READ,
                  str(context.exception))
    with self.assertRaises(KeeWriteOnceError) as context:
      del Permission.READ.extra
    self.assertIs(context.exception.member, Permission.READ)
    self.assertIs(context.exception.keeNum, Permission)
    self.assertEqual(context.exception.attribute, 'extra')
    self.assertIn("'extra'", str(context.exception))
    with self.assertRaises(KeeWriteOnceError) as context:
      Permission.READ.__member_index__ = 9
    self.assertIs(context.exception.member, Permission.READ)
    self.assertIs(context.exception.keeNum, Permission)
    self.assertEqual(context.exception.attribute, '__member_index__')
    self.assertIn("'__member_index__'", str(context.exception))

  def test_equality_is_identity(self) -> None:
    self.assertEqual(Permission.READ, Permission.READ)
    self.assertEqual(Extended.READ, Permission.READ)
    self.assertNotEqual(Permission.READ, Permission.WRITE)
    self.assertNotEqual(Extended.READ_OWN, Permission.READ)

    class Twin(KeeFlags):
      READ = Kee[str]()

    self.assertEqual(Twin.READ.names, Permission.READ.names)
    self.assertNotEqual(Twin.READ, Permission.READ)
    self.assertIs(Permission.READ.__eq__(Twin.READ), NotImplemented)
    self.assertIs(Permission.READ.__eq__(1), NotImplemented)
    self.assertFalse(Permission.READ == 1)
    self.assertTrue(Permission.READ != 1)

  def test_hash(self) -> None:
    self.assertEqual(hash(Permission.READ), hash(frozenset(('READ',))))
    self.assertEqual(hash(Permission.NULL), hash(frozenset()))
    self.assertEqual({Permission.READ: 1}[Extended.READ], 1)

  def test_operators(self) -> None:
    self.assertIs(Permission.READ | Permission.WRITE, Permission.READ_WRITE)
    self.assertIs(Permission.READ | Permission.READ, Permission.READ)
    self.assertIs(Permission.READ_WRITE & Permission.WRITE, Permission.WRITE)
    self.assertIs(Permission.READ & Permission.WRITE, Permission.NULL)
    self.assertIs(Permission.READ ^ Permission.READ_WRITE, Permission.WRITE)
    self.assertIs(Permission.READ ^ Permission.READ, Permission.NULL)
    self.assertIs(Permission.READ | Permission.NULL, Permission.READ)
    self.assertIs(Extended.OWN | Permission.READ, Extended.READ_OWN)
    self.assertIs(Permission.READ | Extended.OWN, Extended.READ_OWN)
    self.assertIs(Extended.READ_OWN & Permission.READ, Permission.READ)

  def test_inversion(self) -> None:
    self.assertIs(~Permission.READ, Permission.WRITE_EXEC)
    self.assertIs(~Permission.READ_WRITE_EXEC, Permission.NULL)
    #  A member inverts within the class that built it.
    self.assertIs(~Extended.READ, Permission.WRITE_EXEC)
    self.assertIs(~Extended.READ_OWN, Extended.WRITE_EXEC)
    with self.assertRaises(ZeroDivisionError) as context:
      _ = ~Permission.NULL
    self.assertEqual(str(context.exception), str.join(' ', """'NULL'
      combines no flags, and there is no universal combination for it to
      invert to.""".split()))

  def test_combinations_of_several_bases(self) -> None:
    class User(KeeFlags):
      READ = Kee[str]()
      EXEC = Kee[str]()

    class Admin(KeeFlags):
      WRITE = Kee[str]()
      DEL = Kee[str]()

    with self.assertRaises(TypeError):
      _ = User.READ | Admin.WRITE

    class Both(User, Admin):
      pass

    class Staff(Admin, User):
      pass

    self.assertIs(Both.READ, User.READ)
    self.assertIs(Both.READ_EXEC, User.READ_EXEC)
    self.assertIs(User.READ | Admin.WRITE, Both.READ_WRITE)
    self.assertIs(Both.READ_WRITE, Staff.WRITE_READ)
    self.assertIs(type(Both.READ_WRITE), Both)
    self.assertEqual([*(~User.READ)], [User.EXEC])
    self.assertIs(~Both.READ_WRITE, Both.EXEC_DEL)
    self.assertEqual([f.name for f in Both.READ_WRITE.lows],
                     ['EXEC', 'DEL'])

  def test_operators_refuse_strangers(self) -> None:
    for other in (FileAccess.OPEN, 1, 'READ'):
      with self.subTest(other=other):
        with self.assertRaises(TypeError):
          _ = Permission.READ | other
        with self.assertRaises(TypeError):
          _ = Permission.READ ^ other
    for other in (1, 'READ'):
      with self.subTest(other=other):
        with self.assertRaises(TypeError):
          _ = Permission.READ & other
    #  Members of unrelated classes share no flag, and the empty set of
    #  flags is 'NULL', which every flags class holds.
    self.assertIs(Permission.READ & FileAccess.OPEN, KeeFlags.NULL)
    self.assertIs(Permission.READ.__or__(FileAccess.OPEN), NotImplemented)
    self.assertIs(Permission.READ.__and__(1), NotImplemented)
    self.assertIs(Permission.READ.__xor__('READ'), NotImplemented)

  def test_copies_and_pickles_are_the_member(self) -> None:
    self.assertIs(copy.copy(Permission.EXEC), Permission.EXEC)
    self.assertIs(copy.deepcopy(Permission.EXEC), Permission.EXEC)
    self.assertIs(copy.deepcopy([Extended.OWN])[0], Extended.OWN)
    for member in Extended:
      with self.subTest(member=member.name):
        self.assertIs(pickle.loads(pickle.dumps(member)), member)

  def test_cast_hook(self) -> None:
    self.assertIs(typeCast(Permission, 'read_write'), Permission.READ_WRITE)
    self.assertIs(typeCast(Permission, ('READ', 'EXEC')),
                  Permission.READ_EXEC)
    self.assertIs(typeCast(Permission, 6), Permission.WRITE_EXEC)
    self.assertIs(typeCast(Extended, Permission.READ), Permission.READ)
    with self.assertRaises(TypeCastException) as context:
      typeCast(Permission, 'nothing')
    self.assertIs(context.exception.type_, Permission)
    self.assertEqual(context.exception.arg, 'nothing')
    self.assertEqual(str(context.exception),
                     "Unable to cast value 'nothing' to type 'Permission'!")
    self.assertIs(Permission.__cast_as__('nothing'), NotImplemented)
    type.__setattr__(Permission, '__allow_instantiation__', True)
    try:
      self.assertIs(Permission.__cast_as__('read'), NotImplemented)
    finally:
      type.__setattr__(Permission, '__allow_instantiation__', False)
    self.assertIs(Permission.__cast_as__('read'), Permission.READ)

  def test_value_override_applies_to_the_members_built(self) -> None:
    class Weighted(KeeFlags):
      LIGHT = Kee[str]()
      HEAVY = Kee[str]()

      def _getValue(self) -> float:
        return 0.5 * len(self.names)

    class Heavier(Weighted):
      HUGE = Kee[str]()

      def _getValue(self) -> float:
        return float(len(self.names))

    self.assertEqual(Weighted.LIGHT_HEAVY.value, 1.0)
    self.assertEqual(Heavier.LIGHT_HEAVY.value, 1.0)
    self.assertEqual(Heavier.HUGE.value, 1.0)
    self.assertEqual(Heavier.LIGHT_HUGE.value, 2.0)
    self.assertIs(Weighted.valueType, float)
    self.assertIs(Heavier.valueType, float)

  def test_value_override_reads_the_lows(self) -> None:
    class Counted(KeeFlags):
      A = Kee[str]()
      B = Kee[str]()

      def _getValue(self) -> int:
        return len([*self.lows])

    self.assertEqual(Counted.A.value, 1)
    self.assertEqual(Counted.A_B.value, 0)

  def test_random_combinations(self) -> None:
    self.randomInteger.size = 6
    for number in self.randomInteger.row:
      index = number % len(Extended)
      member = Extended[index]
      with self.subTest(index=index):
        self.assertIs(Extended(member.names), member)
        self.assertIs(Extended(*member.names), member)
        self.assertIs(member | Extended.NULL, member)
        self.assertIs(member & member, member)
        self.assertIs(member ^ member, Extended.NULL)
        self.assertEqual([*member], [*member.highs])

  def test_resolve_error_names_the_identifier(self) -> None:
    with self.assertRaises(KeeResolveError) as context:
      Permission('nothing')
    self.assertIs(context.exception.keeNum, Permission)
    self.assertEqual(context.exception.identifier, 'nothing')
    self.assertIn("'Permission' could not resolve the identifier 'nothing'",
                  str(context.exception))

"""
TestKeeFlags tests 'KeeFlags' from 'worktoy.keenum', the members of a
flags class.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import copy
import pickle

from worktoy.keenum import KeeFlags, KeeFlag
from worktoy.utilities import typeCast
from worktoy.waitaminute import MissingVariable, TypeException
from worktoy.waitaminute.dispatch import TypeCastException
from worktoy.waitaminute.keenum import KeeWriteOnceError, KeeResolveError
from . import KeenumTest, Permission, Extended, FileAccess


class TestKeeFlags(KeenumTest):
  """
  A flags member knows its high and low flags, its index, value, name
  and names, is falsy only as 'NULL', equal to the member of a related
  class with the same flags, hashes by its names, combines with the
  three operators and the inversion, survives copies and pickling as
  itself, and refuses every change. The tests pin each on the fixtures.
  """

  def test_flags_and_highs_and_lows(self) -> None:
    member = Permission.READ_EXEC
    self.assertEqual(member.flags, Permission.flags)
    self.assertEqual([f.name for f in member.highs], ['READ', 'EXEC'])
    self.assertEqual([f.name for f in member.lows], ['WRITE'])
    self.assertEqual([f.name for f in member], ['READ', 'EXEC'])
    self.assertEqual([f.name for f in Permission.NULL.highs], [])
    self.assertEqual([f.name for f in Permission.NULL.lows],
                     ['READ', 'WRITE', 'EXEC'])
    self.assertEqual(member.names, frozenset(('READ', 'EXEC')))
    self.assertEqual(Permission.NULL.names, frozenset())
    self.assertEqual(Permission.NULL.name, 'NULL')

  def test_index_and_value(self) -> None:
    self.assertEqual(Permission.READ_WRITE.index, 3)
    self.assertEqual(Permission.READ_WRITE.value, 3)
    self.assertEqual(FileAccess.OPEN_CLOSE.value, b'3')
    loose = KeeFlags.__new__(KeeFlags)
    with self.assertRaises(MissingVariable) as context:
      _ = loose.index
    self.assertIs(context.exception.instance, loose)
    self.assertEqual(context.exception.varName, '__member_index__')
    self.assertEqual(context.exception.expectedTypes, (int,))
    self.assertEqual(str(context.exception),
                     "Missing 'KeeFlags.__member_index__: int'!")
    object.__setattr__(loose, '__member_index__', 'x')
    with self.assertRaises(TypeException) as context:
      _ = loose.index
    self.assertEqual(context.exception.varName, '__member_index__')
    self.assertEqual(context.exception.actualObject, 'x')
    self.assertIs(context.exception.actualType, str)
    self.assertEqual(context.exception.expectedTypes, (int,))
    self.assertIn("'__member_index__'", str(context.exception))

  def test_truth(self) -> None:
    self.assertFalse(Permission.NULL)
    self.assertTrue(Permission.READ)
    self.assertEqual([bool(m) for m in Permission].count(False), 1)

  def test_text(self) -> None:
    self.assertEqual(str(Permission.READ_WRITE), 'Permission.READ_WRITE [3]')
    self.assertEqual(repr(Permission.NULL), 'Permission.NULL [0]')
    self.assertEqual(str(Extended.OWN), 'Extended.OWN [8]')

  def test_frozen(self) -> None:
    with self.assertRaises(KeeWriteOnceError) as context:
      Permission.READ.extra = 1
    self.assertIs(context.exception.member, Permission.READ)
    self.assertIs(context.exception.keeNum, Permission)
    self.assertEqual(context.exception.attribute, 'extra')
    self.assertIn("'extra' of member 'Permission.READ [1]'",
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

  def test_equality(self) -> None:
    self.assertEqual(Permission.READ, Permission.READ)
    self.assertNotEqual(Permission.READ, Permission.WRITE)
    self.assertEqual(Permission.READ_WRITE, Extended.READ_WRITE)
    self.assertEqual(Extended.READ, Permission.READ)
    self.assertNotEqual(Extended.OWN, Permission.READ)
    self.assertIs(Permission.READ.__eq__(FileAccess.OPEN), NotImplemented)
    self.assertFalse(Permission.READ == FileAccess.OPEN)
    self.assertIs(Permission.READ.__eq__(1), NotImplemented)
    self.assertFalse(Permission.READ == 1)
    self.assertTrue(Permission.READ != 1)

  def test_hash(self) -> None:
    self.assertEqual(hash(Permission.READ), hash(frozenset(('READ',))))
    self.assertEqual(hash(Permission.READ), hash(Extended.READ))
    self.assertEqual({Permission.READ: 1}[Extended.READ], 1)
    self.assertEqual(len({Permission.NULL, Extended.NULL}), 1)

  def test_operators(self) -> None:
    self.assertIs(Permission.READ | Permission.WRITE, Permission.READ_WRITE)
    self.assertIs(Permission.READ | Permission.READ, Permission.READ)
    self.assertIs(Permission.READ_WRITE & Permission.WRITE, Permission.WRITE)
    self.assertIs(Permission.READ & Permission.WRITE, Permission.NULL)
    self.assertIs(Permission.READ ^ Permission.READ_WRITE, Permission.WRITE)
    self.assertIs(Permission.READ ^ Permission.READ, Permission.NULL)
    self.assertIs(~Permission.READ, Permission.WRITE_EXEC)
    self.assertIs(~Permission.NULL, Permission.READ_WRITE_EXEC)
    self.assertIs(~Permission.READ_WRITE_EXEC, Permission.NULL)

  def test_operators_across_the_lineage(self) -> None:
    self.assertIs(Extended.OWN | Permission.READ, Extended.READ_OWN)
    self.assertIs(Permission.READ | Extended.OWN, Extended.READ_OWN)
    self.assertIs(Permission.READ | Extended.WRITE, Permission.READ_WRITE)
    self.assertIs(Extended.READ_OWN & Permission.READ, Extended.READ)
    self.assertIs(Permission.READ & Extended.READ_OWN, Extended.READ)
    self.assertIs(Permission.READ ^ Extended.READ_WRITE, Permission.WRITE)
    self.assertIs(Permission.READ._asOwn(Extended.WRITE), Permission.WRITE)
    self.assertIsNone(Permission.READ._asOwn(Extended.OWN))
    self.assertIsNone(Permission.READ._asOwn(FileAccess.OPEN))
    self.assertIsNone(Permission.READ._asOwn(3))

  def test_operators_refuse_strangers(self) -> None:
    for other in (FileAccess.OPEN, 1, 'READ'):
      with self.subTest(other=other):
        with self.assertRaises(TypeError):
          _ = Permission.READ | other
        with self.assertRaises(TypeError):
          _ = Permission.READ & other
        with self.assertRaises(TypeError):
          _ = Permission.READ ^ other
    self.assertIs(Permission.READ.__or__(FileAccess.OPEN), NotImplemented)
    self.assertIs(Permission.READ.__and__(1), NotImplemented)
    self.assertIs(Permission.READ.__xor__('READ'), NotImplemented)

  def test_copies_and_pickles_are_the_member(self) -> None:
    self.assertIs(copy.copy(Permission.EXEC), Permission.EXEC)
    self.assertIs(copy.deepcopy(Permission.EXEC), Permission.EXEC)
    self.assertIs(copy.deepcopy([Extended.OWN])[0], Extended.OWN)
    for member in Permission:
      with self.subTest(member=member.name):
        self.assertIs(pickle.loads(pickle.dumps(member)), member)
    self.assertIs(pickle.loads(pickle.dumps(Extended.READ_OWN)),
                  Extended.READ_OWN)

  def test_cast_hook(self) -> None:
    self.assertIs(typeCast(Permission, 'read_write'), Permission.READ_WRITE)
    self.assertIs(typeCast(Permission, ('READ', 'EXEC')),
                  Permission.READ_EXEC)
    self.assertIs(typeCast(Permission, 6), Permission.WRITE_EXEC)
    self.assertIs(typeCast(Extended, Permission.READ), Extended.READ)
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

  def test_cast_of_a_subclass_member_gives_own_member(self) -> None:
    #  The class docstring: a member of the subclass resolves through
    #  'typeCast' to this class's own member when this class holds every
    #  one of its flags.
    self.assertIs(typeCast(Permission, Extended.READ), Permission.READ)

  def test_value_override_wins(self) -> None:
    class Twice(FileAccess):
      def _getValue(self) -> int:
        return self.index * 2

    self.assertEqual(Twice.OPEN.value, 2)
    self.assertIs(Twice.valueType, int)
    self.assertIs(Twice[2], Twice.CLOSE)
    self.assertIs(Twice._resolveValue(4), Twice.CLOSE)
    with self.assertRaises(KeeResolveError) as context:
      Twice._resolveValue(4.0)
    self.assertIs(context.exception.keeNum, Twice)
    self.assertEqual(context.exception.identifier, 4.0)
    self.assertIn("'Twice' could not resolve the identifier '4.0'",
                  str(context.exception))
    self.assertEqual(FileAccess.OPEN.value, b'1')

  def test_random_combinations(self) -> None:
    self.randomInteger.size = 6
    for number in self.randomInteger.row:
      index = number % len(Extended)
      member = Extended[index]
      with self.subTest(index=index):
        self.assertEqual(member.index, index)
        self.assertIs(Extended(member.names), member)
        self.assertIs(Extended(*member.names), member)
        self.assertIs(member | Extended.NULL, member)
        self.assertIs(member & member, member)
        self.assertIs(member ^ member, Extended.NULL)
        self.assertIs(~~member, member)

  def test_equality_in_both_directions(self) -> None:
    self.assertNotEqual(Permission.WRITE, Permission.READ)
    self.assertNotEqual(Permission.READ, Permission.WRITE)
    self.assertNotEqual(Extended.READ_OWN, Permission.READ)
    self.assertNotEqual(Permission.READ, Extended.READ_OWN)
    self.assertNotEqual(Extended.READ, Permission.READ_WRITE)
    self.assertNotEqual(Permission.READ_WRITE, Extended.READ)
    self.assertEqual(Extended.READ, Permission.READ)
    self.assertEqual(Permission.READ_WRITE, Extended.READ_WRITE)

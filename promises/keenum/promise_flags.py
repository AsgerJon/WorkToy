"""
PromiseFlags promises 'KeeFlags' from 'worktoy.keenum'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import copy
import pickle
from unittest import TestCase

from worktoy.desc import AttriBox
from worktoy.keenum import KeeFlags, KeeFlag
from worktoy.mcls import BaseObject
from worktoy.waitaminute.keenum import KeeFlagNameError, KeeFlagDuplicate
from worktoy.waitaminute.keenum import KeeCaseException, KeeMemberNameError
from worktoy.waitaminute.keenum import KeeResolveError, KeeWriteOnceError

from ._file_access import FileAccess


class PromiseFlags(TestCase):
  """
  A 'KeeFlags' class with N flags declared as 'READ = KeeFlag()' holds
  one member per combination, 2 ** N, 'NULL' included. A member's name
  joins its high flag names by '_' in
  declaration order, or is 'NULL'; it has 'names', a frozenset of them,
  'flags', 'highs' and 'lows', and 'value', which a subclass gives by
  overriding '_getValue'. A call or subscript takes a member, a name in
  any case and flag order, several identifiers or a tuple of them, an
  index or a value, and no arguments gives 'NULL'; a miss raises
  'KeeResolveError'. '|', '&', '^' and '~' give members; 'NULL' is
  falsy, every other member truthy; iterating a member gives its high
  flags; 'in' answers by identity. Members of a subclass and its base
  with the same flags are equal
  and hash alike; combined by an operator, they give the member of the
  class holding every flag. Members are frozen and
  copy and pickle as themselves, and a box over the class converts as a
  call does. A flag name with '_' or 'NULL' raises 'KeeFlagNameError',
  one not upper case 'KeeCaseException', a repeated or inherited one
  'KeeFlagDuplicate', and a body name taken by a member
  'KeeMemberNameError'. Source: the docstrings of 'KeeFlags',
  'KeeFlagsMeta' and 'KeeFlagsSpace', and the 1.1.0 changelog.

  Taken back in 1.2.0, each with its reason in 'promises/confessions':
  the bit mask as the default 'value', members of its own in a
  subclass, and '~' of 'NULL'. Deprecated in 1.2.0, each with its
  reason in 'promises/deprecations': 'KeeFlag', and 'index' on a
  member, the bit mask.
  """

  def test_members(self) -> None:
    names = [m.name for m in FileAccess]
    self.assertEqual(names, ['NULL', 'READ', 'WRITE', 'READ_WRITE',
                             'EXECUTE', 'READ_EXECUTE', 'WRITE_EXECUTE',
                             'READ_WRITE_EXECUTE'])
    member = FileAccess.READ_EXECUTE
    self.assertEqual(member.names, frozenset({'READ', 'EXECUTE'}))
    self.assertEqual([f.name for f in member.highs], ['READ', 'EXECUTE'])
    self.assertEqual([f.name for f in member.lows], ['WRITE'])
    self.assertEqual([f.name for f in member], ['READ', 'EXECUTE'])
    self.assertEqual([f.name for f in member.flags],
                     ['READ', 'WRITE', 'EXECUTE'])

  def test_resolution(self) -> None:
    target = FileAccess.READ_EXECUTE
    for identifier in (target, 'read_execute', 'EXECUTE_READ', 5,
                       ('READ', 'EXECUTE')):
      with self.subTest(identifier=identifier):
        self.assertIs(FileAccess(identifier), target)
        self.assertIs(FileAccess[identifier], target)
    self.assertIs(FileAccess('READ', 'EXECUTE'), target)
    self.assertIs(FileAccess(), FileAccess.NULL)
    for miss in ('APPEND', 8, -1):
      with self.subTest(miss=miss):
        with self.assertRaises(KeeResolveError):
          FileAccess(miss)

  def test_operators(self) -> None:
    read, write = FileAccess.READ, FileAccess.WRITE
    self.assertIs(read | write, FileAccess.READ_WRITE)
    self.assertIs(FileAccess.READ_WRITE & write, write)
    self.assertIs(FileAccess.READ_WRITE ^ write, read)
    self.assertIs(~read, FileAccess.WRITE_EXECUTE)
    self.assertFalse(FileAccess.NULL)
    self.assertTrue(read)
    self.assertIn(read, FileAccess)
    self.assertNotIn('READ', FileAccess)

  def test_lineage(self) -> None:
    class Extended(FileAccess):
      APPEND = KeeFlag()

    self.assertEqual(Extended.READ, FileAccess.READ)
    self.assertEqual(hash(Extended.READ), hash(FileAccess.READ))
    self.assertIs(FileAccess(Extended.READ), FileAccess.READ)
    self.assertEqual(len(Extended), 16)
    self.assertIs(Extended.APPEND | FileAccess.READ, Extended.READ_APPEND)
    self.assertIs(FileAccess.READ | Extended.APPEND, Extended.READ_APPEND)

  def test_value_override(self) -> None:
    class Weighted(KeeFlags):
      LIGHT = KeeFlag()
      HEAVY = KeeFlag()

      def _getValue(self) -> float:
        return 0.5 * self.index

    self.assertEqual(Weighted.HEAVY.value, 1.0)
    self.assertIs(Weighted(1.5), Weighted.LIGHT_HEAVY)

  def test_frozen_and_copies(self) -> None:
    member = FileAccess.READ
    with self.assertRaises(KeeWriteOnceError):
      member.index = 3
    self.assertIs(copy.deepcopy(member), member)
    self.assertIs(pickle.loads(pickle.dumps(member)), member)

  def test_box(self) -> None:
    class Document(BaseObject):
      access = AttriBox[FileAccess](FileAccess.READ)

    document = Document()
    document.access = ('read', 'write')
    self.assertIs(document.access, FileAccess.READ_WRITE)

  def test_refusals(self) -> None:
    with self.assertRaises(KeeFlagNameError) as context:
      class Underscore(KeeFlags):
        READ_ONLY = KeeFlag()
    self.assertEqual(context.exception.name, 'READ_ONLY')
    with self.assertRaises(KeeFlagNameError):
      class Null(KeeFlags):
        NULL = KeeFlag()
    with self.assertRaises(KeeCaseException):
      class Lower(KeeFlags):
        read = KeeFlag()
    with self.assertRaises(KeeFlagDuplicate) as context:
      class Again(FileAccess):
        READ = KeeFlag()
    self.assertEqual(context.exception.name, 'READ')
    with self.assertRaises(KeeMemberNameError) as context:
      class Taken(KeeFlags):
        READ = KeeFlag()
        WRITE = KeeFlag()
        READ_WRITE = 3
    self.assertEqual(context.exception.memberName, 'READ_WRITE')

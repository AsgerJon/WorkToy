"""
RefusedFlags holds the refusals that belong with
'design.promises.keenum.promise_flags'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.keenum import KeeFlags, KeeFlag
from worktoy.waitaminute.keenum import KeeFlagNameError, KeeFlagDuplicate
from worktoy.waitaminute.keenum import KeeCaseException, KeeMemberNameError
from worktoy.waitaminute.keenum import KeeResolveError, KeeWriteOnceError

from ...promises.keenum._file_access import FileAccess


class RefusedFlags(TestCase):
  """
  Each of the following is refused, and the exception named is the one raised
  as of 1.2.3. A call or subscript that finds no member raises
  'KeeResolveError'. A flag name with '_' or 'NULL' raises
  'KeeFlagNameError', one not upper case 'KeeCaseException', a repeated or
  inherited one 'KeeFlagDuplicate', and a body name taken by a member
  'KeeMemberNameError'. Source: the docstrings of 'KeeFlags', 'KeeFlagsMeta'
  and 'KeeFlagsSpace', and the 1.1.0 changelog.
  """

  def test_frozen_and_copies(self) -> None:
    member = FileAccess.READ
    with self.assertRaises(Exception) as refused:
      member.index = 3
    self.assertIsInstance(refused.exception, KeeWriteOnceError)

  def test_refusals_1(self) -> None:
    with self.assertRaises(Exception) as refused:
      class Underscore(KeeFlags):
        READ_ONLY = KeeFlag()
    self.assertIsInstance(refused.exception, KeeFlagNameError)

  def test_refusals_2(self) -> None:
    with self.assertRaises(Exception) as refused:
      class Null(KeeFlags):
        NULL = KeeFlag()
    self.assertIsInstance(refused.exception, KeeFlagNameError)

  def test_refusals_3(self) -> None:
    with self.assertRaises(Exception) as refused:
      class Lower(KeeFlags):
        read = KeeFlag()
    self.assertIsInstance(refused.exception, KeeCaseException)

  def test_refusals_4(self) -> None:
    with self.assertRaises(Exception) as refused:
      class Again(FileAccess):
        READ = KeeFlag()
    self.assertIsInstance(refused.exception, KeeFlagDuplicate)

  def test_refusals_5(self) -> None:
    with self.assertRaises(Exception) as refused:
      class Taken(KeeFlags):
        READ = KeeFlag()
        WRITE = KeeFlag()
        READ_WRITE = 3
    self.assertIsInstance(refused.exception, KeeMemberNameError)

  def test_resolution(self) -> None:
    for miss in ('APPEND', 8, -1):
      with self.subTest(miss=miss):
        with self.assertRaises(Exception) as refused:
          FileAccess(miss)
        self.assertIsInstance(refused.exception, KeeResolveError)

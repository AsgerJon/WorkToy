"""
TestKeeNumExceptions tests the KeeNum exceptions raised by the
'worktoy.keenum' module.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase
from typing import TYPE_CHECKING

from worktoy.keenum import KeeNum
from worktoy.waitaminute.keenum import KeeNumTypeException, EmptyKeeNumError
from worktoy.waitaminute.keenum import DuplicateKeeNum

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestKeeNumExceptions(TestCase):
  """
  TestKeeNumExceptions tests the KeeNum exceptions raised by the
  'worktoy.keenum' module.
  """

  @classmethod
  def tearDownClass(cls) -> None:
    import sys
    import gc
    sys.modules.pop(__name__, None)
    gc.collect()

  def test_duplicate_implementation(self) -> None:
    """
    Test that a KeeNum class with multiple entries correctly raises a
    DuplicateKeeNum exception.
    """
    with self.assertRaises(DuplicateKeeNum) as context:
      class Sus(KeeNum):
        BREH = 69
        BREH = 420
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertEqual(e.memberName, 'BREH')
    self.assertEqual(e.memberValue, 420)

  def test_keenum_type_exception(self) -> None:
    """
    Tests that the KeeNumTypeException is raised with the correct
    parameters.
    """
    with self.assertRaises(KeeNumTypeException) as context:
      class Sus(KeeNum):
        FOO = 69
        BAR = '420'
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertEqual(e.memberName, 'BAR')
    self.assertEqual(e.memberValue, '420')

  def test_empty_keenum_error(self) -> None:
    """
    Tests that the EmptyKeeNumError is raised when a KeeNum class is
    instantiated without any members.
    """
    with self.assertRaises(EmptyKeeNumError) as context:
      class EmptyKeeNum(KeeNum):
        pass
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertEqual(str(e), repr(e))
    self.assertEqual(e.className, 'EmptyKeeNum')

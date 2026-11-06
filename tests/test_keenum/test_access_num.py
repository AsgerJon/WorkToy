"""
TestAccessNum tests 'AccessNum' from 'worktoy.keenum'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import AccessNum, KeeNum
from . import KeenumTest


class TestAccessNum(KeenumTest):
  """
  'AccessNum' names the three descriptor operations with their dunder
  names as values. The tests pin the members, their values and the
  three lookups.
  """

  def test_members(self) -> None:
    self.assertIsSubclass(AccessNum, KeeNum)
    self.assertEqual([m.name for m in AccessNum], ['GET', 'SET', 'DELETE'])
    self.assertEqual([m.value for m in AccessNum],
                     ['__get__', '__set__', '__delete__'])
    self.assertIs(AccessNum.valueType, str)
    self.assertEqual(len(AccessNum), 3)

  def test_lookups(self) -> None:
    self.assertIs(AccessNum('__set__'), AccessNum.SET)
    self.assertIs(AccessNum['delete'], AccessNum.DELETE)
    self.assertIs(AccessNum[0], AccessNum.GET)
    self.assertIs(AccessNum.fromValue('__get__'), AccessNum.GET)

"""
TestHashing provides tests specifically for hashing of 'KeeNum' and
'KeeFlags' allowing their use as dictionary keys and set members.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import KeeNum, Kee
from . import KeeTest


class TestHashing(KeeTest):
  """
  TestHashing provides tests specifically for hashing of 'KeeNum' and
  'KeeFlags' allowing their use as dictionary keys and set members.
  """

  def testHashFlags(self) -> None:
    """Tests that KeeFlags instances can be used as dictionary keys."""
    for cls in self.exampleFlags:
      self.assertIsInstance(hash(cls), int)

  def testHashNums(self) -> None:
    """Tests that KeeNum instances can be used as dictionary keys."""
    for cls in self.exampleNums:
      self.assertIsInstance(hash(cls), int)

  def testDictClass(self, ) -> None:
    """
    Tests that subclasses of both KeeNum and KeeFlags work as dictionary
    keys.
    """
    data = dict()
    for cls in self.exampleFlags:
      data[cls] = type(cls)
    for cls in self.exampleNums:
      data[cls] = type(cls)

    for key, val in data.items():
      self.assertIsInstance(key, val)

  def testSetClass(self) -> None:
    """
    Tests that subclasses of both KeeNum and KeeFlags work as set
    members.
    """
    evens = set()
    odds = set()
    flagNums = [*self.exampleFlags, *self.exampleNums, ]
    for i, cls in enumerate(flagNums):
      odds.add(cls) if i % 2 else evens.add(cls)

    for element in odds:
      self.assertIn(element, odds)
      self.assertNotIn(element, evens)
    for element in evens:
      self.assertIn(element, evens)
      self.assertNotIn(element, odds)

  def testUnhashableValueMember(self) -> None:
    """
    A member whose value is unhashable is itself unhashable: hashing it
    raises 'TypeError' naming the member and its value type, keeping the
    member-side hash semantics consistent with the value side.
    """

    class ListNum(KeeNum):
      A = Kee[list]([1, 2, 3])
      B = Kee[list]([4, 5, 6])

    with self.assertRaises(TypeError) as context:
      hash(ListNum.A)
    self.assertIn('unhashable', str(context.exception))

  def testInstanceFlags(self) -> None:
    """
    Tests that instances of KeeFlags subclasses can be used as
    dictionary keys.
    """
    for cls in self.exampleFlags:
      for member in cls:
        self.assertIsInstance(hash(member), int)

  def testInstanceNums(self) -> None:
    """
    Tests that instances of KeeNum subclasses can be used as
    dictionary keys.
    """
    for cls in self.exampleNums:
      for member in cls:
        self.assertIsInstance(hash(member), int)

  def testDictInstance(self) -> None:
    """
    Tests that instances of both KeeNum and KeeFlags work as
    dictionary keys.
    """
    data = dict()
    for cls in self.exampleFlags:
      for member in cls:
        data[member] = cls
    for cls in self.exampleNums:
      for member in cls:
        data[member] = cls

    for key, val in data.items():
      self.assertIsInstance(key, val)

  def testSetInstance(self, ) -> None:
    """
    Tests that instances of both KeeNum and KeeFlags work as set
    members.
    """
    evens = set()
    odds = set()
    for cls in self.exampleFlags:
      for i, member in enumerate(cls):
        odds.add(member) if i % 2 else evens.add(member)
    for cls in self.exampleNums:
      for i, member in enumerate(cls):
        odds.add(member) if i % 2 else evens.add(member)

    for element in odds:
      self.assertIn(element, odds)
      self.assertNotIn(element, evens)
    for element in evens:
      self.assertIn(element, evens)
      self.assertNotIn(element, odds)

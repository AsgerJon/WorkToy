"""
Tests for the KeeFlags class from the 'worktoy.keenum' package.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import Kee, KeeFlags
from worktoy.waitaminute import TypeException
from worktoy.waitaminute.keenum import KeeDuplicate, KeeNameError
from . import FileAccess, KeeTest


class TestFileAccess(KeeTest):
  """Unit tests for FileAccess flag behavior."""

  def testSingleFlags(self) -> None:
    """Test single flag values."""
    self.assertEqual(FileAccess.READ.value, 1)
    self.assertEqual(FileAccess.WRITE.value, 2)
    self.assertEqual(FileAccess.EXECUTE.value, 4)
    self.assertEqual(FileAccess.DELETE.value, 8)

  def testComboNamesAndValues(self) -> None:
    """Test combos and names."""
    combo = FileAccess.READ.value | FileAccess.WRITE.value
    comboNum = FileAccess.fromValue(combo)
    self.assertEqual(comboNum.name, 'READ_WRITE')
    self.assertEqual(comboNum.value, 3)
    allPerms = FileAccess.READ.value
    allPerms |= FileAccess.WRITE.value
    allPerms |= FileAccess.EXECUTE.value
    allPerms |= FileAccess.DELETE.value
    allPermsNum = FileAccess.fromValue(allPerms)
    expectedNames = set('READ_WRITE_EXECUTE_DELETE'.split('_'))
    actualNames = set(allPermsNum.name.split('_'))
    self.assertEqual(expectedNames, actualNames)
    self.assertEqual(allPermsNum.value, 15)
    self.assertIs(FileAccess['READ'], FileAccess.READ)

  def test_bad_flag_type(self) -> None:
    """Test flag types."""
    with self.assertRaises(TypeException) as context:
      class FileDerp(FileAccess):
        DERP = Kee[str]('69420')
    e = context.exception
    self.assertEqual(str(e), repr(e))

  def test_bad_flag_value(self) -> None:
    """Test flag values."""
    with self.assertRaises(KeeDuplicate) as context:
      class FileDerp(FileAccess):
        READ = Kee[int](69420)
    e = context.exception
    self.assertEqual(str(e), repr(e))

  def test_coverage_gymnastics(self) -> None:
    """Test coverage gymnastics."""
    self.assertIs(FileAccess.flagType, int)
    self.assertEqual(FileAccess.READ.value, 0b0001)
    self.assertIs(FileAccess['read'], FileAccess.READ)
    self.assertIs(getattr(FileAccess, 'read'), FileAccess.READ)
    expected = FileAccess.READ_EXECUTE
    actual = getattr(FileAccess, '_execute_read_')
    self.assertIs(actual, expected)
    with self.assertRaises(KeeNameError) as context:
      _ = FileAccess['lemme access them files!']
    e = context.exception
    self.assertEqual(e.name, 'lemme access them files!')
    self.assertEqual(str(e), repr(e))
    self.assertFalse(KeeFlags.flags)
    for flag in FileAccess:
      self.assertIs(FileAccess.ALL | flag, FileAccess.ALL)

  def testOrDunder(self) -> None:
    """Test bitwise OR returns correct combo instance."""
    combo = FileAccess.READ | FileAccess.WRITE
    self.assertIsInstance(combo, FileAccess)
    self.assertEqual(combo.value, 3)
    self.assertEqual(combo.name, 'READ_WRITE')

  def testAndDunder(self) -> None:
    """Test bitwise AND returns intersection instance."""
    readWrite = FileAccess.READ | FileAccess.WRITE
    anded = readWrite & FileAccess.WRITE
    self.assertEqual(anded, FileAccess.WRITE)
    none = FileAccess.READ & FileAccess.WRITE
    self.assertEqual(none, FileAccess.NULL)

  def testXorDunder(self) -> None:
    """Test bitwise XOR returns expected instance."""
    xor = FileAccess.READ ^ FileAccess.WRITE
    self.assertEqual(xor.value, 3)
    self.assertEqual(xor.name, 'READ_WRITE')
    self.assertEqual(xor ^ FileAccess.WRITE, FileAccess.READ)

  def testInvertDunder(self) -> None:
    """Test invert operator returns complement within defined flags."""
    # For FileAccess, defined bits are 0b1111 = 15
    expected = FileAccess.WRITE_EXECUTE_DELETE
    actual = ~FileAccess.READ
    self.assertIs(actual, expected)

  def testBoolDunder(self) -> None:
    """Test __bool__ returns False only for NULL."""
    self.assertFalse(bool(FileAccess.NULL))
    self.assertTrue(bool(FileAccess.READ))
    self.assertTrue(bool(FileAccess.READ | FileAccess.WRITE))

  def testOrNotImplemented(self) -> None:
    """Test __or__ returns NotImplemented for non-KeeFlags."""
    left = FileAccess.READ
    right = 42
    result = FileAccess.__or__(left, right)
    self.assertIs(result, NotImplemented)
    with self.assertRaises(TypeError):
      _ = left | right

  def testAndNotImplemented(self) -> None:
    """Test __and__ returns NotImplemented for non-KeeFlags."""
    left = FileAccess.READ
    right = None
    result = FileAccess.__and__(left, right)
    self.assertIs(result, NotImplemented)
    with self.assertRaises(TypeError):
      _ = left & right

  def testXorNotImplemented(self) -> None:
    """Test __xor__ returns NotImplemented for non-KeeFlags."""
    left = FileAccess.READ
    right = 'abc'
    result = FileAccess.__xor__(left, right)
    self.assertIs(result, NotImplemented)
    with self.assertRaises(TypeError):
      _ = left ^ right

  def testEqNotImplemented(self) -> None:
    """Test __eq__ returns NotImplemented for non-KeeFlags."""
    left = FileAccess.READ
    right = object()
    result = FileAccess.__eq__(left, right)
    self.assertIs(result, NotImplemented)
    self.assertNotEqual(left, right)  # Should fall back to default

  def testDictKey(self) -> None:
    """Test that KeeFlags members can be used as dict keys."""
    mapping = {
        FileAccess.READ                   : 'read',
        FileAccess.WRITE                  : 'write',
        FileAccess.EXECUTE                : 'execute',
        FileAccess.DELETE                 : 'delete',
        FileAccess.NULL                   : 'none',
        FileAccess.READ | FileAccess.WRITE: 'read/write',
    }
    self.assertEqual(mapping[FileAccess.READ], 'read')
    self.assertEqual(mapping[FileAccess.WRITE], 'write')
    expected = 'read/write'
    actual = mapping[FileAccess.READ | FileAccess.WRITE]
    self.assertEqual(actual, expected)
    self.assertEqual(mapping[FileAccess.NULL], 'none')
    # Keys with equivalent values resolve to the same entry
    combo = FileAccess.READ | FileAccess.WRITE
    self.assertIs(combo, FileAccess.READ_WRITE)
    self.assertEqual(mapping[combo], 'read/write')

  def testSetUniqueness(self) -> None:
    """Flags and combos are unique and set membership works."""
    s = set()
    s.add(FileAccess.READ)
    s.add(FileAccess.WRITE)
    s.add(FileAccess.READ | FileAccess.WRITE)
    s.add(FileAccess.READ_WRITE)  # Should not duplicate
    s.add(FileAccess.EXECUTE)
    s.add(FileAccess.DELETE)
    s.add(FileAccess.NULL)
    # All distinct flags and combos are present, no collisions
    self.assertEqual(len(s), 6)
    self.assertIn(FileAccess.READ, s)
    self.assertIn(FileAccess.WRITE, s)
    self.assertIn(FileAccess.READ_WRITE, s)
    self.assertIn(FileAccess.EXECUTE, s)
    self.assertIn(FileAccess.DELETE, s)
    self.assertIn(FileAccess.NULL, s)

  def testComboIdentityAndHash(self) -> None:
    """Equivalent combos are identical and hash to the same value."""
    a = FileAccess.READ | FileAccess.WRITE
    b = FileAccess.WRITE | FileAccess.READ
    c = FileAccess.READ_WRITE
    # All should be same object (singleton property)
    self.assertIs(a, b)
    self.assertIs(b, c)
    self.assertEqual(hash(a), hash(c))
    self.assertEqual(a, c)
    s = {a, b, c}
    self.assertEqual(len(s), 1)

  def testSetNoCollisions(self) -> None:
    """Distinct combos have distinct hashes and do not collide."""
    allNames = [i.name for i in FileAccess.flags]
    all_flags = [getattr(FileAccess, i) for i in allNames if i != 'NULL']
    from itertools import combinations
    combos = set()
    for r in range(1, len(all_flags) + 1):
      for combo in combinations(all_flags, r):
        val = FileAccess.NULL
        for flag in combo:
          val = val | flag
        combos.add(val)
    # There should be 15 non-NULL combos for 4 flags (2^4 - 1)
    self.assertEqual(len(combos), 15)
    # No accidental hash collision between distinct flag sets
    hashes = set(hash(c) for c in combos)
    self.assertEqual(len(hashes), 15)

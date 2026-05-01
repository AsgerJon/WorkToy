"""
TestSlicedLoad tests that the dreaded 'slice' overload no longer causes
issues with the late failure mechanism. Generally, when passing anything
at all to 'slice', it will always instantiate. If what was passed to it
ought not to have instantiated, a 'TypeError' is raised only on usage
attempts.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.work_test import BaseTest
from . import FruitNinja, DataArray
from worktoy.waitaminute.dispatch import DispatchException

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestSlicedLoad(BaseTest):
  """
  TestSlicedLoad tests that the dreaded 'slice' overload no longer causes
  issues with the late failure mechanism. Generally, when passing anything
  at all to 'slice', it will always instantiate. If what was passed to it
  ought not to have instantiated, a 'TypeError' is raised only on usage
  attempts.
  """

  def setUp(self, ) -> None:
    super().setUp()
    self.fruitNinja = FruitNinja()

  def test_get_item_int(self) -> None:
    indices = [-420, -69, -1, *(i for i, _ in enumerate(self.fruitNinja))]
    for index in indices:
      ninja = self.fruitNinja[index]
      self.assertIsInstance(ninja, str)

  def test_get_item_slice(self) -> None:
    ez = self.fruitNinja[0:1]
    self.assertIsInstance(ez, tuple)
    self.assertEqual(len(ez), 1)
    self.assertEqual(ez[0], self.fruitNinja[0])
    mid = self.fruitNinja[1:4]
    self.assertIsInstance(mid, tuple)
    self.assertEqual(len(mid), 3)
    self.assertEqual(mid[0], self.fruitNinja[1])
    self.assertEqual(mid[1], self.fruitNinja[2])
    self.assertEqual(mid[2], self.fruitNinja[3])
    hard = self.fruitNinja[::2]
    self.assertIsInstance(hard, tuple)
    expectedLength = len(self.fruitNinja) // 2 + len(self.fruitNinja) % 2
    self.assertEqual(len(hard), expectedLength)
    darkSouls = self.fruitNinja[:]
    self.assertIsInstance(darkSouls, tuple)
    self.assertEqual(len(darkSouls), len(self.fruitNinja))
    for i, fruit in enumerate(self.fruitNinja):
      self.assertEqual(darkSouls[i], fruit)

  def test_get_item_bad_type(self) -> None:
    """
    This method tests that bad types are *not* being yolo'd into a slice
    object, but instead leads to a 'DispatchException'.
    """
    try:
      from typing import Never
    except ImportError:  # pragma: no cover
      Never = object()
    badTypes = [
      """never gonna give""",
      type('you_up', (), dict()),
      lambda never: 'gonna',
      dict(let='you', down=''),
      Never,
      'gonna',
      lambda run: 'around' and 'desert you',
    ]
    for badType in badTypes:
      with self.assertRaises(DispatchException) as context:
        _ = self.fruitNinja[badType]
      e = context.exception
      self.assertIs(e.dispatch, FruitNinja.__getitem__)
      self.assertEqual(e.args, (badType,))

  def test_get_item_index_error(self) -> None:
    """
    Testing that out-of-bounds indices raise 'IndexError' as expected.
    """
    for index in [69, 420, 1337, 80085, 8008135]:
      with self.assertRaises(IndexError) as context:
        _ = self.fruitNinja[index]
      e = context.exception
      self.assertIn('index out of range', str(e))

  def test_get_item_overloaded(self, ) -> None:
    """
    Testing that the 'slice' overload is indeed being used, and not the
    'int' overload.
    """
    lines = (
      """never gonna give you up""",
      """never gonna let you down""",
      """never gonna run around and desert you""",
      """never gonna make you cry""",
      """never gonna say goodbye""",
      """never gonna tell a lie and hurt you""",
    )
    data = DataArray(*lines, )
    for line, item in zip(lines, data):
      self.assertEqual(line, item)
    intIndices = [-420, -69, -1, 0, 1, 2, 3, 4, 5]
    rolledIndices = [i % 6 for i in intIndices]
    expectedInts = [lines[i] for i in rolledIndices]
    strIndices = ['give', 'let', 'run', 'make', 'say', 'tell']
    expectedStrs = [*lines, ]
    sliceIndices = []
    fakeSlices = []
    expectedSlices = []
    for i, _ in enumerate(intIndices):
      for j, __ in enumerate(intIndices):
        sliceIndices.append(slice(i, j))
        expectedSlices.append((*lines,)[i:j])
        fakeSlices.append((i, j))
    for index, expected in zip(intIndices, expectedInts):
      item = data[index]
      self.assertEqual(item, expected)
    for index, expected in zip(strIndices, expectedStrs):
      item = data[index]
      self.assertEqual(item, expected)
    for index, expected in zip(sliceIndices, expectedSlices):
      item = data[index]
      self.assertEqual(item, expected)

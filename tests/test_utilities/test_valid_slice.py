"""
TestValidSlice tests the ValidSlice class.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.utilities import ValidSlice, typeCast, ExceptionInfo
from worktoy.waitaminute.dispatch import TypeCastException
from . import UtilitiesTest, Freddy, TrollSlice, EvilSlice, DataArray

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestValidSlice(UtilitiesTest):

  def setUp(self, ) -> None:
    super().setUp()
    self.goodSlices = (
      Freddy()[::],
      Freddy()[::-1],
      Freddy()[1:10:2],
      Freddy()[0:5],
    )
    self.badSlices = (
      slice(1.5, 10, 2),
      slice(0, '5'),
      slice([1, 2, 3]),
      slice(None, None, 'step'),
    )
    self.nonSlices = (
      """imma slice, trust me bro!""",
      42,
      [1, 2, 3],
      {'start': 1, 'stop': 10, 'step': 2},
    )
    self.trollSlices = (*(Freddy()[(TrollSlice())] for _ in range(7)),)
    self.evilSlices = (*(Freddy()[(EvilSlice())] for _ in range(7)),)

  def test_good_slices(self, ) -> None:
    for good in self.goodSlices:
      self.assertIsInstance(good, ValidSlice)

  def test_bad_slices(self, ) -> None:
    for bad in self.badSlices:
      self.assertNotIsInstance(bad, ValidSlice)

  def test_non_slices(self, ) -> None:
    for non in self.nonSlices:
      self.assertNotIsInstance(non, ValidSlice)

  def test_troll_slices(self, ) -> None:
    for troll in self.trollSlices:
      self.assertNotIsInstance(troll, ValidSlice)

  def test_evil_slices(self, ) -> None:
    for evil in self.evilSlices:
      self.assertIsInstance(evil, ValidSlice)

  def test_instantiation(self, ) -> None:
    with self.assertRaises(TypeError):
      ValidSlice()

  def test_str(self, ) -> None:
    infoSpec = """<type '%s' | slice object validator>"""
    info = infoSpec % ValidSlice.__name__
    self.assertEqual(str(ValidSlice), info)

  def test_repr(self, ) -> None:
    infoSpec = """worktoy.utilities.%s"""
    info = infoSpec % ValidSlice.__name__
    self.assertEqual(repr(ValidSlice), info)

  def test_casting_bad_slice(self) -> None:
    sus = slice("""Hey, I'm a slice, trust me bro!""")
    with self.assertRaises(TypeCastException) as context:
      _ = typeCast(slice, sus)
    e = context.exception
    self.assertIs(e.arg, sus)
    self.assertIs(e.type_, slice)

    with self.assertRaises(TypeCastException) as context:
      _ = typeCast(slice, ('never', 'gonna', 'give', 'you', 'up'))
    e = context.exception
    self.assertEqual(e.arg, ('never', 'gonna', 'give', 'you', 'up'))
    self.assertIs(e.type_, slice)

  def test_casting_good_slice(self, ) -> None:
    arg = 69
    self.assertEqual(slice(0), slice(0))
    self.assertEqual(slice(arg), typeCast(slice, arg))
    casted = typeCast(slice, slice(0, 10, 2))
    self.assertIsInstance(casted, slice)
    self.assertEqual(casted.start, 0)
    self.assertEqual(casted.stop, 10)
    self.assertEqual(casted.step, 2)
    casted = typeCast(slice, (0, 1))
    self.assertIsInstance(casted, slice)
    self.assertEqual(casted.start, 0)
    self.assertEqual(casted.stop, 1)
    self.assertEqual(casted.step, None)

  def test_data_array(self) -> None:
    lines = (
      """never gonna give you up""",
      """never gonna let you down""",
      """never gonna run around and desert you""",
      """never gonna make you cry""",
      """never gonna say goodbye""",
      """never gonna tell a lie and hurt you""",
    )
    data = DataArray(*lines, )
    self.assertEqual(data[-4], data[2])
    with self.assertRaises(IndexError):
      _ = data[69]
    self.assertEqual(data['give'], data['never gonna give'])
    self.assertEqual(data[str.upper('give')], data['give'])
    with self.assertRaises(KeyError):
      _ = data["""Together forever and never to part"""]

  def test_evil_slice(self, ) -> None:
    with self.assertRaises(TypeError) as context:
      _ = ()[EvilSlice()]
    e = context.exception
    self.assertIn("""__index__ returned non-int""", str(e))

  def test_freddy(self, ) -> None:
    samples = (*Freddy.randSlices(7, ), *Freddy.randSlices())
    for freddy in samples:
      self.assertIsInstance(freddy, slice)
      self.assertIsInstance(freddy, ValidSlice)

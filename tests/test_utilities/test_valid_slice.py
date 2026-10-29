"""
TestValidSlice tests the ValidSlice class.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.utilities import ValidSlice, typeCast
from worktoy.waitaminute.dispatch import TypeCastException
from . import UtilitiesTest, Freddy, TrollSlice, EvilSlice, DataArray


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

  def test_slice_not_cast(self) -> None:
    """'typeCast' passes a slice through as an instance, 'ValidSlice' or
    not, and refuses every other value, since 'slice' is no cast target
    and 'ValidSlice' is a validator alone."""
    sus = slice("""Hey, I'm a slice, trust me bro!""")
    self.assertIs(typeCast(slice, sus), sus)
    good = slice(0, 10, 2)
    self.assertIs(typeCast(slice, good), good)
    for value in (69, (0, 1), ('never', 'gonna', 'give', 'you', 'up')):
      with self.subTest(value=value):
        with self.assertRaises(TypeCastException) as context:
          _ = typeCast(slice, value)
        self.assertIs(context.exception.type_, slice)
        self.assertEqual(context.exception.arg, value)

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

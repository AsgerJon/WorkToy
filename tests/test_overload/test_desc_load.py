"""
TestDescLoad tests the 'DescLoad' scenario overloading scenario.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from . import DescLoad, OverloadTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Self, TypeAlias

  IntSample: TypeAlias = list[tuple[int, ...]]


class TestDescLoad(OverloadTest):
  """
  TestDescLoad tests the 'DescLoad' scenario overloading scenario.
  """

  def test_good_init(self) -> Self:
    """Tests the initialization of the TestDescLoad class."""

    descSample = DescLoad()
    thisSample = DescLoad(descSample)
    self.assertEqual(descSample, thisSample)
    self.assertIn('()', descSample.loaded)

    for sample in self.generateRandomIntegers(1, 255, 0, 256):
      x, = sample
      descSample = DescLoad(x)
      thisSample = DescLoad(descSample)
      self.assertEqual(descSample, thisSample)
      self.assertEqual(x, descSample.x)
      self.assertIn('(int)', descSample.loaded)

    for sample in self.generateRandomIntegers(2, 255, 0, 256):
      x, y = sample
      descSample = DescLoad(x, y)
      thisSample = DescLoad(descSample)
      self.assertEqual(descSample, thisSample)
      self.assertEqual(x, descSample.x)
      self.assertEqual(y, descSample.y)
      self.assertIn('(int, int)', descSample.loaded)

    for sample in self.generateRandomIntegers(3, 255, 0, 256):
      x, y, z = sample
      descSample = DescLoad(x, y, z)
      thisSample = DescLoad(descSample)
      self.assertEqual(descSample, thisSample)
      self.assertEqual(x, descSample.x)
      self.assertEqual(y, descSample.y)
      self.assertEqual(z, descSample.z)
      self.assertIn('(int, int, int)', descSample.loaded)

    for sample in self.generateRandomIntegers(4, 255, 0, 256):
      x, y, z, u = sample
      descSample = DescLoad(x, y, z, u)
      thisSample = DescLoad(descSample)
      self.assertEqual(descSample, thisSample)
      self.assertEqual(x, descSample.x)
      self.assertEqual(y, descSample.y)
      self.assertEqual(z, descSample.z)
      self.assertEqual(u, descSample.u)
      self.assertIn('(int, int, int, int)', descSample.loaded)

    for sample in self.generateRandomIntegers(5, 255, 0, 256):
      x, y, z, u, v = sample
      descSample = DescLoad(x, y, z, u, v)
      thisSample = DescLoad(descSample)
      self.assertEqual(descSample, thisSample)
      self.assertEqual(x, descSample.x)
      self.assertEqual(y, descSample.y)
      self.assertEqual(z, descSample.z)
      self.assertEqual(u, descSample.u)
      self.assertEqual(v, descSample.v)
      self.assertIn('(int, int, int, int, int)', descSample.loaded)

    for sample in self.generateRandomIntegers(6, 255, 0, 256):
      x, y, z, u, v, w = sample
      descSample = DescLoad(x, y, z, u, v, w)
      thisSample = DescLoad(descSample)
      self.assertEqual(descSample, thisSample)
      self.assertEqual(x, descSample.x)
      self.assertEqual(y, descSample.y)
      self.assertEqual(z, descSample.z)
      self.assertEqual(u, descSample.u)
      self.assertEqual(v, descSample.v)
      self.assertEqual(w, descSample.w)
      self.assertIn('(int, int, int, int, int, int)', descSample.loaded)

  def test_not_eq(self, ) -> None:
    """Tests the 'not equal' operator."""
    descSample = DescLoad()
    self.assertNotEqual(descSample, 'breh')
    descSample2 = DescLoad(1, 2, 3, 4, 5, 6)
    self.assertNotEqual(descSample, descSample2)
    self.assertEqual(str(descSample2), repr(descSample2))

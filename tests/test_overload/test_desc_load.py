"""
TestDescLoad tests the 'DescLoad' scenario overloading scenario.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.work_test.samplers import IntSampler
from worktoy.dispatch import TypeSig, overload
from . import DescLoad, OverloadTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Self


class TestDescLoad(OverloadTest):
  """
  TestDescLoad tests the 'DescLoad' scenario overloading scenario.
  """

  randomInteger = IntSampler(255)

  @classmethod
  def setUpClass(cls) -> None:
    """Sets up the test class."""
    super().setUpClass()

  def setUp(self) -> None:
    """Sets up the test case."""
    super().setUp()
    self.randomInteger.colCount = 3
    self.randomInteger.minVal = 0
    self.randomInteger.maxVal = 255
    self.randomInteger.rowCount = 10

  def test_good_init(self) -> Self:
    """Tests the initialization of the TestDescLoad class."""

    descSample = DescLoad()
    thisSample = DescLoad(descSample)
    self.assertEqual(descSample, thisSample)
    self.assertIn('()', descSample.loaded)

    self.randomInteger.colCount = 1
    self.randomInteger.minVal = 69
    self.randomInteger.maxVal = 420
    for sample in self.randomInteger._getTable():
      x, = sample
      descSample = DescLoad(x)
      thisSample = DescLoad(descSample)
      self.assertEqual(descSample, thisSample)
      self.assertEqual(x, descSample.x)
      self.assertIn('(int)', descSample.loaded)

    self.randomInteger.colCount = 2
    for sample in self.randomInteger._getTable():
      x, y = sample
      descSample = DescLoad(x, y)
      thisSample = DescLoad(descSample)
      self.assertEqual(descSample, thisSample)
      self.assertEqual(x, descSample.x)
      self.assertEqual(y, descSample.y)
      self.assertIn('(int, int)', descSample.loaded)

    self.randomInteger.colCount = 3
    for sample in self.randomInteger._getTable():
      x, y, z = sample
      descSample = DescLoad(x, y, z)
      thisSample = DescLoad(descSample)
      self.assertEqual(descSample, thisSample)
      self.assertEqual(x, descSample.x)
      self.assertEqual(y, descSample.y)
      self.assertEqual(z, descSample.z)
      self.assertIn('(int, int, int)', descSample.loaded)

    self.randomInteger.colCount = 4
    for sample in self.randomInteger._getTable():
      x, y, z, u = sample
      descSample = DescLoad(x, y, z, u)
      thisSample = DescLoad(descSample)
      self.assertEqual(descSample, thisSample)
      self.assertEqual(x, descSample.x)
      self.assertEqual(y, descSample.y)
      self.assertEqual(z, descSample.z)
      self.assertEqual(u, descSample.u)
      self.assertIn('(int, int, int, int)', descSample.loaded)

    self.randomInteger.colCount = 5
    for sample in self.randomInteger._getTable():
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

    self.randomInteger.colCount = 6
    for sample in self.randomInteger._getTable():
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

  def test_overload(self) -> None:
    """Tests the 'Overload' class. """

    def func() -> None:
      """A sample function for testing."""

    sig = TypeSig(int, int)

    load = overload(int, int, )(func, )
    self.assertEqual(load.__name__, func.__name__)
    for s, f in load:
      self.assertEqual(s, sig)
      self.assertIs(f, func)

    with self.assertRaises(AttributeError):
      _ = load.__trolololo__

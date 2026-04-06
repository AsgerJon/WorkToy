"""
TestBaseSampler tests the 'BaseSampler' class of the 'worktoy.markwork'
package.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.waitaminute import TypeException
from . import SamplerTest
from worktoy.work_test.samplers import BaseSampler

if TYPE_CHECKING:  # pragma: no cover
  pass


class FooSampler(BaseSampler):
  def _getValueType(self, **kwargs) -> type:
    return object

  def _getItem(self, *args, **kwargs) -> object:
    return object()


class TestBaseSampler(SamplerTest):
  """
  TestBaseSampler tests the 'BaseSampler' class of the 'worktoy.markwork'
  package.
  """

  def test_dev_null(self, ) -> None:
    """
    This method covers the 'FooSampler'.
    """
    fooSampler = FooSampler()
    self.assertIs(fooSampler.valueType, type(fooSampler.item))
    self.assertIs(fooSampler.valueType, type(fooSampler()))
    i = None
    for i, _ in enumerate(fooSampler):
      pass
    self.assertEqual(i, fooSampler.rowCount - 1)

  def test_counts(self, ) -> None:
    """
    This method tests the 'rowCount' and 'colCount' properties of
    'BaseSampler' instances. As the 'BaseSampler' class is abstract,
    this method creates a subclass.
    """

    fooSampler = FooSampler()
    expectedColCount = FooSampler.__fallback_col_count__
    expectedRowCount = FooSampler.__fallback_row_count__
    self.assertEqual(fooSampler.colCount, expectedColCount)
    self.assertEqual(fooSampler.rowCount, expectedRowCount)

  def test_bad_value_counts(self, ) -> None:
    """
    This method tests the exceptions raised when trying to set 'rowCount'
    and 'colCount' to non-positive values.
    """

    fooSampler = FooSampler()
    with self.assertRaises(ValueError):
      fooSampler.colCount = -69
    with self.assertRaises(ValueError):
      fooSampler.rowCount = -420

  def test_bad_type_counts(self, ) -> None:
    """
    This method tests the exceptions raised when trying to set 'rowCount'
    and 'colCount' to object not of type 'int'.
    """

    fooSampler = FooSampler()
    with self.assertRaises(TypeError):
      fooSampler.colCount = print  # noqa

    fooSampler = FooSampler()
    with self.assertRaises(TypeError):
      fooSampler.rowCount = print  # noqa

  def test_bad_value_type(self, ) -> None:
    """
    Tests a sampler class with inconsistencies between the 'valueType' and
    the instances created.
    """

    class DerpSampler(BaseSampler):
      def _getValueType(self, **kwargs) -> type:
        return int

      def _getItem(self, *args, **kwargs) -> object:
        return object()

    with self.assertRaises(TypeException) as context:
      _ = DerpSampler().row
    e = context.exception
    self.assertEqual(e.varName, 'value')
    self.assertIn(int, e.expectedTypes)

  def test_str_repr(self, ) -> None:
    """
    This method tests the string representations of 'BaseSampler' instances.
    """

    fooSampler = FooSampler()
    strStr = str(fooSampler)
    reprStr = repr(fooSampler)
    self.assertIn('FooSampler', strStr)
    self.assertIn('FooSampler', reprStr)
    self.assertIn('object', strStr)

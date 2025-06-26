"""
TestDataField tests the EZData entries of class DataField from the
'worktoy.ez_data' module.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.ezdata import DataField, EZData, EZMeta

from typing import TYPE_CHECKING

from worktoy.text import stringList
from worktoy.waitaminute import TypeException

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Self


class TestDataField(TestCase):
  """
  TestDataField tests the EZData entries of class DataField from the
  'worktoy.ez_data' module.
  """

  @classmethod
  def tearDownClass(cls) -> None:
    import sys
    import gc
    sys.modules.pop(__name__, None)
    gc.collect()

  def test_good_init(self) -> None:
    """
    Tests that 'DataField' can be instantiated.
    """
    strField = DataField('key', str, 'key')
    intField = DataField('index', int, 69)
    floatField = DataField('value', float, )

  def test_str_repr(self, ) -> None:
    """
    Test the output of DataField.__str__ and __repr__.
    """
    strField = DataField('key', str, 'key')
    intField = DataField('index', int, 69)

    words = stringList("""key, str, DataField""")
    for word in words:
      self.assertIn(word, str(strField))
      self.assertIn(word, repr(strField))
    words = stringList("""index, int, 69, DataField""")
    for word in words:
      self.assertIn(word, str(intField))
      self.assertIn(word, repr(intField))

  def test_bad_init(self) -> None:
    """
    Tests that DataField raises an error when initialized with invalid
    arguments.
    """
    with self.assertRaises(TypeException) as context:
      _ = DataField('key', str, 69)
    e = context.exception
    self.assertEqual(e.varName, 'val')
    self.assertEqual(e.actualObject, 69)
    self.assertEqual(e.actualType, int)
    self.assertIn(str, e.expectedType)

    with self.assertRaises(TypeException) as context:
      _ = DataField(69, str, int)
    e = context.exception
    self.assertEqual(e.varName, 'key')
    self.assertEqual(e.actualObject, 69)
    self.assertEqual(e.actualType, int)
    self.assertIn(str, e.expectedType)

    with self.assertRaises(TypeException) as context:
      _ = DataField('key', 69, 420)
    e = context.exception
    self.assertEqual(e.varName, 'type_')
    self.assertEqual(e.actualObject, 69)
    self.assertEqual(e.actualType, int)
    self.assertIn(type, e.expectedType)

    with self.assertRaises(TypeException) as context:
      _ = DataField('key', type, 1337)
    e = context.exception
    self.assertEqual(e.varName, 'val')
    self.assertEqual(e.actualObject, 1337)
    self.assertEqual(e.actualType, int)
    self.assertIn(type, e.expectedType)

    with self.assertRaises(TypeException) as context:
      _ = DataField('key', type)
    e = context.exception
    self.assertEqual(e.varName, 'val')
    self.assertIsNone(e.actualObject)
    self.assertIs(type(None), e.actualType)
    self.assertIn(type, e.expectedType)

  def test_eq(self) -> None:
    """
    Tests that DataField instances can be compared for equality.
    """
    strField1 = DataField('key', str, 'value')
    strField2 = DataField('key', str, 'value')
    strField3 = DataField('key3', str, 'value')
    strField4 = DataField('key', str, 'other_value')
    strField5 = DataField('index', str, '69')
    intField = DataField('index', int, 69)

    self.assertEqual(strField1, strField2)
    self.assertNotEqual(strField5, intField)
    self.assertNotEqual(intField, strField2)
    self.assertNotEqual(strField1, strField3)
    self.assertNotEqual(strField1, strField4)

    self.assertEqual(intField, 69)
    self.assertEqual(intField, intField)
    self.assertIs(intField.__eq__('breh'), NotImplemented)

  def test_hash(self) -> None:
    """
    Testing that DataField instances can be used as dictionary keys.
    """
    data = dict()
    strField1 = DataField('key', str, 'value')
    strField2 = DataField('key', str, 'value')

    data[strField1] = 'first'
    self.assertIn(strField1, data)
    self.assertIn(strField2, data)
    self.assertEqual(data[strField1], 'first')
    self.assertEqual(data[strField2], 'first')

    dataSet = {strField1, strField2}

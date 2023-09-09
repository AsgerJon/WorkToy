"""Test of CoreClass"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations
from unittest import TestCase

from worktoy.worktoyclass import CoreClass


class TestCoreClass(TestCase):
  """Test of CoreClass"""

  def test_maybe(self):
    """Test the maybe method."""
    coreObj = CoreClass()
    # Test with different types of arguments
    self.assertEqual(coreObj.maybe(None, 1, 2), 1)
    self.assertEqual(coreObj.maybe('a', None, 'b'), 'a')
    self.assertEqual(coreObj.maybe(None, None, 2.5), 2.5)
    # Test with all None values
    self.assertIsNone(coreObj.maybe(None, None, None))
    # Test with no arguments
    self.assertIsNone(coreObj.maybe())

  def test_maybeType(self):
    """Test the maybeType method."""
    coreObj = CoreClass()
    # Test with different types of arguments
    self.assertEqual(coreObj.maybeType(int, 'a', 1, 2.5), 1)
    self.assertEqual(coreObj.maybeType(str, 'a', 1, 'b'), 'a')
    self.assertEqual(coreObj.maybeType(float, None, 1, 2.5), 2.5)
    # Test with all incompatible values
    self.assertIsNone(coreObj.maybeType(int, 'a', 'b'))
    # Test with no arguments
    self.assertIsNone(coreObj.maybeType(int))

  def test_maybeTypes(self):
    """Test the maybeTypes method."""
    coreObj = CoreClass()
    # Test with different types of arguments and the specified types
    self.assertEqual(coreObj.maybeTypes(int, 'a', 1, 2.5), [1, ])
    self.assertEqual(coreObj.maybeTypes(str, 'a', 1, 'b'), ['a', 'b'])
    # Test with all incompatible values
    self.assertEqual(coreObj.maybeTypes(int, 'a', 'b'), [])
    # Test with no arguments
    self.assertEqual(coreObj.maybeTypes(int), [])

  def test_searchKey(self):
    """Test the searchKey method."""
    coreObj = CoreClass()
    self.assertEqual(coreObj.searchKey('a', 'b', a=1, b=2), 1)
    self.assertIsNone(coreObj.searchKey('c', a=1, b=2))

  def test_searchKeys(self):
    """Test the searchKeys method."""
    coreObj = CoreClass()
    self.assertEqual(coreObj.searchKeys('a', 'b', a=1, b=2), [1, 2])
    self.assertIsNone(coreObj.searchKeys('c', a=1, b=2))

  def test_maybeKey(self):
    """Test the maybeKey method."""
    coreObj = CoreClass()
    self.assertEqual(coreObj.maybeKey('a', 'b', a=1, b=2), 1)
    self.assertEqual(coreObj.maybeKey('c', a=1, b=2, c=3), 3)

  def test_maybeKeys(self):
    """Test the maybeKeys method."""
    coreObj = CoreClass()
    self.assertEqual(coreObj.maybeKeys('a', 'b', a=1, b=2), [1, 2])
    self.assertEqual(coreObj.maybeKeys('c', a=1, b=2, c=3), [3])

  def test_empty(self):
    """Test the empty method."""
    coreObj = CoreClass()
    self.assertTrue(coreObj.empty(None, None))
    self.assertFalse(coreObj.empty(None, 1))

  def test_plenty(self):
    """Test the plenty method."""
    coreObj = CoreClass()
    self.assertTrue(coreObj.plenty(1, 2))
    self.assertFalse(coreObj.plenty(None, 1))

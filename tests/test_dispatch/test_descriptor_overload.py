"""
TestDescriptorOverloadBasic runs basic tests for the descriptor overload
functionality.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.dispatch import Dispatcher, TypeSig
from worktoy.waitaminute.dispatch import DispatchException
from . import DispatcherTest
from .examples import PlanePoint, SpacePoint


class TestDescriptorOverloadBasic(DispatcherTest):
  """
  TestDescriptorOverloadBasic runs basic tests for the descriptor overload
  functionality.
  """

  def test_exists(self, ) -> None:
    """Tests that the class exists."""
    self.assertTrue(hasattr(PlanePoint, '__init__'))
    self.assertIsInstance(PlanePoint.__dict__['__init__'], Dispatcher)
    for key, val in PlanePoint.__dict__['__init__'].__sig_funcs__:
      self.assertIsInstance(key, TypeSig)
      self.assertTrue(callable(val))

  def test_good_init(self) -> None:
    """Testing that PlanePoint correctly initializes across all overloads."""
    #  Test with two floats
    point = PlanePoint(0.1337, 0.80085)
    self.assertIsInstance(point, PlanePoint)
    self.assertEqual(point.x, 0.1337)
    self.assertEqual(point.y, 0.80085)
    self.assertEqual(str(point), repr(point))
    #  Test with a complex number
    point = PlanePoint(0.1337 + 0.80085j)
    self.assertIsInstance(point, PlanePoint)
    self.assertEqual(point.x, 0.1337)
    self.assertEqual(point.y, 0.80085)
    self.assertEqual(str(point), repr(point))
    #  Test with another PlanePoint
    other = PlanePoint(0.420, 0.69)
    point = PlanePoint(other)
    self.assertIsInstance(point, PlanePoint)
    self.assertEqual(point.x, 0.420)
    self.assertEqual(point.y, 0.69)
    self.assertEqual(str(point), repr(point))
    #  Test with a single float
    point = PlanePoint(0.69)
    self.assertIsInstance(point, PlanePoint)
    self.assertEqual(point.x, 0.69)
    self.assertEqual(point.y, 0.0)
    self.assertEqual(str(point), repr(point))
    #  Test with no arguments
    point = PlanePoint()
    self.assertIsInstance(point, PlanePoint)
    self.assertEqual(point.x, 0.0)
    self.assertEqual(point.y, 0.0)
    self.assertEqual(str(point), repr(point))

  def test_bad_init(self) -> None:
    """Testing that PlanePoint correctly raises DispatchException on
    unsupported arguments."""
    #  Test with malformed strings
    with self.assertRaises(DispatchException) as context:
      PlanePoint('imma number, trust!')
    e = context.exception
    self.assertIs(e.dispatch, PlanePoint.__dict__['__init__'])
    self.assertEqual(e.posArgs, ('imma number, trust!',))
    self.assertEqual(str(e), repr(e))
    #  Test with a list
    with self.assertRaises(DispatchException) as context:
      PlanePoint([0.1337, 0.80085])
    e = context.exception
    self.assertIs(e.dispatch, PlanePoint.__dict__['__init__'])
    self.assertEqual(e.posArgs, ([0.1337, 0.80085],))
    self.assertEqual(str(e), repr(e))
    #  Test with a dict
    with self.assertRaises(DispatchException) as context:
      PlanePoint({'x': 0.1337, 'y': 0.80085})
    e = context.exception
    self.assertIs(e.dispatch, PlanePoint.__dict__['__init__'])
    self.assertEqual(e.posArgs, ({'x': 0.1337, 'y': 0.80085},))
    self.assertEqual(str(e), repr(e))
    #  Test with a tuple
    with self.assertRaises(DispatchException) as context:
      PlanePoint((0.1337, 0.80085))
    e = context.exception
    self.assertIs(e.dispatch, PlanePoint.__dict__['__init__'])
    self.assertEqual(e.posArgs, ((0.1337, 0.80085),))
    self.assertEqual(str(e), repr(e))

  def test_good_subclass_init(self) -> None:
    """Testing that PlanePoint subclasses can be initialized correctly."""
    point = SpacePoint(0.1337, 0.80085, 0.69)
    self.assertIsInstance(point, SpacePoint)
    self.assertIsInstance(point, PlanePoint)
    self.assertEqual(point.x, 0.1337)
    self.assertEqual(point.y, 0.80085)
    self.assertEqual(point.z, 0.69)
    #  Testing with the same as previous PlanePoint
    #  Testing with complex number
    point = SpacePoint(0.1337 + 0.80085j, )  # Using the parent overload
    self.assertIsInstance(point, SpacePoint)
    self.assertIsInstance(point, PlanePoint)
    self.assertEqual(point.x, 0.1337)
    self.assertEqual(point.y, 0.80085)
    self.assertEqual(point.z, 0.0)
    #  Testing with another SpacePoint
    other = SpacePoint(0.420, 0.69, 0.1337)
    point = SpacePoint(other)  # Testing the replaced overload
    self.assertIsInstance(point, SpacePoint)
    self.assertIsInstance(point, PlanePoint)

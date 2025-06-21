"""
TestBaseOverload tests the simple use of the overload functionality. By
simple, we mean the simple case of overloaded constructors tested on the
class defining them without any inheritance or other complications.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.static import Dispatch
from . import ComplexOverload

try:
  from typing import TYPE_CHECKING
except ImportError:  # pragma: no cover
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  pass


class TestBaseOverload(TestCase):
  """
  TestBaseOverload tests the simple use of the overload functionality. By
  simple, we mean the simple case of overloaded constructors tested on the
  class defining them without any inheritance or other complications.
  """

  def setUp(self, ) -> None:
    """
    Set up the test case by creating an instance of ComplexOverload.
    """
    self.fast1 = (0.80085, 0.1337)
    self.fast2 = (420 + 69j)
    self.cast1 = (69, 420)
    self.cast2 = ('0.80085', '0.1337')
    self.flex1 = ('derp', '420', None, 'breh', '0.69')

  def test_init(self, ) -> None:
    """
    Test that the ComplexOverload can actually be instantiated
    """
    fast1Z = ComplexOverload(*self.fast1)
    self.assertIs(Dispatch.getLatestDispatch(), Dispatch._fastDispatch)
    cast1Z = ComplexOverload(*self.cast1)
    self.assertIs(Dispatch.getLatestDispatch(), Dispatch._castDispatch)
    flex1Z = ComplexOverload(*self.flex1)
    self.assertIs(Dispatch.getLatestDispatch(), Dispatch._flexDispatch)
    fast2Z = ComplexOverload(self.fast2)
    self.assertIs(Dispatch.getLatestDispatch(), Dispatch._fastDispatch)
    cast2Z = ComplexOverload(*self.cast2)
    self.assertIs(Dispatch.getLatestDispatch(), Dispatch._castDispatch)
    fast3Z = ComplexOverload(fast1Z)
    self.assertIs(Dispatch.getLatestDispatch(), Dispatch._fastDispatch)

  def test_good_get(self, ) -> None:
    """
    Test that the RE and IM attributes can be accessed correctly.
    """
    z = ComplexOverload(*self.fast1)
    self.assertEqual(z.RE, self.fast1[0])
    self.assertEqual(z.IM, self.fast1[1])
    z = ComplexOverload(*self.cast1)
    self.assertEqual(z.RE, float(self.cast1[0]))
    self.assertEqual(z.IM, float(self.cast1[1]))
    z = ComplexOverload(*self.flex1)
    self.assertEqual(z.RE, float(self.flex1[1]))
    self.assertEqual(z.IM, float(self.flex1[-1]))
    z = ComplexOverload(self.fast2)
    self.assertEqual(z.RE, self.fast2.real)
    self.assertEqual(z.IM, self.fast2.imag)
    z = ComplexOverload(*self.cast2)
    self.assertEqual(z.RE, float(self.cast2[0]))
    self.assertEqual(z.IM, float(self.cast2[1]))

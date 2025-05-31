"""
TestFlexBox tests the FlexBox class.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase
from math import atan2, pi
from random import random

from worktoy.attr import FlexBox, Field, AttriBox
from worktoy.mcls import BaseMeta, BaseObject
from worktoy.parse import maybe
from worktoy.static import overload
from worktoy.static.zeroton import OWNER, THIS
from worktoy.waitaminute import (DispatchException, TypeException)

from . import ComplexNumber as BaseComplexNumber

try:
  from typing import TYPE_CHECKING
except ImportError:
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Self, Any


class ComplexNumber(BaseComplexNumber, metaclass=BaseMeta):
  """
  Complex number representation with FlexBox attributes.
  """

  susRE = AttriBox[float](0.0)
  susIM = AttriBox[float](0.0)


class Owner:
  z = FlexBox[ComplexNumber](0.0, 0.0)
  w = AttriBox[ComplexNumber](0.0, 0.0)


class TestFlexBox(TestCase):
  """
  TestFlexBox tests the FlexBox class.
  """

  def setUp(self) -> None:
    """
    Set up the test case.
    """
    self.z0 = ComplexNumber()
    self.z1 = ComplexNumber(69, 420)
    self.z2 = ComplexNumber(0.1337, 0.80085)
    self.z3 = ComplexNumber(-69 - 420 * 1j)
    self.z11 = ComplexNumber(self.z1)
    self.owner = Owner()

  def test_attr(self) -> None:
    """
    This tests the attributes of complex number with FlexBox
    implementation.
    """
    self.assertIsInstance(ComplexNumber.RE, FlexBox)
    self.assertIsInstance(ComplexNumber.IM, FlexBox)
    self.assertIsInstance(ComplexNumber.susRE, AttriBox)
    self.assertIsInstance(ComplexNumber.susIM, AttriBox)
    self.assertIsInstance(Owner.z, FlexBox)
    self.assertIsInstance(Owner.w, AttriBox)

  def test_init(self, ) -> None:
    """
    This tests the initialization of complex number with FlexBox
    implementation.
    """
    self.assertIsInstance(self.z0, ComplexNumber)
    self.assertIsInstance(self.z1, ComplexNumber)
    self.assertIsInstance(self.z2, ComplexNumber)
    self.assertIsInstance(self.z3, ComplexNumber)
    self.assertIsInstance(self.z11, ComplexNumber)
    self.assertIsInstance(self.owner, Owner)
    self.assertIsInstance(self.owner.z, ComplexNumber)
    self.assertIsInstance(self.owner.w, ComplexNumber)

  def test_get(self, ) -> None:
    """
    Tests that the correct values are returned from the FlexBox
    """
    self.assertAlmostEqual(self.z0.RE, 0.0)
    self.assertAlmostEqual(self.z0.IM, 0.0)
    self.assertAlmostEqual(self.z1.RE, 69.0)
    self.assertAlmostEqual(self.z1.IM, 420.0)
    self.assertAlmostEqual(self.z2.RE, 0.1337)
    self.assertAlmostEqual(self.z2.IM, 0.80085)
    self.assertAlmostEqual(self.z3.RE, -69.0)
    self.assertAlmostEqual(self.z3.IM, -420.0)
    self.assertAlmostEqual(self.z11.RE, 69.0)
    self.assertAlmostEqual(self.z11.IM, 420.0)
    self.assertAlmostEqual(self.owner.z.RE, 0.0)
    self.assertAlmostEqual(self.owner.z.IM, 0.0)

  def test_good_set(self, ) -> None:
    """
    Tests that the correct values are set in the FlexBox
    """
    #  z0 from 0 to 69 + 420j
    self.assertAlmostEqual(self.z0.RE, 0.0)
    self.assertAlmostEqual(self.z0.IM, 0.0)
    self.z0.RE = 69.0
    self.z0.IM = 420.0
    self.assertAlmostEqual(self.z0.RE, 69.0)
    self.assertAlmostEqual(self.z0.IM, 420.0)
    #  z1 from 69 + 420j to 1337 + 80085j
    self.assertAlmostEqual(self.z1.RE, 69.0)
    self.assertAlmostEqual(self.z1.IM, 420.0)
    self.z1.RE = 1337.0
    self.z1.IM = 80085.0
    self.assertAlmostEqual(self.z1.RE, 1337.0)
    self.assertAlmostEqual(self.z1.IM, 80085.0)
    #  z2 from 0.1337 + 0.80085j to 69 + 420j
    self.assertAlmostEqual(self.z2.RE, 0.1337)
    self.assertAlmostEqual(self.z2.IM, 0.80085)
    self.z2.RE = 69.0
    self.z2.IM = 420.0
    self.assertAlmostEqual(self.z2.RE, 69.0)
    self.assertAlmostEqual(self.z2.IM, 420.0)
    #  z3 from -69 - 420j to 0.1337 + 0.80085j
    self.assertAlmostEqual(self.z3.RE, -69.0)
    self.assertAlmostEqual(self.z3.IM, -420.0)
    self.z3.RE = 0.1337
    self.z3.IM = 0.80085
    self.assertAlmostEqual(self.z3.RE, 0.1337)
    self.assertAlmostEqual(self.z3.IM, 0.80085)
    #  z11 from 69 + 420j to -69 - 420j
    self.assertAlmostEqual(self.z11.RE, 69.0)
    self.assertAlmostEqual(self.z11.IM, 420.0)
    self.z11.RE = -69.0
    self.z11.IM = -420.0
    self.assertAlmostEqual(self.z11.RE, -69.0)
    self.assertAlmostEqual(self.z11.IM, -420.0)
    #  owner.z from 0 + 0j to 69 + 420j
    self.assertAlmostEqual(self.owner.z.RE, 0.0)
    self.assertAlmostEqual(self.owner.z.IM, 0.0)
    self.owner.z = ComplexNumber(69, 420)
    self.assertAlmostEqual(self.owner.z.RE, 69.0)
    self.assertAlmostEqual(self.owner.z.IM, 420.0)
    #  owner.w from 0 + 0j to 69 + 420j
    self.assertAlmostEqual(self.owner.w.RE, 0.0)
    self.assertAlmostEqual(self.owner.w.IM, 0.0)
    self.owner.w = ComplexNumber(69, 420)
    self.assertAlmostEqual(self.owner.w.RE, 69.0)
    self.assertAlmostEqual(self.owner.w.IM, 420.0)
    #  owner.z from 69 + 420j to 1337 + 80085j
    self.assertAlmostEqual(self.owner.z.RE, 69.0)
    self.assertAlmostEqual(self.owner.z.IM, 420.0)
    self.owner.z = 1337 + 80085j
    self.assertAlmostEqual(self.owner.z.RE, 1337.)
    self.assertAlmostEqual(self.owner.z.IM, 80085.)
    #  owner.w is an AttriBox, so should raise TypeException
    newValue = 1337 + 80085j
    with self.assertRaises(TypeException) as context:
      self.owner.w = newValue
    e = context.exception
    self.assertEqual(e.varName, 'w')
    self.assertEqual(e.actualObject, newValue)
    self.assertIn(ComplexNumber, e.expectedType)

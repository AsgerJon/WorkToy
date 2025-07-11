"""
TestComplex tests that the ComplexOverload helper class functions
correctly.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.desc import AttriBox
from worktoy.mcls import BaseMeta, BaseObject
from . import ComplexOverload, OverloadTest

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestComplex(OverloadTest):
  """
  TestComplex tests that the ComplexOverload helper class functions
  correctly.
  """

  def test_metaclass(self, ) -> None:
    """
    Test that the ComplexOverload actually exists and is a class derived
    from BaseMeta.
    """
    self.assertIsInstance(ComplexOverload, type)
    self.assertIsInstance(ComplexOverload, BaseMeta)

  def test_baseclass(self, ) -> None:
    """
    Test that ComplexOverload is a subclass of ComplexBase.
    """
    self.assertTrue(issubclass(ComplexOverload, BaseObject))

  def test_attribox(self) -> None:
    """
    Test that the RE and IM attributes are AttriBox instances.
    """
    self.assertIsInstance(ComplexOverload.RE, AttriBox)
    self.assertIsInstance(ComplexOverload.IM, AttriBox)

  def test_init(self) -> None:
    """
    Test that the ComplexOverload can be initialized with various
    parameters.
    """
    z1 = ComplexOverload(3.0, 4.0)
    self.assertEqual(z1.RE, 3.0)
    self.assertEqual(z1.IM, 4.0)

    z2 = ComplexOverload(complex(5.0, 6.0))
    self.assertEqual(z2.RE, 5.0)
    self.assertEqual(z2.IM, 6.0)

    z3 = ComplexOverload(z1)
    self.assertEqual(z3.RE, 3.0)
    self.assertEqual(z3.IM, 4.0)

    z4 = ComplexOverload()
    self.assertEqual(z4.RE, 0.0)
    self.assertEqual(z4.IM, 0.0)

  def test_init_kwargs(self) -> None:
    """
    Test that the ComplexOverload can be initialized with keyword arguments.
    """
    z5 = ComplexOverload(re=7.0, im=8.0)
    self.assertEqual(z5.RE, 7.0)
    self.assertEqual(z5.IM, 8.0)

    z5 = ComplexOverload(69, 420, re=7.0, im=8.0)
    self.assertEqual(z5.RE, 7.0)
    self.assertEqual(z5.IM, 8.0)

    z5 = ComplexOverload(z5, re=7.0, im=8.0)
    self.assertEqual(z5.RE, 7.0)
    self.assertEqual(z5.IM, 8.0)

    z6 = ComplexOverload(69 + 420j, x=9.0, y=10.0)
    self.assertEqual(z6.RE, 9.0)
    self.assertEqual(z6.IM, 10.0)

    z7 = ComplexOverload(real=11.0, imag=12.0)
    self.assertEqual(z7.RE, 11.0)
    self.assertEqual(z7.IM, 12.0)

  def test_bad_init_kwargs(self) -> None:
    """
    Test that initializing with bad keyword arguments raises an error.
    """

    z0 = ComplexOverload(never=0, gonna=1, give=2, you=3, up=4)
    self.assertAlmostEqual(z0.RE, 0.0)
    self.assertAlmostEqual(z0.IM, 0.0)

    z0 = ComplexOverload(z0, never=0, gonna=1, give=2, you=3, up=4)
    self.assertAlmostEqual(z0.RE, 0.0)
    self.assertAlmostEqual(z0.IM, 0.0)

    z0 = ComplexOverload(69 + 420j, never=0, gonna=1, give=2, you=3, up=4)
    self.assertAlmostEqual(z0.RE, 0.0)
    self.assertAlmostEqual(z0.IM, 0.0)

    z0 = ComplexOverload(69, 420, never=0, gonna=1, give=2, you=3, up=4)
    self.assertAlmostEqual(z0.RE, 0.0)
    self.assertAlmostEqual(z0.IM, 0.0)

    z0 = ComplexOverload(69., 420., real=1337)
    self.assertAlmostEqual(z0.RE, 0.0)
    self.assertAlmostEqual(z0.IM, 0.0)

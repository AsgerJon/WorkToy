"""
TestComplex tests that the ComplexOverload helper class functions
correctly.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.desc import AttriBox
from worktoy.mcls import BaseMeta

from . import ComplexOverload

from tests import ComplexBase

from typing import TYPE_CHECKING


class TestComplex(TestCase):
  """
  TestComplex tests that the ComplexOverload helper class functions
  correctly.
  """

  @classmethod
  def tearDownClass(cls) -> None:
    import sys
    import gc
    sys.modules.pop(__name__, None)
    gc.collect()

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
    self.assertTrue(issubclass(ComplexOverload, ComplexBase))

  def test_attribox(self) -> None:
    """
    Test that the RE and IM attributes are AttriBox instances.
    """
    self.assertIsInstance(ComplexOverload.RE, AttriBox)
    self.assertIsInstance(ComplexOverload.IM, AttriBox)

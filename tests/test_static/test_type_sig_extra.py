"""
TestTypeSigExtra tests auxiliary functionality of the 'TypeSig' class from
the 'worktoy.static' module. This includes test for the functionality not
required for the central functionality of the 'TypeSig' class, such as
'__repr__', '__str__' and '__eq__' methods.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase
from typing import TYPE_CHECKING

from worktoy.static import TypeSig

if TYPE_CHECKING:  # pragma: no cover
  from typing import Self


class TestTypeSigExtra(TestCase):
  """
  TestTypeSigExtra tests auxiliary functionality of the 'TypeSig' class from
  the 'worktoy.static' module. This includes test for the functionality not
  required for the central functionality of the 'TypeSig' class, such as
  '__repr__', '__str__' and '__eq__' methods.
  """

  @classmethod
  def tearDownClass(cls) -> None:
    import sys
    import gc
    sys.modules.pop(__name__, None)
    gc.collect()

  def test_str_repr(self: Self) -> None:
    """
    Test the __repr__ method of TypeSig.
    """
    sig = TypeSig(int, str)
    self.assertEqual(str(sig), "TypeSig: [int, str]")
    self.assertEqual(repr(sig), "TypeSig(int, str)")

  def test_eq(self: Self) -> None:
    """
    Test the __eq__ method of TypeSig.
    """
    sig1 = TypeSig(int, str)
    sig2 = TypeSig(int, str)
    sig3 = TypeSig(str, int)

    self.assertEqual(sig1, sig2)  # Same types
    self.assertNotEqual(sig1, sig3)  # Different types
    self.assertNotEqual(sig1, "not a TypeSig")  # Different type

    res = TypeSig.__eq__(sig1, 'imma type sig, trust!')
    self.assertIs(res, NotImplemented)

  def test_in(self) -> None:
    """
    Test the __contains__ method of TypeSig.
    """
    sig = TypeSig(int, str)
    self.assertIn(int, sig)
    self.assertIn(str, sig)
    self.assertNotIn(float, sig)

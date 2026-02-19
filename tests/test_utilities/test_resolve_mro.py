"""
TestResolveMRO tests the resolveMRO function from the 'worktoy.utilities'
module.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.utilities import resolveMRO
from . import UtilitiesTest


class TestResolveMRO(UtilitiesTest):
  """
  TestResolveMRO tests the resolveMRO function from the 'worktoy.utilities'
  module.
  """

  def test_good_mro(self) -> None:
    """
    Test that resolveMRO returns the correct MRO for a class with multiple
    inheritance.
    """

    class A:
      pass

    class B(A):
      pass

    class C(A):
      pass

    mro = resolveMRO(B, C)
    expected_mro = [B, C, A, object]
    self.assertEqual(mro, expected_mro)

  def test_bad_mro(self, ) -> None:
    """
    Test that resolveMRO correctly raises an error when receiving base
    classes that cannot form a valid MRO.
    """

    class X:
      pass

    class Y:
      pass

    class Z(X, Y):
      pass

    class W(Y, X):
      pass

    with self.assertRaises(TypeError) as context:
      resolveMRO(Z, W)
    e = context.exception
    self.assertIn(str('cannot form a consistent mro'), str(e))

  def test_recursion_guard(self) -> None:
    """
    Test that resolveMRO raises a RecursionError when the MRO resolution
    exceeds the maximum recursion depth.
    """

    class A:
      pass

    class B(A):
      pass

    class C(A):
      pass

    with self.assertRaises(RecursionError):
      resolveMRO(B, C, _start=1337)

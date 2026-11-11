"""
PromiseResolveMRO promises 'resolveMRO' from 'worktoy.utilities'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.utilities import resolveMRO


class PromiseResolveMRO(TestCase):
  """
  'resolveMRO(*bases)' gives, as a list, the resolution order a class
  with these bases would have, the class itself left out: for 'class
  Foo(*bases)' it equals 'Foo.mro()[1:]'. No bases give an empty list,
  one base its own '__mro__', and bases Python would refuse raise
  'TypeError', as the class statement does. Source: the 'resolveMRO'
  docstring and its example.
  """

  def test_diamond(self) -> None:
    class A:
      pass

    class B(A):
      pass

    class C(A):
      pass

    class Foo(B, C):
      pass

    self.assertEqual(resolveMRO(B, C), [B, C, A, object])
    self.assertEqual(resolveMRO(B, C), Foo.mro()[1:])

  def test_zero_and_one(self) -> None:
    class A:
      pass

    self.assertEqual(resolveMRO(), [])
    self.assertEqual(resolveMRO(A), [A, object])

  def test_inconsistent(self) -> None:
    class A:
      pass

    class B(A):
      pass

    with self.assertRaises(TypeError):
      resolveMRO(A, B)

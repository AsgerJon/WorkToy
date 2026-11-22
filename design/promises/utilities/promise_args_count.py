"""
PromiseArgsCount promises 'argsCount' from 'worktoy.utilities'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.utilities import argsCount


class PromiseArgsCount(TestCase):
  """
  'argsCount(func)' counts the positional parameters of 'func', leaving
  out '*args', '**kwargs' and keyword-only parameters. A bound method
  counts 'self' too. Source: the 'argsCount' docstring and its example.
  """

  def test_counts(self) -> None:
    self.assertEqual(argsCount(lambda a, b, *args, c=0: None), 2)
    self.assertEqual(argsCount(lambda: None), 0)

  def test_bound_method_counts_self(self) -> None:
    class Greeter:
      def greet(self, name: str, *, loud: bool = False) -> str:
        return name

    self.assertEqual(argsCount(Greeter().greet), 2)
    self.assertEqual(argsCount(Greeter.greet), 2)

"""
PromiseBodyChecks promises the checks the namespace of a worktoy class
runs on its body, from 'worktoy.mcls'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.mcls import BaseObject


class PromiseBodyChecks(TestCase):
  """
  All are 'SyntaxError's. Source: the docstrings of 'NamespaceHook',
  'ReservedNames' and these exceptions.
  """

  def test_finalizer(self) -> None:
    class Trusted(BaseObject, trustMeBro=True):
      def __del__(self) -> None:
        pass

    self.assertTrue(callable(Trusted.__del__))

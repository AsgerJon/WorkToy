"""
PromiseHasCastRule promises 'hasCastRule' from 'worktoy.utilities'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.utilities import hasCastRule


class PromiseHasCastRule(TestCase):
  """
  'hasCastRule(target)' tells whether 'typeCast' decides for 'target': True
  for the number and text builtins, for a subclass of one, and for any class
  with a '__cast_as__' classmethod; False for every other class. Source: the
  'hasCastRule' docstring.
  """

  def test_rules(self) -> None:
    class Meters(float):
      pass

    class Count:
      @classmethod
      def __cast_as__(cls, value):
        return NotImplemented

    for target in (int, float, bool, complex, str, bytes, bytearray):
      with self.subTest(target=target):
        self.assertTrue(hasCastRule(target))
    self.assertTrue(hasCastRule(Meters))
    self.assertTrue(hasCastRule(Count))

  def test_no_rule(self) -> None:
    class Plain:
      pass

    self.assertFalse(hasCastRule(Plain))
    self.assertFalse(hasCastRule(list))

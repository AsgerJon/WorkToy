"""
PromiseFixBox promises 'FixBox' from 'worktoy.desc'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.desc import FixBox
from worktoy.mcls import BaseObject


class PromiseFixBox(TestCase):
  """
  A 'FixBox' is an 'AttriBox' whose first stored value is final. A read
  stores the default it builds, so a value meant to be set at run time is
  assigned before anything reads it. Source: the 'FixBox' docstring and its
  example.
  """

  def test_first_value_final(self) -> None:
    class Config(BaseObject):
      port = FixBox[int](8080)

    config = Config()
    config.port = 9000
    self.assertEqual(config.port, 9000)

  def test_read_fixes_default(self) -> None:
    class Config(BaseObject):
      port = FixBox[int](8080)

    config = Config()
    self.assertEqual(config.port, 8080)

"""
TestLoremIpsumPackage tests the public face of 'worktoy.lorem_ipsum'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy import lorem_ipsum
from worktoy.mcls import BaseObject
from . import LoremTest


class TestLoremIpsumPackage(LoremTest):
  """
  The package exports the three word lists, the three distributions and
  the four generators. The tests pin the exports and the layering: the
  distributions and the generators are worktoy classes based on
  'BaseObject', and the generators share 'BaseGenerator'.
  """

  def test_exports(self) -> None:
    expected = [
      'COMMON_WORDS', 'UNCOMMON_WORDS', 'RARE_WORDS',
      'StochasticVariable', 'GaussianLengths', 'StochasticWord',
      'BaseGenerator', 'Clause', 'Sentence', 'Paragraph',
    ]
    self.assertEqual(lorem_ipsum.__all__, expected)
    for name in expected:
      with self.subTest(name=name):
        self.assertTrue(hasattr(lorem_ipsum, name))

  def test_layering(self) -> None:
    variable = lorem_ipsum.StochasticVariable
    self.assertIsSubclass(variable, BaseObject)
    self.assertIsSubclass(lorem_ipsum.GaussianLengths, variable)
    self.assertIsSubclass(lorem_ipsum.StochasticWord, variable)
    generator = lorem_ipsum.BaseGenerator
    self.assertIsSubclass(generator, BaseObject)
    for name in ('Clause', 'Sentence', 'Paragraph'):
      with self.subTest(name=name):
        self.assertIsSubclass(getattr(lorem_ipsum, name), generator)

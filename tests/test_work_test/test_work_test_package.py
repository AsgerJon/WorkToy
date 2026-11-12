"""
TestWorkTestPackage tests the public face of 'worktoy.work_test'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import ast
import glob
import os
from pathlib import Path
from unittest import TestCase

from worktoy import work_test
from worktoy.mcls import BaseMeta, BaseObject
from worktoy.work_test import BaseTest, SubTest, ComplexMixin, ComplexTest
from worktoy.work_test import samplers
from worktoy.work_test.samplers import BaseSampler, SamplerMeta
from . import WorkTestTest


class TestWorkTestPackage(WorkTestTest):
  """
  The package exports the samplers, 'SubTest', 'TestSpace', 'TestMeta',
  'BaseTest', the worked example 'ComplexMixin' and its bank
  'ComplexTest', and the samplers subpackage exports its text, its
  metaclass, its base and the six samplers. 'BaseTest' is a
  'unittest.TestCase' built by 'TestMeta' in a 'TestSpace',
  'SubTest' is a 'TestCase' and no 'BaseTest', the bank is no test case
  at all, and every sampler is a 'BaseObject' built by 'SamplerMeta'.
  The package is a leaf that imports no other leaf, so a project may
  take its testing support without 'lorem_ipsum', 'keenum' or 'ezdata'.
  The tests pin the exports, the layering and that independence, the
  last by reading every import statement of the package.
  """

  def test_exports(self) -> None:
    expected = ['samplers', 'SubTest', 'TestSpace', 'TestMeta',
                'BaseTest', 'ComplexMixin', 'ComplexTest']
    self.assertEqual(work_test.__all__, expected)
    for name in expected:
      with self.subTest(name=name):
        self.assertTrue(hasattr(work_test, name))
    expected = [
      'LOREM_WORDS', 'randomWord', 'loremSentence', 'SamplerMeta',
      'BaseSampler', 'IntSampler', 'FloatSampler', 'GaussianSampler',
      'SymbolicSampler', 'WordSampler', 'LoremSampler',
    ]
    self.assertEqual(samplers.__all__, expected)
    for name in expected:
      with self.subTest(name=name):
        self.assertTrue(hasattr(samplers, name))

  def test_layering(self) -> None:
    self.assertIsSubclass(BaseTest, TestCase)
    self.assertIs(type(BaseTest), BaseMeta)
    #  Read through the package: bound here under its own name, pytest
    #  would take 'TestMeta' for a test class and warn.
    self.assertIsSubclass(work_test.TestMeta, BaseMeta)
    self.assertIsSubclass(SubTest, TestCase)
    self.assertIsNotSubclass(SubTest, BaseTest)
    self.assertIsNotSubclass(ComplexTest, TestCase)
    self.assertIsNotSubclass(ComplexMixin, BaseObject)
    self.assertIsSubclass(BaseSampler, BaseObject)
    self.assertIs(type(BaseSampler), SamplerMeta)
    for name in ('IntSampler', 'FloatSampler', 'GaussianSampler',
                 'SymbolicSampler', 'WordSampler', 'LoremSampler'):
      with self.subTest(name=name):
        self.assertIsSubclass(getattr(samplers, name), BaseSampler)

  def test_imports_no_other_leaf(self) -> None:
    root = os.path.dirname(work_test.__file__)
    leaves = ('worktoy.lorem_ipsum', 'worktoy.keenum', 'worktoy.ezdata')
    seen = []
    for path in glob.glob(os.path.join(root, '**', '*.py'), recursive=True):
      for name in self._importedNames(root, path):
        seen.append(name)
        for leaf in leaves:
          self.assertFalse(name == leaf or name.startswith(leaf + '.'),
                           '%s imports %s' % (path, name))
    self.assertIn('worktoy.desc', seen)
    self.assertIn('worktoy.mcls', seen)
    self.assertIn('worktoy.work_test.samplers', seen)

  @staticmethod
  def _importedNames(root: str, path: str) -> list:
    """The absolute name each import statement of the file reaches."""
    folder = os.path.relpath(os.path.dirname(path), root)
    package = ['worktoy', 'work_test', *folder.split(os.sep)]
    package = [part for part in package if part != '.']
    names = []
    for node in ast.walk(ast.parse(Path(path).read_text(encoding='utf-8'))):
      if isinstance(node, ast.Import):
        names.extend(alias.name for alias in node.names)
      elif isinstance(node, ast.ImportFrom):
        names.append(TestWorkTestPackage._fromName(package, node))
    return names

  @staticmethod
  def _fromName(package: list, node: ast.ImportFrom) -> str:
    """The absolute name a 'from' import reaches, relative ones resolved."""
    if not node.level:
      return str(node.module)
    base = package[:len(package) - node.level + 1]
    return str.join('.', base + [*filter(None, [node.module])])

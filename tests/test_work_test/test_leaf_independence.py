"""
TestLeafIndependence subclasses 'BaseTest' from 'worktoy.work_test' and
pins that the 'worktoy.work_test' package imports nothing from the leaf
packages 'lorem_ipsum', 'keenum' and 'ezdata'. The test suite stands on
'work_test', so a rewrite of the tests that sets the leaf packages aside
must still have its testing support; 'work_test' used to draw its text
from 'lorem_ipsum'. The check reads the import statements of every module
in the package with 'ast' and resolves relative imports against the
package of the module, so a dependency cannot hide behind a relative
spelling.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

import ast
import os
from importlib.util import resolve_name

import worktoy
from worktoy import work_test
from worktoy.work_test import BaseTest

_LEAVES = ('worktoy.lorem_ipsum', 'worktoy.keenum', 'worktoy.ezdata')


def _moduleName(path: str) -> str:
  """The dotted name of the module at 'path' under the 'worktoy' package
  directory."""
  root = os.path.dirname(os.path.dirname(worktoy.__file__))
  parts = os.path.relpath(path, root)[:-3].split(os.sep)
  if parts[-1] == '__init__':
    parts = parts[:-1]
  return '.'.join(parts)


def _importedNames(path: str) -> list[str]:
  """Every module an import statement in the file at 'path' names, as an
  absolute dotted name."""
  f = None
  try:
    f = open(path, encoding='utf-8')
  except OSError as osError:
    raise osError
  else:
    source = f.read()
  finally:
    try:
      f.close()
    except AttributeError:
      pass
  tree = ast.parse(source, filename=path)
  moduleName = _moduleName(path)
  if os.path.basename(path) == '__init__.py':
    package = moduleName
  else:
    package = moduleName.rpartition('.')[0]
  out = []
  for node in ast.walk(tree):
    if isinstance(node, ast.Import):
      out.extend(alias.name for alias in node.names)
    elif isinstance(node, ast.ImportFrom):
      spec = '.' * node.level + (node.module or '')
      out.append(resolve_name(spec, package) if node.level else spec)
  return out


def _sourceFiles() -> list[str]:
  """Every '.py' file of the 'worktoy.work_test' package, sorted."""
  root = os.path.dirname(work_test.__file__)
  out = []
  for folder, _, files in os.walk(root):
    for file in files:
      if file.endswith('.py'):
        out.append(os.path.join(folder, file))
  return sorted(out)


class TestLeafIndependence(BaseTest):
  """
  TestLeafIndependence provides tests for the imports of the
  'worktoy.work_test' package.
  """

  def test_helper_resolves_relative_imports(self) -> None:
    """The helper reads a relative import back as the absolute name of
    the package it reaches, so the check below is not vacuous."""
    path = os.path.join(os.path.dirname(work_test.__file__), '_base_test.py')
    names = _importedNames(path)
    self.assertIn('worktoy.desc', names)
    self.assertIn('worktoy.mcls', names)
    self.assertIn('worktoy.work_test', names)

  def test_no_leaf_imports(self) -> None:
    """No module of 'worktoy.work_test' names a leaf package in an import
    statement."""
    paths = _sourceFiles()
    self.assertGreater(len(paths), 5)
    offenders = []
    root = os.path.dirname(work_test.__file__)
    for path in paths:
      for name in _importedNames(path):
        for leaf in _LEAVES:
          if name == leaf or name.startswith('%s.' % leaf):
            where = os.path.relpath(path, root)
            offenders.append('%s imports %s' % (where, name))
    self.assertEqual(offenders, [])

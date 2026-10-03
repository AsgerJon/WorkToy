"""
TestDeepGetItem subclasses 'MCLSTest' and pins 'AbstractNamespace'
'deepGetItem' and 'getMROSpace'. 'deepGetItem' finds a name in the
namespace itself, then in the compiled namespaces along the method
resolution order, which it now builds once per call. 'getMROSpace'
follows the lookup order of the namespace, so a namespace built with
'_strictMRO=False', which has no resolved order, answers instead of
iterating 'None'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.mcls import BaseMeta, BaseObject, BaseSpace

from .. import MCLSTest


class Parent(BaseObject):
  """Parent binds 'shared' and 'parentOnly'."""

  shared = 'parent'
  parentOnly = 'parent only'


class X(BaseObject):
  """X is one of two bases whose orders conflict."""


class Y(BaseObject):
  """Y is the other."""


class XY(X, Y):
  """XY puts 'X' before 'Y'."""

  marker = 'xy'


class YX(Y, X):
  """YX puts 'Y' before 'X'."""


class TestDeepGetItem(MCLSTest):
  """
  TestDeepGetItem provides tests for 'deepGetItem' and 'getMROSpace'.
  """

  def test_own_value(self) -> None:
    """A name the namespace holds is returned as itself."""
    space = BaseSpace(BaseMeta, 'Child', (Parent,))
    space['shared'] = 'child'
    self.assertEqual(space.deepGetItem('shared'), 'child')

  def test_inherited_values(self) -> None:
    """A name only a base holds is the list of the values along the
    method resolution order."""
    space = BaseSpace(BaseMeta, 'Child', (Parent,))
    self.assertEqual(space.deepGetItem('parentOnly'), ['parent only'])

  def test_missing(self) -> None:
    """A name nothing holds raises 'KeyError'."""
    space = BaseSpace(BaseMeta, 'Child', (Parent,))
    with self.assertRaises(KeyError):
      space.deepGetItem('nowhere')

  def test_no_resolved_order(self) -> None:
    """A namespace without a resolved order still combines the compiled
    namespaces of its bases."""
    space = BaseSpace(BaseMeta, 'Neither', (XY, YX), _strictMRO=False)
    self.assertIsNone(space.getMRO())
    self.assertEqual(space.getMROSpace()['marker'], ['xy'])
    self.assertEqual(space.deepGetItem('marker'), ['xy'])

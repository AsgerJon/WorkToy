"""
The TestBaseSpace class tests the BaseSpace class which provides the
namespace used by BaseMeta to implement the overload protocol used across
the 'worktoy' library.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase
from typing import TYPE_CHECKING

from worktoy.mcls import AbstractMetaclass, BaseSpace
from worktoy.waitaminute import VariableNotNone
from worktoy.waitaminute import _Attribute  # NOQA

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias

  Bases: TypeAlias = tuple[type, ...]


class TestBaseSpace(TestCase):
  """
  TestBaseSpace tests the BaseSpace class which provides the namespace used
  by BaseMeta to implement the overload protocol used across the 'worktoy'
  library.
  """

  @classmethod
  def tearDownClass(cls):
    import sys
    import gc
    sys.modules.pop(__name__, None)
    gc.collect()

  def test_unexpected_overload_map(self) -> None:
    """
    Tests that duplicate calls to the '_buildOverloadMap' method raises
    'VariableNotNone' exception.
    """
    space = BaseSpace(AbstractMetaclass, 'derp', (), **{})
    space._buildOverloadMap()
    with self.assertRaises(VariableNotNone) as context:
      space._buildOverloadMap()
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertEqual(e.name, '__overload_map__')
    self.assertFalse(e.value, )

  def test_overload_map_recursion(self) -> None:
    """
    Tests that 'BaseSpace' correctly raises recursion errors if
    'getOverloadMap' invokes '_buildOverloadMap' but somehow this
    invocation fails to build the overload map.
    """
    with self.assertRaises(RecursionError):
      space = BaseSpace(AbstractMetaclass, 'derp', (), **{})
      space.getOverloadMap(_recursion=True)
